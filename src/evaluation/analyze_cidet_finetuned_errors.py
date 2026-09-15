"""
analyze_cidet_finetuned_errors.py

Post-hoc error analysis for the final CIDET temporal test evaluation.

This script does not train, select, or modify the model.
It only analyzes the already-saved test predictions.
"""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREDICTIONS_CSV = (
    PROJECT_ROOT
    / "results"
    / "cidet"
    / "finetuned"
    / "vgg16_cidet_temporal_test_predictions.csv"
)


def summarize_group(
    name: str,
    frame: pd.DataFrame,
) -> None:
    if frame.empty:
        print(
            f"{name:<14} n=0"
        )
        return

    targets = frame[
        "target_visibility_m"
    ].to_numpy(
        dtype=float
    )

    predictions = frame[
        "predicted_visibility_m"
    ].to_numpy(
        dtype=float
    )

    errors = (
        predictions
        - targets
    )

    absolute_errors = np.abs(
        errors
    )

    mae = float(
        absolute_errors.mean()
    )

    rmse = float(
        np.sqrt(
            np.mean(
                errors ** 2
            )
        )
    )

    signed_error = float(
        errors.mean()
    )

    median_ae = float(
        np.median(
            absolute_errors
        )
    )

    print(
        f"{name:<14} "
        f"n={len(frame):3d} | "
        f"MAE={mae:8.2f} m | "
        f"RMSE={rmse:8.2f} m | "
        f"MedianAE={median_ae:8.2f} m | "
        f"Bias={signed_error:+8.2f} m"
    )


def main() -> None:
    if not PREDICTIONS_CSV.exists():
        raise FileNotFoundError(
            f"Predictions not found: {PREDICTIONS_CSV}"
        )

    data = pd.read_csv(
        PREDICTIONS_CSV
    )

    required_columns = {
        "image_name",
        "target_visibility_m",
        "predicted_visibility_m",
        "absolute_error_m",
    }

    missing = (
        required_columns
        - set(data.columns)
    )

    if missing:
        raise ValueError(
            "Missing prediction columns: "
            f"{sorted(missing)}"
        )

    if len(data) != 145:
        raise ValueError(
            "Expected 145 final temporal test predictions, "
            f"found {len(data)}."
        )

    bins = [
        0,
        500,
        1000,
        2000,
        3000,
        float("inf"),
    ]

    labels = [
        "<500 m",
        "500-999 m",
        "1000-1999 m",
        "2000-2999 m",
        ">=3000 m",
    ]

    data["visibility_group"] = pd.cut(
        data[
            "target_visibility_m"
        ],
        bins=bins,
        labels=labels,
        right=False,
    )

    print(
        "\n=== CIDET FINETUNED ERROR ANALYSIS ==="
    )

    print(
        "\n--- ERROR BY TRUE VISIBILITY RANGE ---"
    )

    for label in labels:
        group = data[
            data[
                "visibility_group"
            ]
            == label
        ]

        summarize_group(
            label,
            group,
        )

    print(
        "\n--- TEN LARGEST ABSOLUTE ERRORS ---"
    )

    worst = (
        data.sort_values(
            "absolute_error_m",
            ascending=False,
        )
        .head(10)
    )

    for _, row in worst.iterrows():
        error = (
            row[
                "predicted_visibility_m"
            ]
            - row[
                "target_visibility_m"
            ]
        )

        print(
            f"{row['image_name']} | "
            f"target={row['target_visibility_m']:.2f} m | "
            f"prediction={row['predicted_visibility_m']:.2f} m | "
            f"error={error:+.2f} m | "
            f"abs={row['absolute_error_m']:.2f} m"
        )

    print(
        "\n--- PREDICTION COVERAGE ---"
    )

    targets = data[
        "target_visibility_m"
    ]

    predictions = data[
        "predicted_visibility_m"
    ]

    below_target_min = int(
        (
            predictions
            < targets.min()
        ).sum()
    )

    above_target_max = int(
        (
            predictions
            > targets.max()
        ).sum()
    )

    print(
        f"Predictions below test target minimum: "
        f"{below_target_min}"
    )

    print(
        f"Predictions above test target maximum: "
        f"{above_target_max}"
    )

    print(
        "\n=== ERROR ANALYSIS COMPLETE ==="
    )


if __name__ == "__main__":
    main()