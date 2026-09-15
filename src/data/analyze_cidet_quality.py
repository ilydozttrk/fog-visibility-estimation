from bisect import bisect_left
from pathlib import Path
import re

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
CIDET_INTERIM = ROOT / "data" / "interim" / "cidet"


def find_required_file(filename: str) -> Path:
    matches = list(CIDET_INTERIM.rglob(filename))

    if not matches:
        raise FileNotFoundError(
            f"Could not find required CIDET file: {filename}"
        )

    if len(matches) > 1:
        locations = "\n".join(str(path) for path in matches)
        raise RuntimeError(
            f"Found multiple files named {filename}:\n{locations}"
        )

    return matches[0]


def load_split(path: Path, split_name: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=["image_name"])
    df["image_name"] = df["image_name"].astype(str).str.strip()
    df["split"] = split_name
    return df


def parse_image_timestamp(filename: str) -> pd.Timestamp:
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


def nearest_time_difference_seconds(
    timestamp: pd.Timestamp,
    candidates: list[pd.Timestamp],
) -> float | None:
    if pd.isna(timestamp) or not candidates:
        return None

    index = bisect_left(candidates, timestamp)

    possible = []

    if index < len(candidates):
        possible.append(
            abs((candidates[index] - timestamp).total_seconds())
        )

    if index > 0:
        possible.append(
            abs((candidates[index - 1] - timestamp).total_seconds())
        )

    if not possible:
        return None

    return min(possible)


