"""
evaluate_vgg16_cidet_zero_shot.py

Zero-shot evaluation of the synthetic-trained VGG16 visibility
regression baseline on the CIDET real-world temporal test split.

No CIDET samples are used for training or adaptation in this script.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset

from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    IMAGE_SIZE,
    NUM_WORKERS,
    VGG16_CHECKPOINT_PATH,
)
from src.training.dataloader import get_transforms
from src.training.train_vgg16 import build_vgg16_regression_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CIDET_INTERIM = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "cidet"
)

CIDET_TEMPORAL_SPLIT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cidet"
    / "temporal_split"
)

TEST_CSV = (
    CIDET_TEMPORAL_SPLIT
    / "test.csv"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "cidet"
    / "zero_shot"
)

PREDICTIONS_CSV = (
    RESULTS_DIR
    / "vgg16_cidet_temporal_test_predictions.csv"
)


def find_cidet_image(filename: str) -> Path:
    """
    Find exactly one CIDET image recursively.
    """
    matches = list(
        CIDET_INTERIM.rglob(filename)
    )

    if not matches:
        raise FileNotFoundError(
            f"CIDET image not found: {filename}"
        )

    if len(matches) > 1:
        locations = "\n".join(
            str(path)
            for path in matches
        )

        raise RuntimeError(
            f"Multiple CIDET images found for {filename}:\n"
            f"{locations}"
        )

    return matches[0]


class CIDETTestDataset(Dataset):
    """
    CIDET temporal test split for zero-shot evaluation.
    """

    def __init__(
        self,
        csv_path: Path,
    ) -> None:
        self.data = pd.read_csv(
            csv_path
        )

        required_columns = {
            "image_name",
            "visibility estimation average",
            "date",
        }

        missing_columns = (
            required_columns
            - set(self.data.columns)
        )

        if missing_columns:
            raise ValueError(
                "Missing required CIDET columns: "
                f"{sorted(missing_columns)}"
            )

        self.transform = get_transforms(
            image_size=IMAGE_SIZE
        )

    def __len__(self) -> int:
        return len(
            self.data
        )

    def __getitem__(
        self,
        index: int,
    ) -> tuple[
        torch.Tensor,
        torch.Tensor,
        str,
    ]:
        row = self.data.iloc[
            index
        ]

        filename = str(
            row["image_name"]
        )

        image_path = find_cidet_image(
            filename
        )

        with Image.open(
            image_path
        ) as image_file:
            image = (
                image_file
                .convert("RGB")
            )

        image = self.transform(
            image
        )

        target = torch.tensor(
            float(
                row[
                    "visibility estimation average"
                ]
            ),
            dtype=torch.float32,
        )

        return (
            image,
            target,
            filename,
        )


def load_model() -> torch.nn.Module:
    """
    Load the synthetic-trained VGG16 baseline checkpoint.
    """
    if not VGG16_CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            "VGG16 checkpoint not found: "
            f"{VGG16_CHECKPOINT_PATH}"
        )

    model = (
        build_vgg16_regression_model()
    )

    checkpoint = torch.load(
        VGG16_CHECKPOINT_PATH,
        map_location=DEVICE,
    )

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            "Checkpoint does not contain "
            "'model_state_dict'."
        )

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    model = model.to(
        DEVICE
    )

    model.eval()

    return model


def evaluate() -> None:
    """
    Evaluate the synthetic-trained VGG16 model on CIDET temporal test data.
    """
    if not TEST_CSV.exists():
        raise FileNotFoundError(
            "CIDET temporal test split not found: "
            f"{TEST_CSV}"
        )

    dataset = CIDETTestDataset(
        TEST_CSV
    )

    if len(dataset) != 145:
        raise ValueError(
            "Expected 145 CIDET temporal test samples, "
            f"found {len(dataset)}."
        )

    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(
            DEVICE.type == "cuda"
        ),
    )

    model = load_model()

    targets = []
    predictions = []
    filenames = []

    print(
        "\n=== CIDET ZERO-SHOT EVALUATION ==="
    )

    print(
        f"Device:        {DEVICE}"
    )

    print(
        f"Test samples:  {len(dataset)}"
    )

    print(
        f"Checkpoint:    {VGG16_CHECKPOINT_PATH}"
    )

    with torch.no_grad():
        for (
            images,
            batch_targets,
            batch_filenames,
        ) in dataloader:
            images = images.to(
                DEVICE
            )

            batch_predictions = (
                model(images)
                .squeeze(1)
                .cpu()
                .numpy()
            )

            targets.extend(
                batch_targets.numpy()
            )

            predictions.extend(
                batch_predictions
            )

            filenames.extend(
                batch_filenames
            )

    targets_array = np.asarray(
        targets,
        dtype=np.float64,
    )

    predictions_array = np.asarray(
        predictions,
        dtype=np.float64,
    )

    errors = (
        predictions_array
        - targets_array
    )

    absolute_errors = (
        np.abs(errors)
    )

    squared_errors = (
        errors ** 2
    )

    mae = float(
        np.mean(
            absolute_errors
        )
    )

    rmse = float(
        np.sqrt(
            np.mean(
                squared_errors
            )
        )
    )

    signed_error = float(
        np.mean(
            errors
        )
    )

    median_absolute_error = float(
        np.median(
            absolute_errors
        )
    )

    max_absolute_error = float(
        np.max(
            absolute_errors
        )
    )

    prediction_min = float(
        np.min(
            predictions_array
        )
    )

    prediction_max = float(
        np.max(
            predictions_array
        )
    )

    target_min = float(
        np.min(
            targets_array
        )
    )

    target_max = float(
        np.max(
            targets_array
        )
    )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = pd.DataFrame(
        {
            "image_name": filenames,
            "target_visibility_m": (
                targets_array
            ),
            "predicted_visibility_m": (
                predictions_array
            ),
            "signed_error_m": (
                errors
            ),
            "absolute_error_m": (
                absolute_errors
            ),
        }
    )

    output.to_csv(
        PREDICTIONS_CSV,
        index=False,
    )

    print(
        "\n--- RESULTS ---"
    )

    print(
        f"MAE:                   "
        f"{mae:.4f} m"
    )

    print(
        f"RMSE:                  "
        f"{rmse:.4f} m"
    )

    print(
        f"Median absolute error: "
        f"{median_absolute_error:.4f} m"
    )

    print(
        f"Mean signed error:     "
        f"{signed_error:.4f} m"
    )

    print(
        f"Maximum absolute error:"
        f" {max_absolute_error:.4f} m"
    )

    print(
        "\n--- TARGET RANGE ---"
    )

    print(
        f"Minimum: "
        f"{target_min:.4f} m"
    )

    print(
        f"Maximum: "
        f"{target_max:.4f} m"
    )

    print(
        "\n--- PREDICTION RANGE ---"
    )

    print(
        f"Minimum: "
        f"{prediction_min:.4f} m"
    )

    print(
        f"Maximum: "
        f"{prediction_max:.4f} m"
    )

    print(
        "\nPredictions saved to:"
    )

    print(
        PREDICTIONS_CSV
    )

    print(
        "\n=== ZERO-SHOT EVALUATION COMPLETE ==="
    )


def main() -> None:
    evaluate()


if __name__ == "__main__":
    main()