"""
finetune_vgg16_fvei.py

Fine-tune the synthetic FRIDA/FRIDA2-trained VGG16 regression
model on the FVEI real-world visibility dataset.

Protocol:
- initialize from vgg16_baseline_best.pth
- use only FVEI train and validation splits during development
- keep VGG16 Blocks 1-4 frozen
- unfreeze Block 5
- train Block 5 with a lower learning rate
- train the regression head with the baseline learning rate
- optimize L1 loss / MAE
- select the best checkpoint using validation MAE
- never use the held-out FVEI test split for model selection

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import argparse
import csv
import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    IMAGE_SIZE,
    LEARNING_RATE,
    NUM_EPOCHS,
    NUM_WORKERS,
    RANDOM_SEED,
    VGG16_CHECKPOINT_PATH,
    WEIGHT_DECAY,
)
from src.training.fvei_dataloader import (
    DEFAULT_MANIFEST,
    FVEIDataset,
)
from src.training.dataloader import get_transforms
from src.training.train_vgg16 import (
    build_vgg16_regression_model,
)
from src.training.utils import set_seed


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_OUTPUT_CHECKPOINT = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_fvei_block5_best.pth"
)

DEFAULT_HISTORY_PATH = (
    PROJECT_ROOT
    / "results"
    / "fvei"
    / "vgg16_fvei_block5_history.csv"
)

DEFAULT_SUMMARY_PATH = (
    PROJECT_ROOT
    / "results"
    / "fvei"
    / "vgg16_fvei_block5_summary.json"
)

BLOCK5_START_INDEX = 24
BLOCK5_LEARNING_RATE = 1e-5
HEAD_LEARNING_RATE = LEARNING_RATE


def load_synthetic_checkpoint() -> nn.Module:
    """
    Load the selected synthetic-domain VGG16 baseline checkpoint.
    """

    if not VGG16_CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            "Synthetic VGG16 checkpoint not found: "
            f"{VGG16_CHECKPOINT_PATH}"
        )

    # No ImageNet download is needed because the complete
    # synthetic-trained state_dict is loaded immediately afterward.
    model = build_vgg16_regression_model(
        pretrained=False,
    )

    checkpoint = torch.load(
        VGG16_CHECKPOINT_PATH,
        map_location="cpu",
    )

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            "Synthetic checkpoint does not contain "
            "'model_state_dict'."
        )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    print(
        "Synthetic source checkpoint loaded:"
    )
    print(
        f"  {VGG16_CHECKPOINT_PATH}"
    )

    if "epoch" in checkpoint:
        print(
            f"  Source best epoch: "
            f"{checkpoint['epoch']}"
        )

    if "validation_mae" in checkpoint:
        print(
            f"  Source validation MAE: "
            f"{checkpoint['validation_mae']:.4f} m"
        )

    return model


def configure_block5_fine_tuning(
    model: nn.Module,
) -> None:
    """
    Freeze VGG16 Blocks 1-4 and unfreeze Block 5
    plus the regression head.
    """

    for parameter in model.features.parameters():
        parameter.requires_grad = False

    for layer in model.features[
        BLOCK5_START_INDEX:
    ]:
        for parameter in layer.parameters():
            parameter.requires_grad = True

    for parameter in model.classifier.parameters():
        parameter.requires_grad = True


def verify_trainable_parameters(
    model: nn.Module,
) -> None:
    """
    Verify the intended fine-tuning configuration.
    """

    early_parameters = [
        parameter
        for layer in model.features[
            :BLOCK5_START_INDEX
        ]
        for parameter in layer.parameters()
    ]

    block5_parameters = [
        parameter
        for layer in model.features[
            BLOCK5_START_INDEX:
        ]
        for parameter in layer.parameters()
    ]

    head_parameters = list(
        model.classifier.parameters()
    )

    if any(
        parameter.requires_grad
        for parameter in early_parameters
    ):
        raise RuntimeError(
            "VGG16 Blocks 1-4 must remain frozen."
        )

    if not block5_parameters:
        raise RuntimeError(
            "No VGG16 Block 5 parameters found."
        )

    if not all(
        parameter.requires_grad
        for parameter in block5_parameters
    ):
        raise RuntimeError(
            "All VGG16 Block 5 parameters "
            "must be trainable."
        )

    if not all(
        parameter.requires_grad
        for parameter in head_parameters
    ):
        raise RuntimeError(
            "All regression-head parameters "
            "must be trainable."
        )

    block5_values = sum(
        parameter.numel()
        for parameter in block5_parameters
        if parameter.requires_grad
    )

    head_values = sum(
        parameter.numel()
        for parameter in head_parameters
        if parameter.requires_grad
    )

    print("\n=== TRAINABLE PARAMETER CHECK ===")
    print("Blocks 1-4 frozen       : True")
    print("Block 5 trainable       : True")
    print("Regression head trainable: True")
    print(
        f"Block 5 parameters      : "
        f"{block5_values:,}"
    )
    print(
        f"Head parameters         : "
        f"{head_values:,}"
    )


def create_train_val_loaders(
    zip_path: Path,
    manifest_path: Path,
    batch_size: int,
) -> tuple[DataLoader, DataLoader]:
    """
    Create only train and validation loaders.

    The held-out test split is intentionally not instantiated
    during model development.
    """

    transform = get_transforms(
        image_size=IMAGE_SIZE,
    )

    train_dataset = FVEIDataset(
        zip_path=zip_path,
        manifest_path=manifest_path,
        split="train",
        transform=transform,
    )

    val_dataset = FVEIDataset(
        zip_path=zip_path,
        manifest_path=manifest_path,
        split="val",
        transform=transform,
    )

    generator = torch.Generator()
    generator.manual_seed(
        RANDOM_SEED
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=(
            DEVICE.type == "cuda"
        ),
        generator=generator,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(
            DEVICE.type == "cuda"
        ),
    )

    return train_loader, val_loader


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer,
) -> float:
    """
    Train one epoch and return mean MAE.
    """

    model.train()

    total_loss = 0.0
    total_samples = 0

    for images, targets in loader:
        images = images.to(
            DEVICE,
            non_blocking=True,
        )

        targets = targets.to(
            DEVICE,
            non_blocking=True,
        )

        optimizer.zero_grad()

        predictions = model(
            images
        ).squeeze(1)

        loss = loss_function(
            predictions,
            targets,
        )

        loss.backward()
        optimizer.step()

        batch_size = images.size(0)

        total_loss += (
            loss.item() * batch_size
        )

        total_samples += batch_size

    return total_loss / total_samples


def validate(
    model: nn.Module,
    loader: DataLoader,
    loss_function: nn.Module,
) -> float:
    """
    Evaluate validation MAE.
    """

    model.eval()

    total_loss = 0.0
    total_samples = 0

    with torch.no_grad():
        for images, targets in loader:
            images = images.to(
                DEVICE,
                non_blocking=True,
            )

            targets = targets.to(
                DEVICE,
                non_blocking=True,
            )

            predictions = model(
                images
            ).squeeze(1)

            loss = loss_function(
                predictions,
                targets,
            )

            batch_size = images.size(0)

            total_loss += (
                loss.item() * batch_size
            )

            total_samples += batch_size

    return total_loss / total_samples


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    train_mae: float,
    validation_mae: float,
    checkpoint_path: Path,
    manifest_path: Path,
) -> None:
    """
    Save the best validation-selected FVEI checkpoint.
    """

    checkpoint_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": (
            model.state_dict()
        ),
        "optimizer_state_dict": (
            optimizer.state_dict()
        ),
        "training_mae": train_mae,
        "validation_mae": validation_mae,
        "random_seed": RANDOM_SEED,
        "source_checkpoint": str(
            VGG16_CHECKPOINT_PATH
        ),
        "dataset": "FVEI",
        "split_manifest": str(
            manifest_path
        ),
        "fine_tuning_strategy": (
            "VGG16 Block 5 + regression head"
        ),
        "loss_function": "L1Loss",
        "frozen_blocks": (
            "VGG16 Blocks 1-4"
        ),
        "unfrozen_block": (
            "VGG16 Block 5"
        ),
        "block5_start_index": (
            BLOCK5_START_INDEX
        ),
        "block5_learning_rate": (
            BLOCK5_LEARNING_RATE
        ),
        "head_learning_rate": (
            HEAD_LEARNING_RATE
        ),
        "weight_decay": WEIGHT_DECAY,
        "test_used_for_selection": False,
    }

    torch.save(
        checkpoint,
        checkpoint_path,
    )


def save_history(
    history: list[dict],
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
                "epoch",
                "train_mae",
                "validation_mae",
            ],
        )

        writer.writeheader()
        writer.writerows(history)


def run_dry_test(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
) -> None:
    """
    Verify checkpoint and data compatibility without training.
    """

    model.eval()

    train_images, train_targets = next(
        iter(train_loader)
    )

    val_images, val_targets = next(
        iter(val_loader)
    )

    train_images = train_images.to(
        DEVICE
    )

    val_images = val_images.to(
        DEVICE
    )

    with torch.no_grad():
        train_predictions = model(
            train_images
        ).squeeze(1)

        val_predictions = model(
            val_images
        ).squeeze(1)

    print("\n=== DRY RUN SUCCESSFUL ===")
    print(
        "Train batch:",
        tuple(train_images.shape),
    )
    print(
        "Train targets:",
        tuple(train_targets.shape),
    )
    print(
        "Train predictions:",
        tuple(train_predictions.shape),
    )

    print(
        "Validation batch:",
        tuple(val_images.shape),
    )
    print(
        "Validation targets:",
        tuple(val_targets.shape),
    )
    print(
        "Validation predictions:",
        tuple(val_predictions.shape),
    )

    print(
        "\nNo optimizer step was performed."
    )
    print(
        "Held-out test split was not accessed."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
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
        "--epochs",
        type=int,
        default=NUM_EPOCHS,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=BATCH_SIZE,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
    )

    args = parser.parse_args()

    set_seed(
        RANDOM_SEED
    )

    train_loader, val_loader = (
        create_train_val_loaders(
            zip_path=args.zip_path,
            manifest_path=args.manifest,
            batch_size=args.batch_size,
        )
    )

    model = load_synthetic_checkpoint()

    configure_block5_fine_tuning(
        model
    )

    verify_trainable_parameters(
        model
    )

    model = model.to(
        DEVICE
    )

    print("\n=== FVEI FINE-TUNING SETUP ===")
    print(
        f"Device              : {DEVICE}"
    )
    print(
        f"Training samples    : "
        f"{len(train_loader.dataset)}"
    )
    print(
        f"Validation samples  : "
        f"{len(val_loader.dataset)}"
    )
    print(
        "Held-out test       : NOT ACCESSED"
    )
    print(
        f"Epochs              : "
        f"{args.epochs}"
    )
    print(
        f"Batch size          : "
        f"{args.batch_size}"
    )
    print(
        f"Block 5 LR          : "
        f"{BLOCK5_LEARNING_RATE}"
    )
    print(
        f"Regression head LR  : "
        f"{HEAD_LEARNING_RATE}"
    )
    print(
        f"Weight decay        : "
        f"{WEIGHT_DECAY}"
    )
    print(
        "Loss                : L1Loss / MAE"
    )
    print(
        f"Random seed         : "
        f"{RANDOM_SEED}"
    )

    if args.dry_run:
        run_dry_test(
            model=model,
            train_loader=train_loader,
            val_loader=val_loader,
        )

        return

    loss_function = nn.L1Loss()

    block5_parameters = [
        parameter
        for layer in model.features[
            BLOCK5_START_INDEX:
        ]
        for parameter in layer.parameters()
        if parameter.requires_grad
    ]

    head_parameters = [
        parameter
        for parameter in (
            model.classifier.parameters()
        )
        if parameter.requires_grad
    ]

    optimizer = Adam(
        [
            {
                "params": block5_parameters,
                "lr": BLOCK5_LEARNING_RATE,
            },
            {
                "params": head_parameters,
                "lr": HEAD_LEARNING_RATE,
            },
        ],
        weight_decay=WEIGHT_DECAY,
    )

    best_validation_mae = float(
        "inf"
    )

    best_epoch = 0
    history = []

    for epoch in range(
        1,
        args.epochs + 1,
    ):
        train_mae = train_one_epoch(
            model=model,
            loader=train_loader,
            loss_function=loss_function,
            optimizer=optimizer,
        )

        validation_mae = validate(
            model=model,
            loader=val_loader,
            loss_function=loss_function,
        )

        history.append(
            {
                "epoch": epoch,
                "train_mae": train_mae,
                "validation_mae": (
                    validation_mae
                ),
            }
        )

        print(
            f"Epoch "
            f"[{epoch:02d}/{args.epochs}] "
            f"| Train MAE: "
            f"{train_mae:.4f} m "
            f"| Validation MAE: "
            f"{validation_mae:.4f} m"
        )

        if (
            validation_mae
            < best_validation_mae
        ):
            best_validation_mae = (
                validation_mae
            )

            best_epoch = epoch

            save_checkpoint(
                model=model,
                optimizer=optimizer,
                epoch=epoch,
                train_mae=train_mae,
                validation_mae=(
                    validation_mae
                ),
                checkpoint_path=(
                    DEFAULT_OUTPUT_CHECKPOINT
                ),
                manifest_path=(
                    args.manifest
                ),
            )

            print(
                "  -> Best FVEI checkpoint saved."
            )

    save_history(
        history=history,
        output_path=DEFAULT_HISTORY_PATH,
    )

    summary = {
        "dataset": "FVEI",
        "source_checkpoint": str(
            VGG16_CHECKPOINT_PATH
        ),
        "output_checkpoint": str(
            DEFAULT_OUTPUT_CHECKPOINT
        ),
        "training_samples": len(
            train_loader.dataset
        ),
        "validation_samples": len(
            val_loader.dataset
        ),
        "held_out_test_samples": 482,
        "test_used_for_selection": False,
        "best_epoch": best_epoch,
        "best_validation_mae": (
            best_validation_mae
        ),
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "block5_learning_rate": (
            BLOCK5_LEARNING_RATE
        ),
        "head_learning_rate": (
            HEAD_LEARNING_RATE
        ),
        "loss_function": "L1Loss",
        "random_seed": RANDOM_SEED,
    }

    DEFAULT_SUMMARY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    DEFAULT_SUMMARY_PATH.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "\n=== FVEI FINE-TUNING COMPLETE ==="
    )
    print(
        f"Best epoch          : "
        f"{best_epoch}"
    )
    print(
        f"Best validation MAE : "
        f"{best_validation_mae:.4f} m"
    )
    print(
        f"Checkpoint          : "
        f"{DEFAULT_OUTPUT_CHECKPOINT}"
    )
    print(
        "\nHeld-out test split remains untouched."
    )


if __name__ == "__main__":
    main()
