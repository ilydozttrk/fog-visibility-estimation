"""
evaluate_vgg16_fvei_final.py

Final held-out evaluation for the validation-selected FVEI VGG16 model.

Protocol:
- load vgg16_fvei_block5_best.pth
- evaluate the locked FVEI exact-label test split once
- report MAE, RMSE, R2, bias, and level-wise errors
- analyse 500 m ceiling-labelled samples separately
- never treat ceiling-labelled samples as exact regression targets

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import argparse
import csv
import json
import math
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    IMAGE_SIZE,
    NUM_WORKERS,
)
from src.training.dataloader import get_transforms
from src.training.fvei_dataloader import (
    DEFAULT_MANIFEST,
    FVEIDataset,
)
from src.training.train_vgg16 import (
    build_vgg16_regression_model,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_CHECKPOINT = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_fvei_block5_best.pth"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "fvei"
)

DEFAULT_TEST_PREDICTIONS = (
    OUTPUT_DIR
    / "vgg16_fvei_final_test_predictions.csv"
)

DEFAULT_CEILING_PREDICTIONS = (
    OUTPUT_DIR
    / "vgg16_fvei_ceiling_predictions.csv"
)

DEFAULT_SUMMARY = (
    OUTPUT_DIR
    / "vgg16_fvei_final_evaluation.json"
)


def load_model(
    checkpoint_path: Path,
) -> tuple[torch.nn.Module, dict]:
    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {checkpoint_path}"
        )

    checkpoint = torch.load(
        checkpoint_path,
        map_location="cpu",
    )

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            "Checkpoint does not contain model_state_dict."
        )

    model = build_vgg16_regression_model(
        pretrained=False,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(DEVICE)
    model.eval()

    return model, checkpoint


def build_loader(
    zip_path: Path,
    manifest_path: Path,
    split: str,
    batch_size: int,
) -> tuple[FVEIDataset, DataLoader]:
    dataset = FVEIDataset(
        zip_path=zip_path,
        manifest_path=manifest_path,
        split=split,
        transform=get_transforms(
            image_size=IMAGE_SIZE,
        ),
    )

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(
            DEVICE.type == "cuda"
        ),
    )

    return dataset, loader


def predict(
    model: torch.nn.Module,
    loader: DataLoader,
) -> tuple[list[float], list[float]]:
    targets = []
    predictions = []

    with torch.inference_mode():
        for images, batch_targets in loader:
            images = images.to(
                DEVICE,
                non_blocking=True,
            )

            batch_predictions = (
                model(images)
                .squeeze(1)
                .detach()
                .cpu()
            )

            predictions.extend(
                batch_predictions.tolist()
            )

            targets.extend(
                batch_targets.tolist()
            )

    return targets, predictions


def regression_metrics(
    targets: list[float],
    predictions: list[float],
) -> dict:
    if len(targets) != len(predictions):
        raise ValueError(
            "Target and prediction lengths differ."
        )

    if not targets:
        raise ValueError(
            "No samples available for evaluation."
        )

    errors = [
        prediction - target
        for target, prediction
        in zip(targets, predictions)
    ]

    absolute_errors = [
        abs(error)
        for error in errors
    ]

    squared_errors = [
        error ** 2
        for error in errors
    ]

    mae = sum(
        absolute_errors
    ) / len(absolute_errors)

    rmse = math.sqrt(
        sum(squared_errors)
        / len(squared_errors)
    )

    bias = sum(errors) / len(errors)

    target_mean = (
        sum(targets)
        / len(targets)
    )

    ss_res = sum(squared_errors)

    ss_tot = sum(
        (target - target_mean) ** 2
        for target in targets
    )

    r2 = (
        1.0 - (ss_res / ss_tot)
        if ss_tot > 0
        else float("nan")
    )

    return {
        "n": len(targets),
        "mae_m": mae,
        "rmse_m": rmse,
        "r2": r2,
        "bias_m": bias,
    }


def save_exact_predictions(
    dataset: FVEIDataset,
    targets: list[float],
    predictions: list[float],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not (
        len(dataset.rows)
        == len(targets)
        == len(predictions)
    ):
        raise RuntimeError(
            "Prediction alignment check failed."
        )

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "zip_member",
                "level",
                "target_visibility_m",
                "prediction_m",
                "signed_error_m",
                "absolute_error_m",
            ],
        )

        writer.writeheader()

        for row, target, prediction in zip(
            dataset.rows,
            targets,
            predictions,
        ):
            error = prediction - target

            writer.writerow(
                {
                    "zip_member": row[
                        "zip_member"
                    ],
                    "level": int(
                        row["level"]
                    ),
                    "target_visibility_m": (
                        target
                    ),
                    "prediction_m": (
                        prediction
                    ),
                    "signed_error_m": error,
                    "absolute_error_m": abs(
                        error
                    ),
                }
            )


def level_metrics(
    dataset: FVEIDataset,
    targets: list[float],
    predictions: list[float],
) -> dict:
    grouped = {}

    for row, target, prediction in zip(
        dataset.rows,
        targets,
        predictions,
    ):
        level = int(
            row["level"]
        )

        grouped.setdefault(
            level,
            {
                "targets": [],
                "predictions": [],
            },
        )

        grouped[level][
            "targets"
        ].append(target)

        grouped[level][
            "predictions"
        ].append(prediction)

    results = {}

    for level in sorted(grouped):
        metrics = regression_metrics(
            grouped[level]["targets"],
            grouped[level]["predictions"],
        )

        results[str(level)] = metrics

    return results


def analyse_ceiling(
    dataset: FVEIDataset,
    predictions: list[float],
) -> dict:
    if len(dataset.rows) != len(predictions):
        raise RuntimeError(
            "Ceiling prediction alignment check failed."
        )

    threshold = 500.0

    sorted_predictions = sorted(
        predictions
    )

    n = len(
        sorted_predictions
    )

    if n == 0:
        raise ValueError(
            "No ceiling samples available."
        )

    if n % 2 == 1:
        median = sorted_predictions[
            n // 2
        ]
    else:
        median = (
            sorted_predictions[
                (n // 2) - 1
            ]
            + sorted_predictions[
                n // 2
            ]
        ) / 2.0

    at_or_above = sum(
        prediction >= threshold
        for prediction in predictions
    )

    below = n - at_or_above

    shortfalls = [
        max(
            0.0,
            threshold - prediction,
        )
        for prediction in predictions
    ]

    return {
        "n": n,
        "label_interpretation": (
            "ceiling/censored at 500 m; "
            "not treated as exact regression ground truth"
        ),
        "mean_prediction_m": (
            sum(predictions) / n
        ),
        "median_prediction_m": median,
        "min_prediction_m": min(
            predictions
        ),
        "max_prediction_m": max(
            predictions
        ),
        "predictions_at_or_above_500": (
            at_or_above
        ),
        "predictions_below_500": below,
        "fraction_at_or_above_500": (
            at_or_above / n
        ),
        "mean_shortfall_below_500_m": (
            sum(shortfalls) / n
        ),
    }


def save_ceiling_predictions(
    dataset: FVEIDataset,
    predictions: list[float],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "zip_member",
                "level",
                "ceiling_m",
                "prediction_m",
                "prediction_at_or_above_ceiling",
                "shortfall_below_ceiling_m",
            ],
        )

        writer.writeheader()

        for row, prediction in zip(
            dataset.rows,
            predictions,
        ):
            writer.writerow(
                {
                    "zip_member": row[
                        "zip_member"
                    ],
                    "level": int(
                        row["level"]
                    ),
                    "ceiling_m": 500.0,
                    "prediction_m": prediction,
                    "prediction_at_or_above_ceiling": (
                        prediction >= 500.0
                    ),
                    "shortfall_below_ceiling_m": (
                        max(
                            0.0,
                            500.0 - prediction,
                        )
                    ),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Final evaluation of the validation-selected "
            "VGG16 model on locked FVEI data."
        )
    )

    parser.add_argument(
        "--zip-path",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
    )

    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=DEFAULT_CHECKPOINT,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
    )

    args = parser.parse_args()

    model, checkpoint = load_model(
        args.checkpoint
    )

    print(
        "\n=== FINAL FVEI EVALUATION ==="
    )
    print(
        f"Device              : {DEVICE}"
    )
    print(
        f"Checkpoint          : {args.checkpoint}"
    )
    print(
        f"Selected epoch      : "
        f"{checkpoint.get('epoch', 'unknown')}"
    )
    print(
        f"Validation MAE      : "
        f"{checkpoint.get('validation_mae', 'unknown')}"
    )

    if checkpoint.get(
        "test_used_for_selection",
        False,
    ):
        raise RuntimeError(
            "Checkpoint metadata says test data "
            "was used for model selection."
        )

    test_dataset, test_loader = (
        build_loader(
            zip_path=args.zip_path,
            manifest_path=args.manifest,
            split="test",
            batch_size=args.batch_size,
        )
    )

    print(
        f"Held-out test size  : "
        f"{len(test_dataset)}"
    )

    test_targets, test_predictions = (
        predict(
            model=model,
            loader=test_loader,
        )
    )

    overall = regression_metrics(
        test_targets,
        test_predictions,
    )

    by_level = level_metrics(
        test_dataset,
        test_targets,
        test_predictions,
    )

    save_exact_predictions(
        dataset=test_dataset,
        targets=test_targets,
        predictions=test_predictions,
        output_path=(
            DEFAULT_TEST_PREDICTIONS
        ),
    )

    print(
        "\n=== LOCKED EXACT-LABEL TEST RESULTS ==="
    )
    print(
        f"N     : {overall['n']}"
    )
    print(
        f"MAE   : {overall['mae_m']:.4f} m"
    )
    print(
        f"RMSE  : {overall['rmse_m']:.4f} m"
    )
    print(
        f"R2    : {overall['r2']:.6f}"
    )
    print(
        f"Bias  : {overall['bias_m']:.4f} m"
    )

    print(
        "\n=== LEVEL-WISE EXACT TEST RESULTS ==="
    )

    for level, metrics in by_level.items():
        print(
            f"Level {level} | "
            f"N={metrics['n']} | "
            f"MAE={metrics['mae_m']:.4f} m | "
            f"RMSE={metrics['rmse_m']:.4f} m | "
            f"Bias={metrics['bias_m']:.4f} m"
        )

    ceiling_dataset, ceiling_loader = (
        build_loader(
            zip_path=args.zip_path,
            manifest_path=args.manifest,
            split="ceiling_eval",
            batch_size=args.batch_size,
        )
    )

    _, ceiling_predictions = predict(
        model=model,
        loader=ceiling_loader,
    )

    ceiling = analyse_ceiling(
        dataset=ceiling_dataset,
        predictions=ceiling_predictions,
    )

    save_ceiling_predictions(
        dataset=ceiling_dataset,
        predictions=ceiling_predictions,
        output_path=(
            DEFAULT_CEILING_PREDICTIONS
        ),
    )

    print(
        "\n=== 500 m CEILING ANALYSIS ==="
    )
    print(
        f"N                       : "
        f"{ceiling['n']}"
    )
    print(
        f"Mean prediction         : "
        f"{ceiling['mean_prediction_m']:.4f} m"
    )
    print(
        f"Median prediction       : "
        f"{ceiling['median_prediction_m']:.4f} m"
    )
    print(
        f"Predictions >= 500 m    : "
        f"{ceiling['predictions_at_or_above_500']}"
        f"/{ceiling['n']} "
        f"({ceiling['fraction_at_or_above_500']:.2%})"
    )
    print(
        f"Mean shortfall below 500: "
        f"{ceiling['mean_shortfall_below_500_m']:.4f} m"
    )

    summary = {
        "dataset": "FVEI",
        "checkpoint": str(
            args.checkpoint
        ),
        "selected_epoch": checkpoint.get(
            "epoch"
        ),
        "selection_validation_mae_m": (
            checkpoint.get(
                "validation_mae"
            )
        ),
        "held_out_test": {
            "used_for_model_selection": False,
            "metrics": overall,
            "level_metrics": by_level,
        },
        "ceiling_eval": ceiling,
        "notes": [
            (
                "Exact-label test metrics use only "
                "FVEI levels 0-3."
            ),
            (
                "Level-4 500 m samples are analysed "
                "separately as ceiling/censored labels."
            ),
            (
                "Ceiling samples are not included in "
                "exact-label MAE, RMSE, or R2."
            ),
        ],
    }

    DEFAULT_SUMMARY.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    DEFAULT_SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "\nResults saved:"
    )
    print(
        f"  {DEFAULT_TEST_PREDICTIONS}"
    )
    print(
        f"  {DEFAULT_CEILING_PREDICTIONS}"
    )
    print(
        f"  {DEFAULT_SUMMARY}"
    )


if __name__ == "__main__":
    main()
