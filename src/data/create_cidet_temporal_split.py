"""
create_cidet_temporal_split.py

CIDET için calendar-day-grouped temporal train/validation/test split üretir.

Amaçlar:
1. Aynı takvim gününe ait tüm görüntüler aynı splitte kalır.
2. Yaklaşık 70/15/15 örnek oranı korunur.
3. Visibility target dağılımı splitler arasında mümkün olduğunca benzer kalır.
4. Sonuç RANDOM_SEED ile deterministiktir.

Birden fazla aday grup bölünmesi üretilir ve global objective score
üzerinden en iyi aday seçilir.
"""

from pathlib import Path
import random
import re

import numpy as np
import pandas as pd


RANDOM_SEED = 42

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15

N_VISIBILITY_BINS = 5

N_SEARCH_ITERATIONS = 10000


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CIDET_INTERIM = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "cidet"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cidet"
    / "temporal_split"
)


def find_required_file(filename: str) -> Path:
    matches = list(
        CIDET_INTERIM.rglob(filename)
    )

    if not matches:
        raise FileNotFoundError(
            f"Required CIDET file not found: {filename}"
        )

    if len(matches) > 1:
        locations = "\n".join(
            str(path)
            for path in matches
        )

        raise RuntimeError(
            f"Multiple files named {filename} found:\n"
            f"{locations}"
        )

    return matches[0]


def load_split(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        header=None,
        names=["image_name"],
    )

    df["image_name"] = (
        df["image_name"]
        .astype(str)
        .str.strip()
    )

    return df


def parse_image_timestamp(
    filename: str,
) -> pd.Timestamp:
    match = re.search(
        r"(\d{8})-(\d{6})",
        filename,
    )

    if match is None:
        return pd.NaT

    return pd.to_datetime(
        f"{match.group(1)}{match.group(2)}",
        format="%Y%m%d%H%M%S",
        errors="coerce",
    )


def build_valid_dataset() -> pd.DataFrame:
    annotation_path = find_required_file(
        "tabular_data_and_visibility_annotation.csv"
    )

    train_path = find_required_file(
        "images_train.csv"
    )

    validation_path = find_required_file(
        "images_val.csv"
    )

    test_path = find_required_file(
        "images_test.csv"
    )

    annotations = pd.read_csv(
        annotation_path
    )

    official_images = pd.concat(
        [
            load_split(train_path),
            load_split(validation_path),
            load_split(test_path),
        ],
        ignore_index=True,
    )

    if official_images[
        "image_name"
    ].duplicated().any():
        raise ValueError(
            "Duplicate image names detected in "
            "official CIDET splits."
        )

    dataset = official_images.merge(
        annotations,
        on="image_name",
        how="left",
        validate="one_to_one",
    )

    target_column = (
        "visibility estimation average"
    )

    dataset[target_column] = (
        pd.to_numeric(
            dataset[target_column],
            errors="coerce",
        )
    )

    if dataset[
        target_column
    ].isna().any():
        raise ValueError(
            "Missing visibility target detected."
        )

    dataset["timestamp"] = (
        dataset[
            "image_name"
        ].apply(
            parse_image_timestamp
        )
    )

    if dataset[
        "timestamp"
    ].isna().any():
        raise ValueError(
            "Timestamp parsing failed."
        )

    dataset["date"] = (
        dataset["timestamp"]
        .dt.strftime("%Y-%m-%d")
    )

    return dataset


def add_visibility_bins(
    dataset: pd.DataFrame,
) -> pd.DataFrame:
    dataset = dataset.copy()

    target_column = (
        "visibility estimation average"
    )

    dataset["visibility_bin"] = (
        pd.qcut(
            dataset[
                target_column
            ],
            q=N_VISIBILITY_BINS,
            labels=False,
            duplicates="drop",
        )
    )

    if dataset[
        "visibility_bin"
    ].isna().any():
        raise ValueError(
            "Visibility bin assignment failed."
        )

    dataset["visibility_bin"] = (
        dataset[
            "visibility_bin"
        ].astype(int)
    )

    return dataset


def build_day_groups(
    dataset: pd.DataFrame,
) -> list[dict]:
    n_bins = (
        dataset[
            "visibility_bin"
        ].nunique()
    )

    groups = []

    for date, frame in dataset.groupby(
        "date",
        sort=True,
    ):
        histogram = np.bincount(
            frame[
                "visibility_bin"
            ].to_numpy(),
            minlength=n_bins,
        ).astype(float)

        groups.append(
            {
                "date": date,
                "count": len(frame),
                "histogram": histogram,
                "mean_visibility": frame[
                    "visibility estimation average"
                ].mean(),
            }
        )

    return groups


