"""
evaluation_vgg16_se.py

Evaluation pipeline for the SE-enhanced VGG16 regression model
used in fog visibility estimation.

The evaluation procedure is intentionally aligned with the VGG16
baseline and VGG16 + CBAM evaluations so that the effect of the
attention mechanism can be compared under identical test conditions.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn

from src.models.vgg16_se import (
    build_vgg16_se_regression_model,
)
from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    DROPOUT_RATE,
    FREEZE_BACKBONE,
    IMAGE_SIZE,
    NUM_WORKERS,
    RANDOM_SEED,
    REGRESSION_HIDDEN_DIM_1,
    REGRESSION_HIDDEN_DIM_2,
    RESULTS_DIR,
    TEST_RATIO,
    TRAIN_RATIO,
    VAL_RATIO,
    VGG16_SE_CHECKPOINT_PATH,
    create_output_directories,
)
from src.training.dataloader import create_dataloaders
from src.training.utils import set_seed


SE_REDUCTION_RATIO = 16


def load_se_model(
    checkpoint_path: Path,
) -> tuple[nn.Module, dict]:
    """
    Build the VGG16 + SE model and load the best checkpoint.
    """

    model = build_vgg16_se_regression_model(
        freeze_backbone=FREEZE_BACKBONE,
        regression_hidden_dim_1=REGRESSION_HIDDEN_DIM_1,
        regression_hidden_dim_2=REGRESSION_HIDDEN_DIM_2,
        dropout_rate=DROPOUT_RATE,
        se_reduction_ratio=SE_REDUCTION_RATIO,
    )

    checkpoint = torch.load(
        checkpoint_path,
        map_location=DEVICE,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model = model.to(DEVICE)
    model.eval()

    return model, checkpoint


def evaluate_model(
    model: nn.Module,
    test_loader,
) -> tuple[pd.DataFrame, dict]:
    """
    Evaluate the model on the independent test set.
    """

    predictions = []
    targets = []

    model.eval()

    with torch.no_grad():
        for images, batch_targets in test_loader:
            images = images.to(DEVICE)
            batch_targets = batch_targets.to(DEVICE)

            batch_predictions = (
                model(images)
                .squeeze(1)
            )

            predictions.extend(
                batch_predictions.cpu().numpy().tolist()
            )

            targets.extend(
                batch_targets.cpu().numpy().tolist()
            )

    results_df = pd.DataFrame(
        {
            "actual_visibility_m": targets,
            "predicted_visibility_m": predictions,
        }
    )

    results_df["signed_error_m"] = (
        results_df["predicted_visibility_m"]
        - results_df["actual_visibility_m"]
    )

    results_df["absolute_error_m"] = (
        results_df["signed_error_m"].abs()
    )

    test_mae = (
        results_df["absolute_error_m"].mean()
    )

    mean_signed_error = (
        results_df["signed_error_m"].mean()
    )

    min_absolute_error = (
        results_df["absolute_error_m"].min()
    )

    max_absolute_error = (
        results_df["absolute_error_m"].max()
    )

    summary = {
        "test_samples": int(len(results_df)),
        "test_mae_m": float(test_mae),
        "mean_signed_error_m": float(
            mean_signed_error
        ),
        "min_absolute_error_m": float(
            min_absolute_error
        ),
        "max_absolute_error_m": float(
            max_absolute_error
        ),
    }

    return results_df, summary


def save_actual_vs_predicted_plot(
    results_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Save actual vs predicted visibility scatter plot.
    """

    actual = results_df[
        "actual_visibility_m"
    ]

    predicted = results_df[
        "predicted_visibility_m"
    ]

    minimum = min(
        actual.min(),
        predicted.min(),
    )

    maximum = max(
        actual.max(),
        predicted.max(),
    )

    plt.figure(
        figsize=(8, 8)
    )

    plt.scatter(
        actual,
        predicted,
        alpha=0.7,
    )

    plt.plot(
        [minimum, maximum],
        [minimum, maximum],
        linestyle="--",
        label="Ideal Prediction",
    )

    plt.xlabel(
        "Actual Visibility (m)"
    )

    plt.ylabel(
        "Predicted Visibility (m)"
    )

    plt.title(
        "VGG16 + SE: Actual vs Predicted Visibility"
    )

    plt.legend()
    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def save_error_histogram(
    results_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Save prediction signed-error histogram.
    """

    signed_errors = results_df[
        "signed_error_m"
    ]

    plt.figure(
        figsize=(10, 6)
    )

    plt.hist(
        signed_errors,
        bins=20,
        edgecolor="black",
    )

    plt.axvline(
        0,
        linestyle="--",
        label="Zero Error",
    )

    plt.xlabel(
        "Prediction Error (m)"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.title(
        "VGG16 + SE Prediction Error Distribution"
    )

    plt.legend()
    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def save_evaluation_report(
    report_path: Path,
    summary: dict,
    checkpoint: dict,
) -> None:
    """
    Save a human-readable Markdown evaluation report.
    """

    checkpoint_epoch = checkpoint.get(
        "epoch",
        "unknown",
    )

    validation_mae = checkpoint.get(
        "validation_mae",
        "unknown",
    )

    if isinstance(
        validation_mae,
        (int, float),
    ):
        validation_mae_text = (
            f"{validation_mae:.4f} m"
        )
    else:
        validation_mae_text = str(
            validation_mae
        )

    lines = [
        "# VGG16 + SE Evaluation Report",
        "",
        "## Model",
        "",
        "- Architecture: VGG16 + SE",
        "- Pretrained weights: ImageNet",
        f"- Frozen backbone: {FREEZE_BACKBONE}",
        (
            "- SE reduction ratio: "
            f"{SE_REDUCTION_RATIO}"
        ),
        (
            "- SE integration point: "
            "after VGG16 conv5_3 and before final MaxPool"
        ),
        "",
        "## Checkpoint",
        "",
        (
            "- Best checkpoint epoch: "
            f"{checkpoint_epoch}"
        ),
        (
            "- Validation MAE at checkpoint: "
            f"{validation_mae_text}"
        ),
        "",
        "## Test Results",
        "",
        (
            "- Test samples: "
            f"{summary['test_samples']}"
        ),
        (
            "- Test MAE: "
            f"{summary['test_mae_m']:.4f} m"
        ),
        (
            "- Mean signed error: "
            f"{summary['mean_signed_error_m']:.4f} m"
        ),
        (
            "- Minimum absolute error: "
            f"{summary['min_absolute_error_m']:.4f} m"
        ),
        (
            "- Maximum absolute error: "
            f"{summary['max_absolute_error_m']:.4f} m"
        ),
        "",
        "## Interpretation",
        "",
        (
            "The VGG16 + SE model was evaluated on the same "
            "independent scene-based test split used for the "
            "VGG16 baseline and VGG16 + CBAM experiments. "
            "The resulting metrics can therefore be directly "
            "compared under the current synthetic FRIDA/FRIDA2 "
            "experimental setup."
        ),
    ]

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    """
    Run the complete VGG16 + SE evaluation pipeline.
    """

    set_seed(
        RANDOM_SEED
    )

    create_output_directories()

    _, _, test_loader = create_dataloaders(
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        random_seed=RANDOM_SEED,
        pin_memory=(DEVICE.type == "cuda"),
    )

    model, checkpoint = load_se_model(
        VGG16_SE_CHECKPOINT_PATH
    )

    results_df, summary = evaluate_model(
        model,
        test_loader,
    )

    evaluation_dir = (
        RESULTS_DIR / "evaluation"
    )

    plots_dir = (
        RESULTS_DIR / "plots"
    )

    logs_dir = (
        RESULTS_DIR / "logs"
    )

    predictions_path = (
        evaluation_dir
        / "vgg16_se_test_predictions.csv"
    )

    summary_path = (
        evaluation_dir
        / "vgg16_se_evaluation_summary.json"
    )

    actual_vs_predicted_path = (
        plots_dir
        / "vgg16_se_actual_vs_predicted.png"
    )

    error_histogram_path = (
        plots_dir
        / "vgg16_se_prediction_error_histogram.png"
    )

    report_path = (
        logs_dir
        / "vgg16_se_evaluation_report.md"
    )

    evaluation_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df.to_csv(
        predictions_path,
        index=False,
    )

    summary_with_checkpoint = {
        **summary,
        "checkpoint_epoch": checkpoint.get(
            "epoch"
        ),
        "checkpoint_validation_mae_m": checkpoint.get(
            "validation_mae"
        ),
        "random_seed": checkpoint.get(
            "random_seed",
            RANDOM_SEED,
        ),
        "model_name": checkpoint.get(
            "model_name",
            "VGG16_SE",
        ),
        "se_reduction_ratio": checkpoint.get(
            "se_reduction_ratio",
            SE_REDUCTION_RATIO,
        ),
    }

    summary_path.write_text(
        json.dumps(
            summary_with_checkpoint,
            indent=4,
        ),
        encoding="utf-8",
    )

    save_actual_vs_predicted_plot(
        results_df,
        actual_vs_predicted_path,
    )

    save_error_histogram(
        results_df,
        error_histogram_path,
    )

    save_evaluation_report(
        report_path,
        summary,
        checkpoint,
    )

    print("=" * 70)
    print(
        "VGG16 + SE Fog Visibility Regression Evaluation"
    )
    print("=" * 70)

    print(
        f"Device                : {DEVICE}"
    )

    print(
        "Checkpoint epoch      : "
        f"{checkpoint.get('epoch')}"
    )

    print(
        "Checkpoint val MAE    : "
        f"{checkpoint.get('validation_mae'):.4f} m"
    )

    print(
        "Test samples          : "
        f"{summary['test_samples']}"
    )

    print(
        "Test MAE              : "
        f"{summary['test_mae_m']:.4f} m"
    )

    print(
        "Mean signed error     : "
        f"{summary['mean_signed_error_m']:.4f} m"
    )

    print(
        "Min absolute error    : "
        f"{summary['min_absolute_error_m']:.4f} m"
    )

    print(
        "Max absolute error    : "
        f"{summary['max_absolute_error_m']:.4f} m"
    )

    print("=" * 70)

    print(
        f"Predictions CSV       : {predictions_path}"
    )

    print(
        f"Summary JSON          : {summary_path}"
    )

    print(
        "Actual vs predicted   : "
        f"{actual_vs_predicted_path}"
    )

    print(
        "Error histogram       : "
        f"{error_histogram_path}"
    )

    print(
        f"Evaluation report     : {report_path}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()