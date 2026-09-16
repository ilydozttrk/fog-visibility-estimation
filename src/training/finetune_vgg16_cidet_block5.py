"""
finetune_vgg16_cidet_block5.py

Gradually fine-tune the synthetic-trained VGG16 regression model
on the CIDET real-world training split.

Protocol:
- initialize from the synthetic VGG16 checkpoint
- keep VGG16 convolutional Blocks 1-4 frozen
- unfreeze convolutional Block 5
- train Block 5 with a lower learning rate
- train the regression head with the baseline learning rate
- select the best checkpoint using CIDET validation MAE
- never use the CIDET test split during training or model selection

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from src.training.cidet_dataloader import create_cidet_dataloaders
from src.training.config import (
    BATCH_SIZE,
    DEVICE,
    LEARNING_RATE,
    NUM_EPOCHS,
    NUM_WORKERS,
    RANDOM_SEED,
    VGG16_CHECKPOINT_PATH,
    WEIGHT_DECAY,
)
from src.training.train_vgg16 import build_vgg16_regression_model
from src.training.utils import set_seed


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CIDET_BLOCK5_CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_cidet_block5_finetuned_best.pth"
)

BLOCK5_START_INDEX = 24
BLOCK5_LEARNING_RATE = 1e-5
HEAD_LEARNING_RATE = LEARNING_RATE


def load_synthetic_checkpoint() -> nn.Module:
    """Load the synthetic-domain VGG16 regression checkpoint."""
    if not VGG16_CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            "Synthetic VGG16 checkpoint not found: "
            f"{VGG16_CHECKPOINT_PATH}"
        )

    model = build_vgg16_regression_model()

    checkpoint = torch.load(
        VGG16_CHECKPOINT_PATH,
        map_location="cpu",
    )

    if "model_state_dict" not in checkpoint:
        raise KeyError(
            "Synthetic checkpoint does not contain "
            "'model_state_dict'."
        )

    model.load_state_dict(checkpoint["model_state_dict"])

    return model


def configure_block5_fine_tuning(model: nn.Module) -> None:
    """
    Freeze Blocks 1-4 and unfreeze VGG16 Block 5.

    In torchvision VGG16, Block 5 begins at features[24].
    The regression classifier remains trainable.
    """
    for parameter in model.features.parameters():
        parameter.requires_grad = False

    for layer in model.features[BLOCK5_START_INDEX:]:
        for parameter in layer.parameters():
            parameter.requires_grad = True

    for parameter in model.classifier.parameters():
        parameter.requires_grad = True


def verify_trainable_parameters(model: nn.Module) -> None:
    """Verify the intended gradual fine-tuning configuration."""
    frozen_early_parameters = [
        parameter
        for layer in model.features[:BLOCK5_START_INDEX]
        for parameter in layer.parameters()
    ]

    block5_parameters = [
        parameter
        for layer in model.features[BLOCK5_START_INDEX:]
        for parameter in layer.parameters()
    ]

    classifier_parameters = list(model.classifier.parameters())

    if any(
        parameter.requires_grad
        for parameter in frozen_early_parameters
    ):
        raise RuntimeError(
            "A parameter in VGG16 Blocks 1-4 is unexpectedly trainable."
        )

    if not block5_parameters:
        raise RuntimeError(
            "No parameters were found in VGG16 Block 5."
        )

    if not all(
        parameter.requires_grad
        for parameter in block5_parameters
    ):
        raise RuntimeError(
            "Not all VGG16 Block 5 parameters are trainable."
        )

    if not all(
        parameter.requires_grad
        for parameter in classifier_parameters
    ):
        raise RuntimeError(
            "Not all regression-head parameters are trainable."
        )

    frozen_early_count = sum(
        not parameter.requires_grad
        for parameter in frozen_early_parameters
    )

    trainable_block5_count = sum(
        parameter.requires_grad
        for parameter in block5_parameters
    )

    trainable_classifier_count = sum(
        parameter.requires_grad
        for parameter in classifier_parameters
    )

    trainable_block5_values = sum(
        parameter.numel()
        for parameter in block5_parameters
        if parameter.requires_grad
    )

    trainable_classifier_values = sum(
        parameter.numel()
        for parameter in classifier_parameters
        if parameter.requires_grad
    )

    print("\n--- TRAINABLE PARAMETER CHECK ---")
    print(
        "Frozen Blocks 1-4 parameter tensors: "
        f"{frozen_early_count}"
    )
    print(
        "Trainable Block 5 parameter tensors: "
        f"{trainable_block5_count}"
    )
    print(
        "Trainable classifier parameter tensors: "
        f"{trainable_classifier_count}"
    )
    print(
        "Trainable Block 5 parameters: "
        f"{trainable_block5_values:,}"
    )
    print(
        "Trainable classifier parameters: "
        f"{trainable_classifier_values:,}"
    )


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer,
) -> float:
    """Train for one epoch and return mean MAE."""
    model.train()

    running_loss = 0.0
    total_samples = 0

    for images, targets in dataloader:
        images = images.to(DEVICE)
        targets = targets.to(DEVICE)

        optimizer.zero_grad()

        predictions = model(images).squeeze(1)

        loss = loss_function(
            predictions,
            targets,
        )

        loss.backward()
        optimizer.step()

        batch_size = images.size(0)

        running_loss += loss.item() * batch_size
        total_samples += batch_size

    return running_loss / total_samples


def validate_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    loss_function: nn.Module,
) -> float:
    """Evaluate on validation data and return mean MAE."""
    model.eval()

    running_loss = 0.0
    total_samples = 0

    with torch.no_grad():
        for images, targets in dataloader:
            images = images.to(DEVICE)
            targets = targets.to(DEVICE)

            predictions = model(images).squeeze(1)

            loss = loss_function(
                predictions,
                targets,
            )

            batch_size = images.size(0)

            running_loss += loss.item() * batch_size
            total_samples += batch_size

    return running_loss / total_samples


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    validation_mae: float,
    training_mae: float,
) -> None:
    """Save the best validation-selected Block 5 checkpoint."""
    CIDET_BLOCK5_CHECKPOINT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "training_mae": training_mae,
        "validation_mae": validation_mae,
        "random_seed": RANDOM_SEED,
        "source_checkpoint": str(VGG16_CHECKPOINT_PATH),
        "dataset": "CIDET",
        "split": "calendar-day-grouped temporal split",
        "fine_tuning_strategy": "VGG16 Block 5 + regression head",
        "backbone_frozen": False,
        "frozen_blocks": "VGG16 Blocks 1-4",
        "unfrozen_block": "VGG16 Block 5",
        "block5_start_index": BLOCK5_START_INDEX,
        "block5_learning_rate": BLOCK5_LEARNING_RATE,
        "head_learning_rate": HEAD_LEARNING_RATE,
        "test_used_for_selection": False,
    }

    torch.save(
        checkpoint,
        CIDET_BLOCK5_CHECKPOINT_PATH,
    )


def main() -> None:
    set_seed(RANDOM_SEED)

    (
        train_loader,
        validation_loader,
        _,
    ) = create_cidet_dataloaders(
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        random_seed=RANDOM_SEED,
        pin_memory=(DEVICE.type == "cuda"),
    )

    model = load_synthetic_checkpoint()

    configure_block5_fine_tuning(model)
    verify_trainable_parameters(model)

    model = model.to(DEVICE)

    loss_function = nn.L1Loss()

    block5_parameters = [
        parameter
        for layer in model.features[BLOCK5_START_INDEX:]
        for parameter in layer.parameters()
        if parameter.requires_grad
    ]

    classifier_parameters = [
        parameter
        for parameter in model.classifier.parameters()
        if parameter.requires_grad
    ]

    optimizer = Adam(
        [
            {
                "params": block5_parameters,
                "lr": BLOCK5_LEARNING_RATE,
            },
            {
                "params": classifier_parameters,
                "lr": HEAD_LEARNING_RATE,
            },
        ],
        weight_decay=WEIGHT_DECAY,
    )

    best_validation_mae = float("inf")
    best_epoch = 0

    print("\n=== CIDET VGG16 BLOCK 5 FINE-TUNING ===")
    print(f"Device:              {DEVICE}")
    print(
        f"Training samples:    "
        f"{len(train_loader.dataset)}"
    )
    print(
        f"Validation samples:  "
        f"{len(validation_loader.dataset)}"
    )
    print(f"Epochs:              {NUM_EPOCHS}")
    print(
        f"Block 5 LR:          "
        f"{BLOCK5_LEARNING_RATE}"
    )
    print(
        f"Regression head LR:  "
        f"{HEAD_LEARNING_RATE}"
    )
    print(f"Weight decay:        {WEIGHT_DECAY}")
    print(
        f"Source checkpoint:   "
        f"{VGG16_CHECKPOINT_PATH}"
    )
    print(
        f"Output checkpoint:   "
        f"{CIDET_BLOCK5_CHECKPOINT_PATH}"
    )
    print("Blocks 1-4 frozen:   True")
    print("Block 5 trainable:   True")

    print("\nIMPORTANT:")
    print(
        "CIDET test split is not used during "
        "training or model selection."
    )

    for epoch in range(1, NUM_EPOCHS + 1):
        training_mae = train_one_epoch(
            model=model,
            dataloader=train_loader,
            loss_function=loss_function,
            optimizer=optimizer,
        )

        validation_mae = validate_one_epoch(
            model=model,
            dataloader=validation_loader,
            loss_function=loss_function,
        )

        print(
            f"Epoch [{epoch:02d}/{NUM_EPOCHS}] "
            f"| Train MAE: {training_mae:.4f} m "
            f"| Validation MAE: {validation_mae:.4f} m"
        )

        if validation_mae < best_validation_mae:
            best_validation_mae = validation_mae
            best_epoch = epoch

            save_checkpoint(
                model=model,
                optimizer=optimizer,
                epoch=epoch,
                validation_mae=validation_mae,
                training_mae=training_mae,
            )

            print(
                "  -> Best Block 5 checkpoint saved."
            )

    print("\n=== BLOCK 5 FINE-TUNING COMPLETE ===")
    print(f"Best epoch:          {best_epoch}")
    print(
        f"Best validation MAE: "
        f"{best_validation_mae:.4f} m"
    )
    print(
        f"Checkpoint:          "
        f"{CIDET_BLOCK5_CHECKPOINT_PATH}"
    )
    print("\nTest split remains untouched.")


if __name__ == "__main__":
    main()
