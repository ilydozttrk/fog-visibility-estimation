"""
split_fvei.py

Create the reproducible FVEI train/validation/test split used in the project.

Policy:
- Exact-label samples (levels 0-3) are stratified by visibility level.
- Random seed = 42.
- Split ratio = 70% train / 15% validation / 15% test.
- Two validation samples identified during pre-training similarity screening
  are excluded to reduce cross-split near-duplicate leakage.
- Level-4 / 500 m ceiling samples are kept separately for ceiling analysis.
- The held-out test split must not be used for model selection.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_MANIFEST = (
    ROOT / "data" / "processed" / "fvei" / "manifest.csv"
)

DEFAULT_OUTPUT = (
    ROOT
    / "data"
    / "processed"
    / "fvei"
    / "fvei_final_split_manifest.csv"
)

RANDOM_SEED = 42
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SIMILARITY_EXCLUSIONS = {
    "fog open data/0/0-381-47.jpg",
    "fog open data/1/1-00073-62.jpg",
}


def create_split(
    manifest_path: Path,
    output_path: Path,
    random_seed: int = RANDOM_SEED,
) -> dict:
    with manifest_path.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError("FVEI manifest is empty.")

    required_columns = {
        "zip_member",
        "level",
        "visibility_m",
        "label_kind",
        "sha256",
    }

    missing_columns = required_columns.difference(
        rows[0].keys()
    )

    if missing_columns:
        raise ValueError(
            "Missing manifest columns: "
            f"{sorted(missing_columns)}"
        )

    exact_groups = defaultdict(list)
    ceiling_rows = []

    for row in rows:
        if row["label_kind"] == "exact":
            exact_groups[int(row["level"])].append(row)
        elif row["label_kind"] == "ceiling":
            ceiling_rows.append(row)
        else:
            raise ValueError(
                "Unexpected label_kind: "
                f"{row['label_kind']}"
            )

    rng = random.Random(random_seed)
    output_rows = []

    for level in sorted(exact_groups):
        level_rows = list(exact_groups[level])
        rng.shuffle(level_rows)

        n = len(level_rows)

        n_val = round(n * VAL_RATIO)
        n_test = round(n * TEST_RATIO)
        n_train = n - n_val - n_test

        train_end = n_train
        val_end = train_end + n_val

        assignments = (
            [(row, "train") for row in level_rows[:train_end]]
            + [
                (row, "val")
                for row in level_rows[train_end:val_end]
            ]
            + [
                (row, "test")
                for row in level_rows[val_end:]
            ]
        )

        for row, split in assignments:
            output_row = dict(row)
            output_row["split"] = split
            output_rows.append(output_row)

    # Similarity screening was performed before model fitting.
    # Keep the test set unchanged and exclude the validation-side
    # samples involved in the two strict cross-split similarity matches.
    found_exclusions = set()

    for row in output_rows:
        name = row["zip_member"]

        if name in SIMILARITY_EXCLUSIONS:
            found_exclusions.add(name)

            if row["split"] != "val":
                raise RuntimeError(
                    "Similarity exclusion was expected in "
                    f"validation but found in {row['split']}: "
                    f"{name}"
                )

            row["split"] = "excluded_similarity"

    missing_exclusions = (
        SIMILARITY_EXCLUSIONS - found_exclusions
    )

    if missing_exclusions:
        raise RuntimeError(
            "Similarity exclusion samples were not found: "
            f"{sorted(missing_exclusions)}"
        )

    for row in ceiling_rows:
        output_row = dict(row)
        output_row["split"] = "ceiling_eval"
        output_rows.append(output_row)

    # Preserve deterministic manifest ordering.
    output_rows.sort(
        key=lambda row: row["zip_member"]
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(rows[0].keys()) + ["split"]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(output_rows)

    split_counts = Counter(
        row["split"]
        for row in output_rows
    )

    level_distribution = {}

    for split in ("train", "val", "test"):
        counts = Counter(
            int(row["level"])
            for row in output_rows
            if row["split"] == split
        )

        level_distribution[split] = {
            str(level): counts[level]
            for level in sorted(counts)
        }

    summary = {
        "random_seed": random_seed,
        "strategy": (
            "level-stratified deterministic split"
        ),
        "train_ratio_target": 0.70,
        "validation_ratio_target": 0.15,
        "test_ratio_target": 0.15,
        "split_counts": dict(split_counts),
        "level_distribution": level_distribution,
        "similarity_exclusions": sorted(
            SIMILARITY_EXCLUSIONS
        ),
        "test_used_for_model_selection": False,
    }

    summary_path = output_path.with_suffix(".json")

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=RANDOM_SEED,
    )

    args = parser.parse_args()

    summary = create_split(
        manifest_path=args.manifest,
        output_path=args.output,
        random_seed=args.seed,
    )

    print(
        json.dumps(
            summary,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
