"""
finetune_fvei.py

Architecture-agnostic FVEI fine-tuning, used to close two gaps in the
research design:

1. The research question compares VGG16 and ResNet50 on synthetic
   *and* real-world data, but only VGG16 had been fine-tuned on FVEI.
   This script fine-tunes ResNet50 with the same protocol:

       python -m src.training.finetune_fvei --arch resnet50 \
           --init synthetic --zip-path <FVEI.zip>

2. The proposal motivates a staged data strategy (synthetic first,
   then real data). Whether the synthetic stage actually helps can be
   tested by starting directly from ImageNet weights:

       python -m src.training.finetune_fvei --arch vgg16 \
           --init imagenet --zip-path <FVEI.zip>

Protocol (identical for every run)
----------------------------------
- FVEI train / validation splits from the final split manifest
- last convolutional stage + regression head trainable
  (VGG16 Block 5 / ResNet50 layer4), everything else frozen
- last stage LR 1e-5, head LR 1e-4, Adam, weight decay 1e-5
- L1 loss, 20 epochs, batch size 16, seed 42
- checkpoint selected by validation MAE only
- the locked test split is never instantiated here

The original final model (results/checkpoints/vgg16_fvei_block5_best.pth)
is never overwritten. Every run is written under its own run name.

Outputs
-------
results/checkpoints/fvei_runs/<run_name>_best.pth
results/fvei/runs/<run_name>/history.csv
results/fvei/runs/<run_name>/training_summary.json

After training, evaluate the run once on the locked test split with
src.evaluation.evaluate_fvei.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from src.models.regression_models import (
    DISPLAY_NAMES,
    LAST_BLOCK_NAMES,
    SUPPORTED_ARCHITECTURES,
    build_regression_model,
    configure_last_block_finetuning,
    last_block_parameter_groups,
    set_train_mode,
    verify_last_block_finetuning,
)
from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    IMAGE_SIZE,
    LEARNING_RATE,
    NUM_EPOCHS,
    NUM_WORKERS,
    RANDOM_SEED,
    RESNET50_CHECKPOINT_PATH,
    VGG16_CHECKPOINT_PATH,
    WEIGHT_DECAY,
)
from src.training.dataloader import get_transforms
from src.training.fvei_dataloader import DEFAULT_MANIFEST, FVEIDataset
from src.training.utils import set_seed


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHECKPOINT_DIR = PROJECT_ROOT / "results" / "checkpoints" / "fvei_runs"
RUNS_DIR = PROJECT_ROOT / "results" / "fvei" / "runs"

SYNTHETIC_CHECKPOINTS = {
    "vgg16": VGG16_CHECKPOINT_PATH,
    "resnet50": RESNET50_CHECKPOINT_PATH,
}

DEFAULT_LAST_BLOCK_LR = 1e-5
DEFAULT_HEAD_LR = LEARNING_RATE

HELD_OUT_TEST_SIZE = 482


def relative_path(path: Path) -> str:
    """Store project paths relative to the repository root."""

    try:
        return Path(path).resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return Path(path).name


def default_run_name(arch: str, init: str, seed: int) -> str:
    return f"{arch}_fvei_{init}_lastblock_s{seed}"


def build_initial_model(arch: str, init: str) -> tuple[nn.Module, dict]:
    """
    init='synthetic': start from the synthetic FRIDA/FRIDA2 checkpoint.
    init='imagenet' : start from ImageNet weights with a new head.
    """

    if init == "imagenet":
        model = build_regression_model(arch, pretrained=True)
        return model, {"source": "ImageNet", "source_checkpoint": None}

    checkpoint_path = SYNTHETIC_CHECKPOINTS[arch]

    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Synthetic {DISPLAY_NAMES[arch]} checkpoint not found: "
            f"{checkpoint_path}"
        )

    model = build_regression_model(arch, pretrained=False)
    checkpoint = torch.load(checkpoint_path, map_location="cpu")

    if "model_state_dict" not in checkpoint:
        raise KeyError("Synthetic checkpoint has no 'model_state_dict'.")

    # strict=True (default): fails loudly if the head layout differs.
    model.load_state_dict(checkpoint["model_state_dict"])

    return model, {
        "source": "synthetic FRIDA/FRIDA2",
        "source_checkpoint": relative_path(checkpoint_path),
        "source_epoch": checkpoint.get("epoch"),
        "source_validation_mae_m": checkpoint.get("validation_mae"),
    }


def create_train_val_loaders(
    zip_path: Path,
    manifest_path: Path,
    batch_size: int,
    seed: int,
) -> tuple[DataLoader, DataLoader]:
    transform = get_transforms(image_size=IMAGE_SIZE)

    train_dataset = FVEIDataset(zip_path, manifest_path, "train", transform)
    val_dataset = FVEIDataset(zip_path, manifest_path, "val", transform)

    generator = torch.Generator()
    generator.manual_seed(seed)

    pin_memory = DEVICE.type == "cuda"

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=pin_memory,
        generator=generator,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=pin_memory,
    )

    return train_loader, val_loader


def run_epoch(
    model: nn.Module,
    loader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer | None = None,
    max_batches: int | None = None,
) -> float:
    """Train when an optimizer is given, otherwise evaluate. Returns MAE."""

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

            images = images.to(DEVICE, non_blocking=True)
            targets = targets.to(DEVICE, non_blocking=True)

            predictions = model(images).squeeze(1)
            loss = loss_function(predictions, targets)

            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            total_loss += loss.item() * images.size(0)
            total_samples += images.size(0)

    return total_loss / max(total_samples, 1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--arch", choices=SUPPORTED_ARCHITECTURES, required=True)
    parser.add_argument(
        "--init", choices=("synthetic", "imagenet"), default="synthetic"
    )
    parser.add_argument("--zip-path", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--last-block-lr", type=float, default=DEFAULT_LAST_BLOCK_LR)
    parser.add_argument("--head-lr", type=float, default=DEFAULT_HEAD_LR)
    parser.add_argument("--run-name", type=str, default=None)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load data and model, run 2 train + 2 val batches, save nothing.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting an existing run with the same name.",
    )
    args = parser.parse_args()

    run_name = args.run_name or default_run_name(args.arch, args.init, args.seed)
    run_dir = RUNS_DIR / run_name
    checkpoint_path = CHECKPOINT_DIR / f"{run_name}_best.pth"

    if (
        not args.dry_run
        and not args.overwrite
        and (run_dir / "training_summary.json").exists()
    ):
        raise FileExistsError(
            f"Run '{run_name}' already exists. Use --overwrite or --run-name."
        )

    set_seed(args.seed)

    train_loader, val_loader = create_train_val_loaders(
        args.zip_path, args.manifest, args.batch_size, args.seed
    )

    model, source_info = build_initial_model(args.arch, args.init)
    configure_last_block_finetuning(model, args.arch)
    counts = verify_last_block_finetuning(model, args.arch)
    model = model.to(DEVICE)

    print("=" * 64)
    print(f"FVEI fine-tuning : {run_name}")
    print("=" * 64)
    print(f"Architecture     : {DISPLAY_NAMES[args.arch]}")
    print(f"Initialisation   : {source_info['source']}")
    print(f"Trainable stage  : {LAST_BLOCK_NAMES[args.arch]} + regression head")
    print(f"  last block     : {counts['last_block']:,} parameters")
    print(f"  head           : {counts['head']:,} parameters")
    print(f"  frozen         : {counts['frozen']:,} parameters")
    print(f"Device           : {DEVICE}")
    print(f"Train / val      : {len(train_loader.dataset)} / {len(val_loader.dataset)}")
    print("Locked test      : NOT ACCESSED")
    print(f"Epochs           : {args.epochs}")
    print(f"LR (block/head)  : {args.last_block_lr} / {args.head_lr}")
    print(f"Seed             : {args.seed}")

    loss_function = nn.L1Loss()
    optimizer = Adam(
        last_block_parameter_groups(
            model, args.arch, args.last_block_lr, args.head_lr
        ),
        weight_decay=WEIGHT_DECAY,
    )

    if args.dry_run:
        train_mae = run_epoch(model, train_loader, loss_function, optimizer, 2)
        val_mae = run_epoch(model, val_loader, loss_function, None, 2)
        print("\n=== DRY RUN OK ===")
        print(f"2-batch train MAE : {train_mae:.2f} m")
        print(f"2-batch val MAE   : {val_mae:.2f} m")
        print("Nothing was saved. Locked test split was not accessed.")
        return

    best_validation_mae = float("inf")
    best_epoch = 0
    history = []

    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        train_mae = run_epoch(model, train_loader, loss_function, optimizer)
        validation_mae = run_epoch(model, val_loader, loss_function)

        history.append(
            {"epoch": epoch, "train_mae": train_mae, "validation_mae": validation_mae}
        )

        print(
            f"Epoch [{epoch:02d}/{args.epochs}] | Train MAE: {train_mae:.4f} m "
            f"| Validation MAE: {validation_mae:.4f} m"
        )

        if validation_mae < best_validation_mae:
            best_validation_mae = validation_mae
            best_epoch = epoch

            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "training_mae": train_mae,
                    "validation_mae": validation_mae,
                    "arch": args.arch,
                    "init": args.init,
                    "run_name": run_name,
                    "random_seed": args.seed,
                    "dataset": "FVEI",
                    "split_manifest": relative_path(args.manifest),
                    "fine_tuning_strategy": (
                        f"{LAST_BLOCK_NAMES[args.arch]} + regression head"
                    ),
                    "last_block_learning_rate": args.last_block_lr,
                    "head_learning_rate": args.head_lr,
                    "weight_decay": WEIGHT_DECAY,
                    "loss_function": "L1Loss",
                    "test_used_for_selection": False,
                    **source_info,
                },
                checkpoint_path,
            )
            print("  -> best checkpoint saved")

    with (run_dir / "history.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["epoch", "train_mae", "validation_mae"]
        )
        writer.writeheader()
        writer.writerows(history)

    summary = {
        "run_name": run_name,
        "dataset": "FVEI",
        "arch": args.arch,
        "init": args.init,
        **source_info,
        "output_checkpoint": relative_path(checkpoint_path),
        "fine_tuning_strategy": f"{LAST_BLOCK_NAMES[args.arch]} + regression head",
        "trainable_parameters": counts,
        "training_samples": len(train_loader.dataset),
        "validation_samples": len(val_loader.dataset),
        "held_out_test_samples": HELD_OUT_TEST_SIZE,
        "test_used_for_selection": False,
        "best_epoch": best_epoch,
        "best_validation_mae": best_validation_mae,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "last_block_learning_rate": args.last_block_lr,
        "head_learning_rate": args.head_lr,
        "weight_decay": WEIGHT_DECAY,
        "loss_function": "L1Loss",
        "random_seed": args.seed,
        "device": str(DEVICE),
    }

    (run_dir / "training_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    print("\n=== FVEI FINE-TUNING COMPLETE ===")
    print(f"Best epoch          : {best_epoch}")
    print(f"Best validation MAE : {best_validation_mae:.4f} m")
    print(f"Checkpoint          : {relative_path(checkpoint_path)}")
    print("\nNext (run once):")
    print(
        f"  python -m src.evaluation.evaluate_fvei --run-name {run_name} "
        f"--zip-path \"{args.zip_path}\""
    )


if __name__ == "__main__":
    main()
