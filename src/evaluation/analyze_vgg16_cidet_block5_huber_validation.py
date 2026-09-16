"""
analyze_vgg16_cidet_block5_huber_validation.py

Post-hoc validation error analysis for the CIDET VGG16 Block 5
fine-tuning experiment.

IMPORTANT:
- uses the validation split only
- does not evaluate the CIDET test split
- intended to guide validation-driven model development

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path

import numpy as np
import pandas as pd
import torch

from src.training.cidet_dataloader import create_cidet_dataloaders
from src.training.config import DEVICE
from src.training.train_vgg16 import build_vgg16_regression_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_cidet_block5_huber_best.pth"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "cidet"
    / "block5_huber"
    / "validation"
)

PREDICTIONS_CSV = (
    RESULTS_DIR
    / "vgg16_cidet_block5_huber_validation_predictions.csv"
)


def assign_visibility_bin(target: float) -> str:
    if target < 500.0:
        return "<500"

    if target < 1000.0:
        return "500-999"

    if target < 2000.0:
        return "1000-1999"

    if target < 3000.0:
        return "2000-2999"

    return ">=3000"


def load_model() -> torch.nn.Module:
    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {CHECKPOINT_PATH}"
        )

    model = build_vgg16_regression_model()

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location=DEVICE,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(DEVICE)
    model.eval()

    print(
        f"Loaded checkpoint epoch: "
        f"{checkpoint.get('epoch')}"
    )

    print(
        f"Checkpoint validation MAE: "
        f"{checkpoint.get('validation_mae'):.4f} m"
    )

    return model


def main() -> None:
    (
        _,
        validation_loader,
        _,
    ) = create_cidet_dataloaders(
        pin_memory=(DEVICE.type == "cuda")
    )

    if len(validation_loader.dataset) != 147:
        raise ValueError(
            "Expected 147 validation samples, "
            f"found {len(validation_loader.dataset)}."
        )

    model = load_model()

    targets = []
    predictions = []

    with torch.no_grad():
        for images, batch_targets in validation_loader:
            images = images.to(DEVICE)

            batch_predictions = (
                model(images)
                .squeeze(1)
                .cpu()
                .numpy()
            )

            predictions.extend(batch_predictions)
            targets.extend(batch_targets.numpy())

    targets = np.asarray(
        targets,
        dtype=np.float64,
    )

    predictions = np.asarray(
        predictions,
        dtype=np.float64,
    )

    errors = predictions - targets
    absolute_errors = np.abs(errors)

    mae = float(np.mean(absolute_errors))

    rmse = float(
        np.sqrt(np.mean(errors ** 2))
    )

    median_ae = float(
        np.median(absolute_errors)
    )

    signed_error = float(
        np.mean(errors)
    )

    correlation = float(
        np.corrcoef(
            targets,
            predictions,
        )[0, 1]
    )

    split_dataframe = (
        validation_loader.dataset.data
        .reset_index(drop=True)
    )

    output = pd.DataFrame(
        {
            "image_name": split_dataframe[
                "image_name"
            ],
            "date": split_dataframe[
                "date"
            ],
            "target_visibility_m": targets,
            "predicted_visibility_m": predictions,
            "signed_error_m": errors,
            "absolute_error_m": absolute_errors,
        }
    )

    output["visibility_bin"] = [
        assign_visibility_bin(target)
        for target in targets
    ]

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.to_csv(
        PREDICTIONS_CSV,
        index=False,
    )

    print(
        "\n=== CIDET BLOCK 5 + HUBER VALIDATION ANALYSIS ==="
    )

    print(f"Samples:               {len(targets)}")
    print(f"MAE:                   {mae:.4f} m")
    print(f"RMSE:                  {rmse:.4f} m")
    print(
        f"Median absolute error: "
        f"{median_ae:.4f} m"
    )
    print(
        f"Mean signed error:     "
        f"{signed_error:.4f} m"
    )
    print(
        f"Pearson correlation:   "
        f"{correlation:.6f}"
    )

    print(
        "\n--- ERROR BY VISIBILITY RANGE ---"
    )

    ordered_bins = [
        "<500",
        "500-999",
        "1000-1999",
        "2000-2999",
        ">=3000",
    ]

    for bin_name in ordered_bins:
        group = output[
            output["visibility_bin"]
            == bin_name
        ]

        if group.empty:
            print(
                f"{bin_name:10s} "
                "| n=0"
            )
            continue

        group_errors = group[
            "signed_error_m"
        ].to_numpy()

        group_absolute_errors = group[
            "absolute_error_m"
        ].to_numpy()

        print(
            f"{bin_name:10s} "
            f"| n={len(group):3d} "
            f"| MAE={np.mean(group_absolute_errors):8.2f} m "
            f"| MedianAE={np.median(group_absolute_errors):8.2f} m "
            f"| Bias={np.mean(group_errors):+8.2f} m"
        )

    print(
        "\n--- TEN LARGEST VALIDATION ERRORS ---"
    )

    largest_errors = (
        output
        .sort_values(
            "absolute_error_m",
            ascending=False,
        )
        .head(10)
    )

    for _, row in largest_errors.iterrows():
        print(
            f"{row['image_name']} "
            f"| date={row['date']} "
            f"| target={row['target_visibility_m']:.2f} "
            f"| prediction={row['predicted_visibility_m']:.2f} "
            f"| error={row['signed_error_m']:+.2f} "
            f"| abs={row['absolute_error_m']:.2f}"
        )

    print(
        "\n--- PREDICTION RANGE ---"
    )

    print(
        f"Target:     "
        f"{targets.min():.4f} - "
        f"{targets.max():.4f} m"
    )

    print(
        f"Prediction: "
        f"{predictions.min():.4f} - "
        f"{predictions.max():.4f} m"
    )

    print(
        "\nPredictions saved to:"
    )

    print(PREDICTIONS_CSV)

    print(
        "\nCIDET test split was not evaluated."
    )


if __name__ == "__main__":
    main()



