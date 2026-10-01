from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = PROJECT_ROOT / "figures"
REPORTS_DIR = PROJECT_ROOT / "docs" / "reports"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def add_bar_labels(ax, bars, digits=1):
    for bar in bars:
        value = bar.get_height()
        ax.annotate(
            f"{value:.{digits}f}",
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
        )


# ============================================================
# FIGURE 1 — SYNTHETIC MODEL TEST MAE COMPARISON
# ============================================================

models = [
    "VGG16\nBaseline",
    "VGG16 +\nCBAM",
    "VGG16 +\nSE",
    "ResNet50\nBaseline",
]

synthetic_test_mae = [
    66.7227,
    67.6214,
    72.4412,
    124.6181,
]

fig, ax = plt.subplots(figsize=(9, 5.5))

bars = ax.bar(
    models,
    synthetic_test_mae,
)

ax.set_title(
    "Synthetic FRIDA/FRIDA2 Model Comparison"
)
ax.set_ylabel(
    "Test MAE (m)"
)
ax.set_xlabel(
    "Model"
)

add_bar_labels(
    ax,
    bars,
    digits=1,
)

ax.set_ylim(
    0,
    max(synthetic_test_mae) * 1.18,
)

fig.tight_layout()

synthetic_path = (
    FIGURES_DIR
    / "synthetic_model_test_mae_comparison.png"
)

fig.savefig(
    synthetic_path,
    dpi=220,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# FIGURE 2 — FVEI FINE-TUNING CURVE
# ============================================================

epochs = np.arange(
    1,
    21,
)

train_mae = np.array(
    [
        36.2769,
        29.6925,
        27.8267,
        27.3721,
        26.0067,
        25.0751,
        23.9177,
        23.7444,
        22.4987,
        21.2353,
        21.3657,
        21.9587,
        20.8836,
        20.0084,
        19.8957,
        19.9092,
        19.2767,
        19.0097,
        18.3570,
        17.1478,
    ],
    dtype=float,
)

validation_mae = np.array(
    [
        32.2482,
        30.8165,
        28.3073,
        27.9038,
        27.8876,
        28.4745,
        26.8564,
        27.8244,
        28.3680,
        27.8311,
        28.2669,
        26.4428,
        27.3586,
        26.8907,
        26.9281,
        26.9374,
        26.5604,
        28.0043,
        27.8942,
        28.5279,
    ],
    dtype=float,
)

selected_epoch = 12

fig, ax = plt.subplots(
    figsize=(9, 5.5)
)

ax.plot(
    epochs,
    train_mae,
    marker="o",
    linewidth=1.5,
    label="Train MAE",
)

ax.plot(
    epochs,
    validation_mae,
    marker="o",
    linewidth=1.5,
    label="Validation MAE",
)

ax.axvline(
    selected_epoch,
    linestyle="--",
    linewidth=1.2,
    label="Selected Epoch 12",
)

ax.scatter(
    [selected_epoch],
    [validation_mae[selected_epoch - 1]],
    s=70,
    zorder=5,
)

ax.annotate(
    "Best Val MAE = 26.4428 m",
    xy=(
        selected_epoch,
        validation_mae[selected_epoch - 1],
    ),
    xytext=(13, 33),
    textcoords="data",
    arrowprops={
        "arrowstyle": "->",
    },
)

ax.set_title(
    "FVEI Fine-Tuning: Training and Validation MAE"
)
ax.set_xlabel(
    "Epoch"
)
ax.set_ylabel(
    "MAE (m)"
)

ax.set_xticks(
    epochs,
)

ax.legend()

fig.tight_layout()

training_curve_path = (
    FIGURES_DIR
    / "fvei_finetuning_mae_curve.png"
)

fig.savefig(
    training_curve_path,
    dpi=220,
    bbox_inches="tight",
)

plt.close(fig)


# ============================================================
# FIGURE 3 — FVEI LEVEL-WISE ERROR ANALYSIS
# ============================================================

levels = [
    "Level 0",
    "Level 1",
    "Level 2",
    "Level 3",
]

level_mae = np.array(
    [
        11.1879,
        12.5699,
        21.8013,
        55.9664,
    ],
    dtype=float,
)

level_rmse = np.array(
    [
        14.2664,
        15.7690,
        29.4082,
        68.5106,
    ],
    dtype=float,
)

x = np.arange(
    len(levels)
)

width = 0.36

fig, ax = plt.subplots(
    figsize=(9, 5.5)
)

mae_bars = ax.bar(
    x - width / 2,
    level_mae,
    width,
    label="MAE",
)

rmse_bars = ax.bar(
    x + width / 2,
    level_rmse,
    width,
    label="RMSE",
)

ax.set_title(
    "FVEI Held-Out Test Error by Visibility Level"
)
ax.set_xlabel(
    "Visibility Level"
)
ax.set_ylabel(
    "Error (m)"
)

ax.set_xticks(
    x,
    levels,
)

ax.legend()

add_bar_labels(
    ax,
    mae_bars,
    digits=1,
)

add_bar_labels(
    ax,
    rmse_bars,
    digits=1,
)

ax.set_ylim(
    0,
    max(level_rmse) * 1.20,
)

fig.tight_layout()

level_error_path = (
    FIGURES_DIR
    / "fvei_levelwise_error_comparison.png"
)

fig.savefig(
    level_error_path,
    dpi=220,
    bbox_inches="tight",
)

plt.close(fig)


print(
    f"Created: {synthetic_path}"
)
print(
    f"Created: {training_curve_path}"
)
print(
    f"Created: {level_error_path}"
)
