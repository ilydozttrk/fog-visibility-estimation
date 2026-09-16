"""
evaluate_vgg16_benchmark_external.py

Independent external evaluation of the CIDET-selected VGG16
Block 5 + Huber model on the Benchmark-Visibility dataset.

Protocol:
- checkpoint was selected using CIDET validation only
- Benchmark-Visibility is used for external evaluation only
- no fine-tuning, calibration, model selection, or hyperparameter
  tuning is performed on Benchmark-Visibility
- preprocessing is identical to the CIDET/synthetic experiments
- Benchmark ground truth is expressed in metres
- the source dataset contains a 20,000 m visibility ceiling

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset

from src.training.cidet_dataloader import get_cidet_transforms
from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    IMAGE_SIZE,
    NUM_WORKERS,
)
from src.training.train_vgg16 import build_vgg16_regression_model


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "benchmark_visibility"
    / "manifest.csv"
)

CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_cidet_block5_huber_best.pth"
)

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "benchmark_visibility"
    / "external"
)

PREDICTIONS_CSV = (
    RESULTS_DIR
    / "vgg16_cidet_block5_huber_predictions.csv"
)

EXPECTED_SAMPLES = 1856
VISIBILITY_CEILING_M = 20000.0


class BenchmarkVisibilityDataset(Dataset):
    """
    Benchmark-Visibility external evaluation dataset.
    """

    def __init__(
        self,
        manifest_path: Path,
        transform: Optional[object] = None,
    ) -> None:
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Benchmark manifest not found: {manifest_path}"
            )

        self.data = pd.read_csv(manifest_path)

        required_columns = {
            "image_path",
            "visibility_m",
            "date",
            "timestamp",
            "day",
            "frame_index",
        }

        missing_columns = (
            required_columns
            - set(self.data.columns)
        )

        if missing_columns:
            raise ValueError(
                "Missing Benchmark manifest columns: "
                f"{sorted(missing_columns)}"
            )

        if len(self.data) != EXPECTED_SAMPLES:
            raise ValueError(
                f"Expected {EXPECTED_SAMPLES} Benchmark samples, "
                f"found {len(self.data)}."
            )

        self.transform = transform

        self.image_paths = []

        for raw_path in self.data["image_path"].astype(str):
            image_path = Path(raw_path)

            if not image_path.is_absolute():
                image_path = PROJECT_ROOT / image_path

            if not image_path.is_file():
                raise FileNotFoundError(
                    f"Benchmark image not found: {image_path}"
                )

            self.image_paths.append(image_path)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(
        self,
        index: int,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        image_path = self.image_paths[index]

        with Image.open(image_path) as image_file:
            image = image_file.convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        target = torch.tensor(
            float(
                self.data.iloc[index][
                    "visibility_m"
                ]
            ),
            dtype=torch.float32,
        )

        return image, target


def assign_visibility_bin(target: float) -> str:
    """
    Assign broad visibility ranges suitable for the much wider
    Benchmark-Visibility target domain.
    """
    if target < 1000.0:
        return "<1000"

    if target < 3000.0:
        return "1000-2999"

    if target < 5000.0:
        return "3000-4999"

    if target < 10000.0:
        return "5000-9999"

    if target < VISIBILITY_CEILING_M:
        return "10000-19999"

    return "20000"


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

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            "Checkpoint does not contain model_state_dict."
        )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(DEVICE)
    model.eval()

    print("=== CHECKPOINT ===")
    print(f"Path: {CHECKPOINT_PATH}")
    print(
        "Epoch: "
        f"{checkpoint.get('epoch')}"
    )
    print(
        "CIDET validation MAE: "
        f"{checkpoint.get('validation_mae'):.4f} m"
    )
    print(
        "Benchmark used for checkpoint selection: False"
    )

    return model


def main() -> None:
    transform = get_cidet_transforms(
        image_size=IMAGE_SIZE
    )

    dataset = BenchmarkVisibilityDataset(
        manifest_path=MANIFEST_PATH,
        transform=transform,
    )

    loader = DataLoader(
        dataset=dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE.type == "cuda"),
    )

    if len(dataset) != EXPECTED_SAMPLES:
        raise ValueError(
            f"Expected {EXPECTED_SAMPLES} samples, "
            f"found {len(dataset)}."
        )

    model = load_model()

    targets = []
    predictions = []

    with torch.no_grad():
        for images, batch_targets in loader:
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

    if len(targets) != EXPECTED_SAMPLES:
        raise RuntimeError(
            "Unexpected number of evaluated samples: "
            f"{len(targets)}"
        )

    if not np.all(np.isfinite(predictions)):
        raise RuntimeError(
            "Non-finite model predictions detected."
        )

    errors = predictions - targets
    absolute_errors = np.abs(errors)

    mae = float(
        np.mean(absolute_errors)
    )

    rmse = float(
        np.sqrt(
            np.mean(errors ** 2)
        )
    )

    median_ae = float(
        np.median(absolute_errors)
    )

    signed_error = float(
        np.mean(errors)
    )

    max_ae = float(
        np.max(absolute_errors)
    )

    correlation = float(
        np.corrcoef(
            targets,
            predictions,
        )[0, 1]
    )

    metadata = (
        dataset.data
        .reset_index(drop=True)
        .copy()
    )

    output = pd.DataFrame(
        {
            "image_path": metadata["image_path"],
            "date": metadata["date"],
            "timestamp": metadata["timestamp"],
            "day": metadata["day"],
            "frame_index": metadata["frame_index"],
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

    output["at_20000m_ceiling"] = np.isclose(
        targets,
        VISIBILITY_CEILING_M,
    )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.to_csv(
        PREDICTIONS_CSV,
        index=False,
    )

    print(
        "\n=== BENCHMARK-VISIBILITY EXTERNAL EVALUATION ==="
    )

    print(f"Device:                 {DEVICE}")
    print(f"Samples:                {len(targets)}")
    print(f"MAE:                    {mae:.4f} m")
    print(f"RMSE:                   {rmse:.4f} m")
    print(
        f"Median absolute error:  "
        f"{median_ae:.4f} m"
    )
    print(
        f"Mean signed error:      "
        f"{signed_error:+.4f} m"
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
        "\n--- TARGET / PREDICTION RANGE ---"
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
        "\n--- ERROR BY VISIBILITY RANGE ---"
    )

    ordered_bins = [
        "<1000",
        "1000-2999",
        "3000-4999",
        "5000-9999",
        "10000-19999",
        "20000",
    ]

    for bin_name in ordered_bins:
        group = output[
            output["visibility_bin"]
            == bin_name
        ]

        if group.empty:
            print(
                f"{bin_name:12s} | n=0"
            )
            continue

        group_errors = group[
            "signed_error_m"
        ].to_numpy()

        group_absolute_errors = group[
            "absolute_error_m"
        ].to_numpy()

        print(
            f"{bin_name:12s} "
            f"| n={len(group):4d} "
            f"| MAE={np.mean(group_absolute_errors):9.2f} m "
            f"| MedianAE={np.median(group_absolute_errors):9.2f} m "
            f"| Bias={np.mean(group_errors):+9.2f} m"
        )

    ceiling_group = output[
        output["at_20000m_ceiling"]
    ]

    non_ceiling_group = output[
        ~output["at_20000m_ceiling"]
    ]

    print(
        "\n--- 20,000 m SENSOR CEILING ANALYSIS ---"
    )

    print(
        f"Ceiling samples: "
        f"{len(ceiling_group)}"
    )

    if not ceiling_group.empty:
        print(
            "Ceiling MAE:     "
            f"{ceiling_group['absolute_error_m'].mean():.4f} m"
        )

        print(
            "Ceiling bias:    "
            f"{ceiling_group['signed_error_m'].mean():+.4f} m"
        )

    print(
        f"Non-ceiling samples: "
        f"{len(non_ceiling_group)}"
    )

    if not non_ceiling_group.empty:
        print(
            "Non-ceiling MAE: "
            f"{non_ceiling_group['absolute_error_m'].mean():.4f} m"
        )

        print(
            "Non-ceiling bias:"
            f" {non_ceiling_group['signed_error_m'].mean():+.4f} m"
        )

    print(
        "\n--- TEN LARGEST ABSOLUTE ERRORS ---"
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
            f"{row['timestamp']} "
            f"| target={row['target_visibility_m']:.2f} "
            f"| prediction={row['predicted_visibility_m']:.2f} "
            f"| error={row['signed_error_m']:+.2f} "
            f"| abs={row['absolute_error_m']:.2f}"
        )

    print(
        "\nPredictions saved to:"
    )
    print(PREDICTIONS_CSV)

    print(
        "\nIMPORTANT:"
    )
    print(
        "Benchmark-Visibility was used for external evaluation only."
    )
    print(
        "No Benchmark samples were used for model training, "
        "fine-tuning, calibration, or checkpoint selection."
    )

    print(
        "\n=== EXTERNAL EVALUATION COMPLETE ==="
    )


if __name__ == "__main__":
    main()
