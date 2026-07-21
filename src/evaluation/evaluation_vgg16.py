"""
evaluation_vgg16.py

Evaluation pipeline for the pretrained VGG16 baseline model
used in fog visibility regression.

This script loads the best saved checkpoint and evaluates the
model on the held-out test dataset. It also generates evaluation
metrics, prediction files, plots, and a summary report.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn

from src.training.config import (
    BATCH_SIZE,
    CHECKPOINTS_DIR,
    DEVICE,
    IMAGE_SIZE,
    NUM_WORKERS,
    RANDOM_SEED,
    TEST_RATIO,
    TRAIN_RATIO,
    VAL_RATIO,
    VGG16_CHECKPOINT_PATH,
)

from src.training.dataloader import (
    create_dataloaders,
    split_dataframe_by_scene,
)

from src.training.train_vgg16 import (
    build_vgg16_regression_model,
)

from src.training.utils import set_seed


# =============================================================================
# Output Directories
# =============================================================================

RESULTS_DIR = CHECKPOINTS_DIR.parent

EVALUATION_DIR = RESULTS_DIR / "evaluation"
PLOTS_DIR = RESULTS_DIR / "plots"
LOGS_DIR = RESULTS_DIR / "logs"

EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Checkpoint Loading
# =============================================================================

def load_trained_model(
    checkpoint_path: Path = VGG16_CHECKPOINT_PATH,
) -> tuple[nn.Module, dict]:
    """
    Load the trained VGG16 regression model from a checkpoint.

    Returns:
        tuple[nn.Module, dict]:
            Loaded model and checkpoint metadata.
    """

    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {checkpoint_path}"
        )

    model = build_vgg16_regression_model()

    checkpoint = torch.load(
        checkpoint_path,
        map_location=DEVICE,
        weights_only=False,
    )

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            "Checkpoint does not contain 'model_state_dict'."
        )

    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(DEVICE)
    model.eval()

    return model, checkpoint

# =============================================================================
# Evaluation
# =============================================================================

def evaluate_model(
    model: nn.Module,
) -> tuple[list[float], list[float], float]:
    """
    Evaluate the trained model on the held-out test dataset.

    Returns:
        tuple:
            Ground-truth visibility values,
            predicted visibility values,
            mean test MAE.
    """

    set_seed(RANDOM_SEED)

    pin_memory = DEVICE.type == "cuda"

    _, _, test_loader = create_dataloaders(
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        random_seed=RANDOM_SEED,
        pin_memory=pin_memory,
    )

    loss_function = nn.L1Loss()

    ground_truths: list[float] = []
    predictions_list: list[float] = []

    running_mae = 0.0
    total_samples = 0

    model.eval()

    with torch.no_grad():
        for images, targets in test_loader:

            images = images.to(DEVICE)
            targets = targets.to(DEVICE)

            predictions = model(images).squeeze(1)

            loss = loss_function(predictions, targets)

            batch_size = images.size(0)

            running_mae += loss.item() * batch_size
            total_samples += batch_size

            ground_truths.extend(
                targets.cpu().tolist()
            )

            predictions_list.extend(
                predictions.cpu().tolist()
            )

    test_mae = running_mae / total_samples

    return (
        ground_truths,
        predictions_list,
        test_mae,
    )

# =============================================================================
# Prediction and Summary Outputs
# =============================================================================

def save_predictions_csv(
    ground_truths: list[float],
    predictions: list[float],
    output_path: Path,
) -> pd.DataFrame:
    """
    Save test predictions and absolute errors to a CSV file.

    Returns:
        pd.DataFrame:
            DataFrame containing test metadata, predictions, and errors.
    """

    _, _, test_dataframe = split_dataframe_by_scene(
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        random_seed=RANDOM_SEED,
    )

    test_dataframe = test_dataframe.reset_index(drop=True)

    if len(test_dataframe) != len(ground_truths):
        raise ValueError(
            "Test dataframe length does not match the number of predictions."
        )

    if len(ground_truths) != len(predictions):
        raise ValueError(
            "Ground-truth and prediction list lengths do not match."
        )

    prediction_dataframe = test_dataframe[
        [
            "filename",
            "scene_id",
            "source_dataset",
            "visibility_m",
        ]
    ].copy()

    prediction_dataframe = prediction_dataframe.rename(
        columns={
            "visibility_m": "ground_truth_m",
        }
    )

    prediction_dataframe["prediction_m"] = predictions

    prediction_dataframe["absolute_error_m"] = (
        prediction_dataframe["prediction_m"]
        - prediction_dataframe["ground_truth_m"]
    ).abs()

    prediction_dataframe["signed_error_m"] = (
        prediction_dataframe["prediction_m"]
        - prediction_dataframe["ground_truth_m"]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    prediction_dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    return prediction_dataframe


def save_evaluation_summary(
    checkpoint: dict,
    prediction_dataframe: pd.DataFrame,
    test_mae: float,
    output_path: Path,
) -> dict:
    """
    Save checkpoint and test evaluation information as JSON.

    Returns:
        dict:
            Evaluation summary.
    """

    summary = {
        "model": "VGG16",
        "dataset_split": "test",
        "test_samples": len(prediction_dataframe),
        "test_mae_m": round(test_mae, 4),
        "mean_signed_error_m": round(
            prediction_dataframe["signed_error_m"].mean(),
            4,
        ),
        "maximum_absolute_error_m": round(
            prediction_dataframe["absolute_error_m"].max(),
            4,
        ),
        "minimum_absolute_error_m": round(
            prediction_dataframe["absolute_error_m"].min(),
            4,
        ),
        "checkpoint_epoch": checkpoint.get("epoch"),
        "checkpoint_validation_mae_m": round(
            float(checkpoint.get("validation_mae")),
            4,
        ),
        "random_seed": checkpoint.get(
            "random_seed",
            RANDOM_SEED,
        ),
        "checkpoint_path": str(VGG16_CHECKPOINT_PATH),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        mode="w",
        encoding="utf-8",
    ) as output_file:
        json.dump(
            summary,
            output_file,
            indent=4,
            ensure_ascii=False,
        )

    return summary

# =============================================================================
# Evaluation Plots
# =============================================================================

def plot_actual_vs_predicted(
    prediction_dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Plot actual visibility values against model predictions.
    """

    plt.figure(figsize=(8, 8))

    plt.scatter(
        prediction_dataframe["ground_truth_m"],
        prediction_dataframe["prediction_m"],
        alpha=0.7,
    )

    minimum = min(
        prediction_dataframe["ground_truth_m"].min(),
        prediction_dataframe["prediction_m"].min(),
    )

    maximum = max(
        prediction_dataframe["ground_truth_m"].max(),
        prediction_dataframe["prediction_m"].max(),
    )

    plt.plot(
        [minimum, maximum],
        [minimum, maximum],
        linestyle="--",
        linewidth=2,
    )

    plt.xlabel("Ground Truth Visibility (m)")
    plt.ylabel("Predicted Visibility (m)")
    plt.title("VGG16 Predictions vs Ground Truth")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def plot_prediction_error_histogram(
    prediction_dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Plot the distribution of prediction errors.
    """

    plt.figure(figsize=(8, 5))

    plt.hist(
        prediction_dataframe["signed_error_m"],
        bins=20,
    )

    plt.axvline(
        0,
        linestyle="--",
        linewidth=2,
    )

    plt.xlabel("Prediction Error (m)")
    plt.ylabel("Image Count")
    plt.title("Prediction Error Distribution")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

# =============================================================================
# Evaluation Report
# =============================================================================

def save_evaluation_report(
    checkpoint: dict,
    summary: dict,
    output_path: Path,
) -> None:
    """
    Save a human-readable Markdown report for the VGG16 evaluation.
    """

    validation_mae = float(
        checkpoint.get(
            "validation_mae",
            summary["checkpoint_validation_mae_m"],
        )
    )

    test_mae = float(summary["test_mae_m"])

    mae_difference = test_mae - validation_mae

    if abs(mae_difference) < 10:
        generalization_comment = (
            "The test MAE is close to the validation MAE. "
            "This indicates that the model preserves similar performance "
            "on previously unseen scenes."
        )
    elif mae_difference > 0:
        generalization_comment = (
            "The test MAE is higher than the validation MAE. "
            "This suggests a performance decrease on previously unseen scenes "
            "and should be reviewed during model comparison."
        )
    else:
        generalization_comment = (
            "The test MAE is lower than the validation MAE. "
            "The model performed better on the held-out test scenes than on "
            "the validation scenes."
        )

    target_comment = (
        "The project target of MAE below 100 metres was achieved."
        if test_mae < 100
        else "The project target of MAE below 100 metres was not achieved."
    )

    lines = [
        "# VGG16 Baseline Evaluation Report",
        "",
        "## Model Information",
        "",
        "- Model: VGG16",
        "- Pretrained weights: ImageNet",
        f"- Checkpoint path: `{VGG16_CHECKPOINT_PATH}`",
        f"- Best checkpoint epoch: {summary['checkpoint_epoch']}",
        (
            "- Best validation MAE: "
            f"{summary['checkpoint_validation_mae_m']:.4f} m"
        ),
        "",
        "## Test Dataset",
        "",
        "- Split: Held-out test set",
        f"- Test image count: {summary['test_samples']}",
        f"- Random seed: {summary['random_seed']}",
        "",
        "## Evaluation Results",
        "",
        f"- Test MAE: {summary['test_mae_m']:.4f} m",
        (
            "- Mean signed error: "
            f"{summary['mean_signed_error_m']:.4f} m"
        ),
        (
            "- Minimum absolute error: "
            f"{summary['minimum_absolute_error_m']:.4f} m"
        ),
        (
            "- Maximum absolute error: "
            f"{summary['maximum_absolute_error_m']:.4f} m"
        ),
        (
            "- Test-validation MAE difference: "
            f"{mae_difference:.4f} m"
        ),
        "",
        "## Interpretation",
        "",
        generalization_comment,
        "",
        target_comment,
        "",
        "## Generated Outputs",
        "",
        "- `results/evaluation/vgg16_test_predictions.csv`",
        "- `results/evaluation/vgg16_evaluation_summary.json`",
        "- `results/plots/vgg16_actual_vs_predicted.png`",
        "- `results/plots/vgg16_prediction_error_histogram.png`",
        "",
        "## Next Stage",
        "",
        "The next stage is to implement and train the ResNet50 baseline "
        "under the same dataset split, preprocessing pipeline, evaluation "
        "metrics, and reproducibility settings. The VGG16 and ResNet50 "
        "results will then be compared using validation MAE, test MAE, "
        "error distributions, and prediction behaviour.",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

# =============================================================================
# Evaluation Pipeline
# =============================================================================

def evaluate_vgg16() -> None:
    """
    Run the complete VGG16 test evaluation pipeline.
    """

    set_seed(RANDOM_SEED)

    prediction_csv_path = (
        EVALUATION_DIR / "vgg16_test_predictions.csv"
    )

    summary_json_path = (
        EVALUATION_DIR / "vgg16_evaluation_summary.json"
    )

    actual_vs_predicted_path = (
        PLOTS_DIR / "vgg16_actual_vs_predicted.png"
    )

    error_histogram_path = (
        PLOTS_DIR / "vgg16_prediction_error_histogram.png"
    )

    evaluation_report_path = (
        LOGS_DIR / "vgg16_evaluation_report.md"
    )

    print("=" * 70)
    print("VGG16 Fog Visibility Regression Evaluation")
    print("=" * 70)
    print(f"Device          : {DEVICE}")
    print(f"Checkpoint path : {VGG16_CHECKPOINT_PATH}")
    print("=" * 70)

    model, checkpoint = load_trained_model()

    print(
        "Checkpoint loaded "
        f"(Epoch: {checkpoint.get('epoch')}, "
        f"Validation MAE: "
        f"{float(checkpoint.get('validation_mae')):.4f} m)"
    )

    ground_truths, predictions, test_mae = evaluate_model(
        model=model,
    )

    prediction_dataframe = save_predictions_csv(
        ground_truths=ground_truths,
        predictions=predictions,
        output_path=prediction_csv_path,
    )

    summary = save_evaluation_summary(
        checkpoint=checkpoint,
        prediction_dataframe=prediction_dataframe,
        test_mae=test_mae,
        output_path=summary_json_path,
    )

    plot_actual_vs_predicted(
        prediction_dataframe=prediction_dataframe,
        output_path=actual_vs_predicted_path,
    )

    plot_prediction_error_histogram(
        prediction_dataframe=prediction_dataframe,
        output_path=error_histogram_path,
    )

    save_evaluation_report(
        checkpoint=checkpoint,
        summary=summary,
        output_path=evaluation_report_path,
    )

    print("=" * 70)
    print("Evaluation completed.")
    print(f"Test samples      : {summary['test_samples']}")
    print(f"Test MAE          : {summary['test_mae_m']:.4f} m")
    print(
        "Validation MAE    : "
        f"{summary['checkpoint_validation_mae_m']:.4f} m"
    )
    print(
        "Mean signed error : "
        f"{summary['mean_signed_error_m']:.4f} m"
    )
    print(f"Predictions CSV   : {prediction_csv_path}")
    print(f"Summary JSON      : {summary_json_path}")
    print(f"Prediction plot   : {actual_vs_predicted_path}")
    print(f"Error histogram   : {error_histogram_path}")
    print(f"Evaluation report : {evaluation_report_path}")
    print("=" * 70)


def main() -> None:
    evaluate_vgg16()


if __name__ == "__main__":
    main()