def partition_candidate(
    groups: list[dict],
    rng: random.Random,
    total_samples: int,
) -> dict[str, list[dict]]:
    shuffled = groups.copy()

    rng.shuffle(
        shuffled
    )

    train_target = (
        total_samples
        * TRAIN_RATIO
    )

    validation_target = (
        total_samples
        * VALIDATION_RATIO
    )

    cumulative_counts = (
        np.cumsum(
            [
                group["count"]
                for group in shuffled
            ]
        )
    )

    train_cut = int(
        np.argmin(
            np.abs(
                cumulative_counts
                - train_target
            )
        )
    ) + 1

    remaining = (
        shuffled[
            train_cut:
        ]
    )

    if len(remaining) < 2:
        raise RuntimeError(
            "Not enough day groups remaining "
            "for validation/test."
        )

    validation_cumulative = (
        np.cumsum(
            [
                group["count"]
                for group in remaining
            ]
        )
    )

    validation_cut = int(
        np.argmin(
            np.abs(
                validation_cumulative
                - validation_target
            )
        )
    ) + 1

    validation_groups = (
        remaining[
            :validation_cut
        ]
    )

    test_groups = (
        remaining[
            validation_cut:
        ]
    )

    if (
        not validation_groups
        or not test_groups
    ):
        raise RuntimeError(
            "Empty validation or test split."
        )

    return {
        "train": shuffled[
            :train_cut
        ],
        "validation": validation_groups,
        "test": test_groups,
    }


def candidate_score(
    candidate: dict[str, list[dict]],
    total_samples: int,
    global_histogram: np.ndarray,
    global_mean: float,
) -> float:
    ratios = {
        "train": TRAIN_RATIO,
        "validation": VALIDATION_RATIO,
        "test": TEST_RATIO,
    }

    score = 0.0

    global_distribution = (
        global_histogram
        / global_histogram.sum()
    )

    for split_name, split_groups in (
        candidate.items()
    ):
        target_count = (
            total_samples
            * ratios[
                split_name
            ]
        )

        actual_count = sum(
            group["count"]
            for group in split_groups
        )

        count_error = (
            (
                actual_count
                - target_count
            )
            / target_count
        ) ** 2

        split_histogram = np.sum(
            [
                group[
                    "histogram"
                ]
                for group
                in split_groups
            ],
            axis=0,
        )

        split_distribution = (
            split_histogram
            / split_histogram.sum()
        )

        distribution_error = (
            np.mean(
                (
                    split_distribution
                    - global_distribution
                )
                ** 2
            )
        )

        weighted_visibility_sum = sum(
            group[
                "mean_visibility"
            ]
            * group[
                "count"
            ]
            for group in split_groups
        )

        split_mean = (
            weighted_visibility_sum
            / actual_count
        )

        mean_error = (
            (
                split_mean
                - global_mean
            )
            / global_mean
        ) ** 2

        score += (
            5.0
            * count_error
            + 10.0
            * distribution_error
            + 2.0
            * mean_error
        )

    return score


def search_best_split(
    groups: list[dict],
    dataset: pd.DataFrame,
) -> dict[str, list[dict]]:
    total_samples = len(
        dataset
    )

    global_histogram = (
        np.bincount(
            dataset[
                "visibility_bin"
            ].to_numpy(),
            minlength=dataset[
                "visibility_bin"
            ].nunique(),
        ).astype(float)
    )

    global_mean = (
        dataset[
            "visibility estimation average"
        ].mean()
    )

    rng = random.Random(
        RANDOM_SEED
    )

    best_candidate = None
    best_score = None

    for _ in range(
        N_SEARCH_ITERATIONS
    ):
        candidate = (
            partition_candidate(
                groups=groups,
                rng=rng,
                total_samples=total_samples,
            )
        )

        score = candidate_score(
            candidate=candidate,
            total_samples=total_samples,
            global_histogram=global_histogram,
            global_mean=global_mean,
        )

        if (
            best_score is None
            or score < best_score
        ):
            best_score = score
            best_candidate = candidate

    if best_candidate is None:
        raise RuntimeError(
            "No valid split candidate found."
        )

    print(
        "\nBest split objective score: "
        f"{best_score:.8f}"
    )

    return best_candidate


def create_output_frames(
    dataset: pd.DataFrame,
    candidate: dict[str, list[dict]],
) -> dict[str, pd.DataFrame]:
    output_frames = {}

    for (
        split_name,
        groups,
    ) in candidate.items():
        dates = {
            group["date"]
            for group in groups
        }

        frame = dataset[
            dataset[
                "date"
            ].isin(
                dates
            )
        ].copy()

        frame = frame.sort_values(
            "timestamp"
        )

        output_frames[
            split_name
        ] = frame

    return output_frames


