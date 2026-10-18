"""
train_synthetic_multiseed.py

Repeat the synthetic FRIDA/FRIDA2 baseline training with several
training seeds.

Why
---
All architecture comparisons were made with a single training seed
(42). Seed-to-seed variation shows whether the VGG16 vs ResNet50 gap
is robust. In addition, the original ResNet50 run selected its last
epoch (20/20), so it may not have converged; --epochs 50 checks this.
The 50-epoch ResNet50 runs again selected their last epoch in every
seed, so --patience adds validation-based early stopping: training
runs until validation MAE has not improved for <patience> epochs (or
--epochs is reached), letting both backbones train to convergence.

Protocol
--------
- same scene-based split as the original experiments (split seed 42)
- same model, head, frozen backbone, optimizer, LR and loss
- only the training seed changes (weight init of the head, dropout,
  shuffling order)
- checkpoint selected by validation MAE; the test split is evaluated
  once per seed with the selected weights
- the original checkpoints in results/checkpoints are never touched

Usage
-----
python -m src.training.train_synthetic_multiseed --arch vgg16
python -m src.training.train_synthetic_multiseed --arch resnet50
python -m src.training.train_synthetic_multiseed --arch resnet50 --epochs 50
python -m src.training.train_synthetic_multiseed --arch vgg16 --epochs 200 --patience 20
python -m src.training.train_synthetic_multiseed --arch resnet50 --epochs 200 --patience 20

Outputs (per seed)
------------------
results/multiseed/<arch>_e<epochs>[_p<patience>]/seed_<n>/summary.json
results/multiseed/<arch>_e<epochs>/seed_<n>/history.csv
results/multiseed/<arch>_e<epochs>/seed_<n>/test_predictions.csv

Checkpoints are not saved by default (~100-200 MB each); use
--save-checkpoints if needed.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from src.models.regression_models import (
    DISPLAY_NAMES,
    SUPPORTED_ARCHITECTURES,
    build_regression_model,
    freeze_all_but_head,
    set_train_mode,
)
from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    IMAGE_SIZE,
    LEARNING_RATE,
    NUM_EPOCHS,
    NUM_WORKERS,
    RANDOM_SEED,
    TEST_RATIO,
    TRAIN_RATIO,
    VAL_RATIO,
    WEIGHT_DECAY,
)
from src.training.dataloader import create_dataloaders
from src.training.utils import set_seed


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = PROJECT_ROOT / "results" / "multiseed"

DEFAULT_SEEDS = (42, 7, 123, 2024, 3407)


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer | None = None,
    max_batches: int | None = None,
) -> float:
    training = optimizer is not None

    if training:
        set_train_mode(model)
    else:
        model.eval()

    total_loss = 0.0
    total_samples = 0

    with torch.set_grad_enabled(training):
        for batch_index, (images, targets) in enumerate(loader):
            if max_batches is not None and batch_index >= max_batches:
                break

            images = images.to(DEVICE)
            targets = targets.to(DEVICE)

            predictions = model(images).squeeze(1)
            loss = loss_function(predictions, targets)

            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            total_loss += loss.item() * images.size(0)
            total_samples += images.size(0)

    return total_loss / max(total_samples, 1)


def predict(model: nn.Module, loader: DataLoader) -> np.ndarray:
    model.eval()
    outputs = []

    with torch.inference_mode():
        for images, _ in loader:
            outputs.append(model(images.to(DEVICE)).squeeze(1).cpu().numpy())

    return np.concatenate(outputs)


def train_one_seed(
    arch: str,
    training_seed: int,
    split_seed: int,
    epochs: int,
    output_dir: Path,
    save_checkpoint: bool,
    max_batches: int | None = None,
    patience: int | None = None,
) -> dict:
    set_seed(training_seed)

    pin_memory = DEVICE.type == "cuda"

    # The split is fixed by split_seed. The loaders' own shuffle
    # generator is also seeded with split_seed, so the training loader
    # is rebuilt with a generator seeded by the training seed.
    base_train, val_loader, test_loader = create_dataloaders(
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        random_seed=split_seed,
        pin_memory=pin_memory,
    )

    generator = torch.Generator()
    generator.manual_seed(training_seed)

    train_loader = DataLoader(
        base_train.dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=pin_memory,
        generator=generator,
    )

    model = build_regression_model(arch, pretrained=True)
    freeze_all_but_head(model, arch)
    model = model.to(DEVICE)

    loss_function = nn.L1Loss()
    optimizer = Adam(
        [p for p in model.parameters() if p.requires_grad],
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
    )

    best_validation_mae = float("inf")
    best_epoch = 0
    best_state = None
    history = []
    epochs_without_improvement = 0
    stopped_epoch = epochs

    for epoch in range(1, epochs + 1):
        train_mae = run_epoch(model, train_loader, loss_function, optimizer, max_batches)
        validation_mae = run_epoch(model, val_loader, loss_function, None, max_batches)
        history.append(
            {"epoch": epoch, "train_mae": train_mae, "validation_mae": validation_mae}
        )

        print(
            f"  [{DISPLAY_NAMES[arch]} seed {training_seed}] "
            f"epoch {epoch:02d}/{epochs} | train {train_mae:.2f} m "
            f"| val {validation_mae:.2f} m"
        )

        if validation_mae < best_validation_mae:
            best_validation_mae = validation_mae
            best_epoch = epoch
            best_state = copy.deepcopy(
                {k: v.detach().cpu() for k, v in model.state_dict().items()}
            )
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        if patience is not None and epochs_without_improvement >= patience:
            stopped_epoch = epoch
            print(
                f"  early stop at epoch {epoch}: no validation improvement "
                f"for {patience} epochs (best epoch {best_epoch})"
            )
            break

    model.load_state_dict(best_state)

    test_frame = test_loader.dataset.data
    predictions = predict(model, test_loader)
    targets = test_frame["visibility_m"].to_numpy(dtype=float)

    if max_batches is not None:
        n = min(len(predictions), len(targets))
        predictions, targets, test_frame = predictions[:n], targets[:n], test_frame.iloc[:n]

    errors = predictions - targets
    test_mae = float(np.mean(np.abs(errors)))

    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "test_predictions.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "filename",
                "scene_id",
                "source_dataset",
                "ground_truth_m",
                "prediction_m",
                "absolute_error_m",
                "signed_error_m",
            ]
        )
        for (_, row), prediction, error in zip(
            test_frame.iterrows(), predictions, errors
        ):
            writer.writerow(
                [
                    row["filename"],
                    row["scene_id"],
                    row["source_dataset"],
                    float(row["visibility_m"]),
                    float(prediction),
                    float(abs(error)),
                    float(error),
                ]
            )

    with (output_dir / "history.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["epoch", "train_mae", "validation_mae"]
        )
        writer.writeheader()
        writer.writerows(history)

    if save_checkpoint:
        torch.save(
            {
                "epoch": best_epoch,
                "model_state_dict": best_state,
                "validation_mae": best_validation_mae,
                "arch": arch,
                "training_seed": training_seed,
                "split_seed": split_seed,
            },
            output_dir / "best.pth",
        )

    summary = {
        "arch": arch,
        "model": DISPLAY_NAMES[arch],
        "training_seed": training_seed,
        "split_seed": split_seed,
        "epochs": epochs,
        "best_epoch": best_epoch,
        "best_epoch_is_last": best_epoch == epochs,
        "patience": patience,
        "stopped_epoch": stopped_epoch,
        "early_stopped": patience is not None and stopped_epoch < epochs,
        "converged_within_budget": (
            stopped_epoch < epochs if patience is not None else best_epoch < stopped_epoch
        ),
        "best_validation_mae_m": best_validation_mae,
        "test_mae_m": test_mae,
        "test_bias_m": float(np.mean(errors)),
        "test_samples": int(len(targets)),
        "frozen_backbone": True,
        "learning_rate": LEARNING_RATE,
        "weight_decay": WEIGHT_DECAY,
        "batch_size": BATCH_SIZE,
        "loss_function": "L1Loss",
        "device": str(DEVICE),
        "dry_run": max_batches is not None,
    }

    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--arch", choices=SUPPORTED_ARCHITECTURES, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS)
    parser.add_argument("--split-seed", type=int, default=RANDOM_SEED)
    parser.add_argument(
        "--patience",
        type=int,
        default=None,
        help=(
            "Stop when validation MAE has not improved for this many epochs. "
            "Selection still uses validation MAE only; test is evaluated once."
        ),
    )
    parser.add_argument("--save-checkpoints", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="1 seed, 1 epoch, 2 batches; output goes to results/multiseed/_dry_run.",
    )
    args = parser.parse_args()

    if args.dry_run:
        group_dir = OUTPUT_ROOT / "_dry_run"
        seeds, epochs, max_batches = args.seeds[:1], 1, 2
    else:
        suffix = f"_p{args.patience}" if args.patience is not None else ""
        group_dir = OUTPUT_ROOT / f"{args.arch}_e{args.epochs}{suffix}"
        seeds, epochs, max_batches = args.seeds, args.epochs, None

    print("=" * 64)
    print(f"Multi-seed synthetic training: {DISPLAY_NAMES[args.arch]}")
    print(f"Seeds  : {seeds}")
    print(f"Epochs : {epochs}   Split seed: {args.split_seed}   Device: {DEVICE}")
    print("=" * 64)

    summaries = []

    for seed in seeds:
        seed_dir = group_dir / f"seed_{seed}"

        if (seed_dir / "summary.json").exists() and not args.dry_run:
            print(f"[skip] seed {seed}: already finished")
            summaries.append(
                json.loads((seed_dir / "summary.json").read_text(encoding="utf-8"))
            )
            continue

        summaries.append(
            train_one_seed(
                args.arch,
                seed,
                args.split_seed,
                epochs,
                seed_dir,
                args.save_checkpoints,
                max_batches,
                args.patience,
            )
        )

    values = np.array([s["test_mae_m"] for s in summaries])

    print("\n=== RESULTS ===")
    for s in summaries:
        print(
            f"seed {s['training_seed']:>5} | best epoch {s['best_epoch']:>2} "
            f"| stopped {s.get('stopped_epoch', s['epochs']):>3} "
            f"| val {s['best_validation_mae_m']:.2f} m | test {s['test_mae_m']:.2f} m"
        )
    std = values.std(ddof=1) if len(values) > 1 else 0.0
    print(f"Test MAE: {values.mean():.2f} ± {std:.2f} m")

    if args.dry_run:
        print("\nDRY RUN OK (results/multiseed/_dry_run can be deleted).")
    else:
        print("\nRefresh statistics: python -m src.evaluation.statistical_analysis")


if __name__ == "__main__":
    main()