def main() -> None:
    annotation_path = find_required_file(
        "tabular_data_and_visibility_annotation.csv"
    )
    train_path = find_required_file("images_train.csv")
    val_path = find_required_file("images_val.csv")
    test_path = find_required_file("images_test.csv")

    annotations = pd.read_csv(annotation_path)

    split_df = pd.concat(
        [
            load_split(train_path, "train"),
            load_split(val_path, "validation"),
            load_split(test_path, "test"),
        ],
        ignore_index=True,
    )

    df = split_df.merge(
        annotations,
        on="image_name",
        how="left",
        validate="one_to_one",
    )

    person1_column = "visibility estimation person 1"
    person2_column = "visibility estimation person 2"
    average_column = "visibility estimation average"

    df[person1_column] = pd.to_numeric(
        df[person1_column],
        errors="coerce",
    )
    df[person2_column] = pd.to_numeric(
        df[person2_column],
        errors="coerce",
    )
    df[average_column] = pd.to_numeric(
        df[average_column],
        errors="coerce",
    )

    df["observer_abs_diff_m"] = (
        df[person1_column] - df[person2_column]
    ).abs()

    df["timestamp"] = df["image_name"].apply(
        parse_image_timestamp
    )

    print("\n=== CIDET QUALITY ANALYSIS ===")

    print("\n--- OFFICIAL DATASET ---")
    print(f"Usable official samples: {len(df)}")
    print(
        "Missing merged annotations: "
        f"{df[average_column].isna().sum()}"
    )

    print("\n--- OBSERVER DISAGREEMENT ---")
    disagreement = df["observer_abs_diff_m"]

    print(f"Valid observer pairs: {disagreement.notna().sum()}")
    print(f"Mean absolute disagreement [m]:   {disagreement.mean():.4f}")
    print(f"Median absolute disagreement [m]: {disagreement.median():.4f}")
    print(
        "95th percentile disagreement [m]: "
        f"{disagreement.quantile(0.95):.4f}"
    )
    print(f"Maximum disagreement [m]:         {disagreement.max():.4f}")

    observer_corr = df[
        [person1_column, person2_column]
    ].corr().iloc[0, 1]

    print(
        f"Person 1 / Person 2 correlation:  "
        f"{observer_corr:.6f}"
    )

    print("\nLargest observer disagreements:")
    largest_disagreements = df.nlargest(
        10,
        "observer_abs_diff_m",
    )[
        [
            "image_name",
            person1_column,
            person2_column,
            average_column,
            "observer_abs_diff_m",
            "split",
        ]
    ]

    print(
        largest_disagreements.to_string(
            index=False
        )
    )

    print("\n--- TARGET DISTRIBUTION BY SPLIT ---")

    for split_name in ["train", "validation", "test"]:
        split_values = df.loc[
            df["split"] == split_name,
            average_column,
        ]

        print(f"\n{split_name.upper()}")
        print(f"n:      {len(split_values)}")
        print(f"min:    {split_values.min():.4f}")
        print(f"mean:   {split_values.mean():.4f}")
        print(f"median: {split_values.median():.4f}")
        print(f"max:    {split_values.max():.4f}")

    print("\n--- TIMESTAMP PARSING ---")
    valid_timestamps = df["timestamp"].notna().sum()

    print(f"Parsed timestamps: {valid_timestamps}/{len(df)}")

    if valid_timestamps != len(df):
        print("\nUnparsed filename examples:")
        print(
            df.loc[
                df["timestamp"].isna(),
                "image_name",
            ].head(10).to_string(index=False)
        )

    df["date"] = df["timestamp"].dt.date

    print("\n--- DATE OVERLAP BETWEEN SPLITS ---")

    split_dates = {}

    for split_name in ["train", "validation", "test"]:
        dates = set(
            df.loc[
                df["split"] == split_name,
                "date",
            ].dropna()
        )

        split_dates[split_name] = dates
        print(
            f"{split_name}: "
            f"{len(dates)} unique calendar dates"
        )

    print(
        "Train ∩ Validation dates: "
        f"{len(split_dates['train'] & split_dates['validation'])}"
    )
    print(
        "Train ∩ Test dates:       "
        f"{len(split_dates['train'] & split_dates['test'])}"
    )
    print(
        "Validation ∩ Test dates:  "
        f"{len(split_dates['validation'] & split_dates['test'])}"
    )

    print("\n--- CROSS-SPLIT TEMPORAL PROXIMITY ---")

    timestamps_by_split = {}

    for split_name in ["train", "validation", "test"]:
        timestamps_by_split[split_name] = sorted(
            df.loc[
                (df["split"] == split_name)
                & df["timestamp"].notna(),
                "timestamp",
            ].tolist()
        )

    thresholds_minutes = [1, 5, 10, 30, 60]

    nearest_other_split_seconds = []

    closest_pairs = []

    for _, row in df.iterrows():
        source_split = row["split"]
        timestamp = row["timestamp"]

        candidates = []

        for target_split in [
            "train",
            "validation",
            "test",
        ]:
            if target_split == source_split:
                continue

            diff_seconds = nearest_time_difference_seconds(
                timestamp,
                timestamps_by_split[target_split],
            )

            if diff_seconds is not None:
                candidates.append(
                    (diff_seconds, target_split)
                )

        if candidates:
            nearest_seconds, nearest_split = min(
                candidates,
                key=lambda item: item[0],
            )

            nearest_other_split_seconds.append(
                nearest_seconds
            )

            closest_pairs.append(
                {
                    "image_name": row["image_name"],
                    "source_split": source_split,
                    "nearest_other_split": nearest_split,
                    "difference_seconds": nearest_seconds,
                }
            )

    proximity_series = pd.Series(
        nearest_other_split_seconds,
        dtype=float,
    )

    for threshold in thresholds_minutes:
        count = (
            proximity_series
            <= threshold * 60
        ).sum()

        percentage = (
            count / len(proximity_series) * 100
            if len(proximity_series)
            else 0.0
        )

        print(
            f"Samples with another-split frame within "
            f"{threshold:>2} min: "
            f"{count:>4} "
            f"({percentage:6.2f}%)"
        )

    if len(proximity_series):
        print(
            "\nMedian nearest cross-split time gap [min]: "
            f"{proximity_series.median() / 60:.2f}"
        )
        print(
            "Minimum nearest cross-split time gap [min]: "
            f"{proximity_series.min() / 60:.2f}"
        )

    print("\nClosest cross-split examples:")

    closest_df = pd.DataFrame(
        closest_pairs
    ).sort_values(
        "difference_seconds"
    ).head(15)

    if not closest_df.empty:
        closest_df["difference_minutes"] = (
            closest_df["difference_seconds"] / 60
        )

        print(
            closest_df[
                [
                    "image_name",
                    "source_split",
                    "nearest_other_split",
                    "difference_minutes",
                ]
            ].to_string(index=False)
        )

    print("\n=== QUALITY ANALYSIS COMPLETE ===")


if __name__ == "__main__":
    main()