def validate_split(
    output_frames: dict[str, pd.DataFrame],
    expected_total: int,
) -> None:
    train = output_frames[
        "train"
    ]

    validation = output_frames[
        "validation"
    ]

    test = output_frames[
        "test"
    ]

    total = (
        len(train)
        + len(validation)
        + len(test)
    )

    if total != expected_total:
        raise ValueError(
            f"Expected {expected_total} samples, "
            f"found {total}."
        )

    name_sets = {
        split: set(
            frame[
                "image_name"
            ]
        )
        for split, frame
        in output_frames.items()
    }

    date_sets = {
        split: set(
            frame[
                "date"
            ]
        )
        for split, frame
        in output_frames.items()
    }

    if (
        name_sets["train"]
        & name_sets[
            "validation"
        ]
    ):
        raise ValueError(
            "Train/validation image overlap."
        )

    if (
        name_sets["train"]
        & name_sets[
            "test"
        ]
    ):
        raise ValueError(
            "Train/test image overlap."
        )

    if (
        name_sets[
            "validation"
        ]
        & name_sets[
            "test"
        ]
    ):
        raise ValueError(
            "Validation/test image overlap."
        )

    if (
        date_sets["train"]
        & date_sets[
            "validation"
        ]
    ):
        raise ValueError(
            "Train/validation date overlap."
        )

    if (
        date_sets["train"]
        & date_sets[
            "test"
        ]
    ):
        raise ValueError(
            "Train/test date overlap."
        )

    if (
        date_sets[
            "validation"
        ]
        & date_sets[
            "test"
        ]
    ):
        raise ValueError(
            "Validation/test date overlap."
        )


def save_split_files(
    output_frames: dict[str, pd.DataFrame],
) -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    columns = [
        "image_name",
        "visibility estimation average",
        "date",
    ]

    for (
        split_name,
        frame,
    ) in output_frames.items():
        output_path = (
            OUTPUT_DIR
            / f"{split_name}.csv"
        )

        frame[
            columns
        ].to_csv(
            output_path,
            index=False,
        )


def print_summary(
    output_frames: dict[str, pd.DataFrame],
) -> None:
    target_column = (
        "visibility estimation average"
    )

    total = sum(
        len(frame)
        for frame
        in output_frames.values()
    )

    global_values = pd.concat(
        [
            frame[
                target_column
            ]
            for frame
            in output_frames.values()
        ],
        ignore_index=True,
    )

    print(
        "\n=== CIDET DAY-GROUPED TEMPORAL SPLIT ==="
    )

    print(
        "\nGLOBAL"
    )

    print(
        f"Samples: {total}"
    )

    print(
        f"Mean visibility: "
        f"{global_values.mean():.4f} m"
    )

    print(
        f"Median visibility: "
        f"{global_values.median():.4f} m"
    )

    for split_name in [
        "train",
        "validation",
        "test",
    ]:
        frame = (
            output_frames[
                split_name
            ]
        )

        values = frame[
            target_column
        ]

        percentage = (
            len(frame)
            / total
            * 100
        )

        print(
            f"\n--- "
            f"{split_name.upper()} "
            f"---"
        )

        print(
            f"Samples:      "
            f"{len(frame)} "
            f"({percentage:.2f}%)"
        )

        print(
            f"Unique dates: "
            f"{frame['date'].nunique()}"
        )

        print(
            f"Visibility min:    "
            f"{values.min():.4f} m"
        )

        print(
            f"Visibility mean:   "
            f"{values.mean():.4f} m"
        )

        print(
            f"Visibility median: "
            f"{values.median():.4f} m"
        )

        print(
            f"Visibility max:    "
            f"{values.max():.4f} m"
        )

    train_dates = set(
        output_frames[
            "train"
        ][
            "date"
        ]
    )

    validation_dates = set(
        output_frames[
            "validation"
        ][
            "date"
        ]
    )

    test_dates = set(
        output_frames[
            "test"
        ][
            "date"
        ]
    )

    print(
        "\n--- LEAKAGE CHECK ---"
    )

    print(
        "Train ∩ Validation dates: "
        f"{len(train_dates & validation_dates)}"
    )

    print(
        "Train ∩ Test dates:       "
        f"{len(train_dates & test_dates)}"
    )

    print(
        "Validation ∩ Test dates:  "
        f"{len(validation_dates & test_dates)}"
    )

    print(
        f"\nOutput directory: "
        f"{OUTPUT_DIR}"
    )

    print(
        "\n=== TEMPORAL SPLIT COMPLETE ==="
    )


def main() -> None:
    dataset = (
        build_valid_dataset()
    )

    if len(dataset) != 977:
        raise ValueError(
            "Expected 977 usable official "
            "CIDET samples, "
            f"found {len(dataset)}."
        )

    dataset = (
        add_visibility_bins(
            dataset
        )
    )

    groups = (
        build_day_groups(
            dataset
        )
    )

    print(
        "\nSearching for balanced "
        "day-grouped split..."
    )

    print(
        f"Samples: {len(dataset)}"
    )

    print(
        f"Unique dates: "
        f"{dataset['date'].nunique()}"
    )

    print(
        f"Search iterations: "
        f"{N_SEARCH_ITERATIONS}"
    )

    candidate = (
        search_best_split(
            groups=groups,
            dataset=dataset,
        )
    )

    output_frames = (
        create_output_frames(
            dataset=dataset,
            candidate=candidate,
        )
    )

    validate_split(
        output_frames,
        expected_total=len(
            dataset
        ),
    )

    save_split_files(
        output_frames
    )

    print_summary(
        output_frames
    )


if __name__ == "__main__":
    main()