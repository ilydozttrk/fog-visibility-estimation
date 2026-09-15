"""
evaluate_vgg16_cidet_finetuned.py

Evaluate the CIDET-finetuned VGG16 model on the held-out
CIDET temporal test split.

This script must be run only after model selection is complete.
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
    / "vgg16_cidet_finetuned_best.pth"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "cidet"
    / "finetuned"
)

PREDICTIONS_CSV = (
    RESULTS_DIR
    / "vgg16_cidet_temporal_test_predictions.csv"
)


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
        f"Loaded checkpoint from epoch: "
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
        _,
        test_loader,
    ) = create_cidet_dataloaders(
        pin_memory=(
            DEVICE.type == "cuda"
        )
    )

    if len(test_loader.dataset) != 145:
        raise ValueError(
            "Expected 145 temporal test samples, "
            f"found {len(test_loader.dataset)}."
        )

    model = load_model()

    targets = []
    predictions = []

    with torch.no_grad():
        for images, batch_targets in test_loader:
            images = images.to(DEVICE)

            batch_predictions = (
                model(images)
                .squeeze(1)
                .cpu()
                .numpy()
            )

            predictions.extend(
                batch_predictions
            )

            targets.extend(
                batch_targets.numpy()
            )

    targets = np.asarray(
        targets,
        dtype=np.float64,
    )

    predictions = np.asarray(
        predictions,
        dtype=np.float64,
    )

    errors = predictions - targets

    absolute_errors = np.abs(
        errors
    )

    mae = float(
        np.mean(
            absolute_errors
        )
    )

    rmse = float(
        np.sqrt(
            np.mean(
                errors ** 2
            )
        )
    )

    median_ae = float(
        np.median(
            absolute_errors
        )
    )

    signed_error = float(
        np.mean(
            errors
        )
    )

    max_ae = float(
        np.max(
            absolute_errors
        )
    )

    correlation = float(
        np.corrcoef(
            targets,
            predictions,
        )[0, 1]
    )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    split_dataframe = (
        test_loader.dataset.data
        .reset_index(drop=True)
    )

    output = pd.DataFrame(
        {
            "image_name": split_dataframe[
                "image_name"
            ],
            "target_visibility_m": targets,
            "predicted_visibility_m": predictions,
            "signed_error_m": errors,
            "absolute_error_m": absolute_errors,
        }
    )

    output.to_csv(
        PREDICTIONS_CSV,
        index=False,
    )

    print(
        "\n=== CIDET FINETUNED TEST EVALUATION ==="
    )

    print(
        f"Test samples:           "
        f"{len(targets)}"
    )

    print(
        f"MAE:                    "
        f"{mae:.4f} m"
    )

    print(
        f"RMSE:                   "
        f"{rmse:.4f} m"
    )

    print(
        f"Median absolute error:  "
        f"{median_ae:.4f} m"
    )

    print(
        f"Mean signed error:      "
        f"{signed_error:.4f} m"
    )

    print(
        f"Maximum absolute error: "
        f"{max_ae:.4f} m"
    )

    print(
        f"Pearson correlation:    "
        f"{correlation:.6f}"
    )

    print(
        "\n--- TARGET RANGE ---"
    )

    print(
        f"Minimum: "
        f"{targets.min():.4f} m"
    )

    print(
        f"Maximum: "
        f"{targets.max():.4f} m"
    )

    print(
        "\n--- PREDICTION RANGE ---"
    )

    print(
        f"Minimum: "
        f"{predictions.min():.4f} m"
    )

    print(
        f"Maximum: "
        f"{predictions.max():.4f} m"
    )

    print(
        "\nPredictions saved to:"
    )

    print(
        PREDICTIONS_CSV
    )

    print(
        "\n=== TEST EVALUATION COMPLETE ==="
    )


if __name__ == "__main__":
    main()