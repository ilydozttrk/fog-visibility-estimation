"""
train_vgg16.py

Training pipeline for the pretrained VGG16 baseline model
used in fog visibility regression.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader
from torchvision.models import VGG16_Weights, vgg16

from src.training.config import (
    BATCH_SIZE,
    CHECKPOINTS_DIR,
    DEVICE,
    DROPOUT_RATE,
    FREEZE_BACKBONE,
    IMAGE_SIZE,
    LEARNING_RATE,
    NUM_EPOCHS,
    NUM_WORKERS,
    RANDOM_SEED,
    REGRESSION_HIDDEN_DIM_1,
    REGRESSION_HIDDEN_DIM_2,
    TEST_RATIO,
    TRAIN_RATIO,
    VAL_RATIO,
    VGG16_CHECKPOINT_PATH,
    WEIGHT_DECAY,
    create_output_directories,
)
from src.training.dataloader import create_dataloaders
from src.training.utils import set_seed


# =============================================================================
# Model
# =============================================================================

def build_vgg16_regression_model() -> nn.Module:
    """
    Load an ImageNet-pretrained VGG16 model and replace its
    classification head with a regression head.
    """

    weights = VGG16_Weights.DEFAULT
    model = vgg16(weights=weights)

    if FREEZE_BACKBONE:
        for parameter in model.features.parameters():
            parameter.requires_grad = False

    input_features = model.classifier[0].in_features

    model.classifier = nn.Sequential(
        nn.Linear(input_features, REGRESSION_HIDDEN_DIM_1),
        nn.ReLU(inplace=True),
        nn.Dropout(DROPOUT_RATE),
        nn.Linear(
            REGRESSION_HIDDEN_DIM_1,
            REGRESSION_HIDDEN_DIM_2,
        ),
        nn.ReLU(inplace=True),
        nn.Dropout(DROPOUT_RATE),
        nn.Linear(REGRESSION_HIDDEN_DIM_2, 1),
    )

    return model


# =============================================================================
# Training
# =============================================================================

def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    """
    Train the model for one epoch and return mean training MAE.
    """

    model.train()

    running_loss = 0.0
    total_samples = 0

    for images, targets in dataloader:
        images = images.to(device)
        targets = targets.to(device)

        optimizer.zero_grad()

        predictions = model(images).squeeze(1)

        loss = loss_function(predictions, targets)

        loss.backward()
        optimizer.step()

        batch_size = images.size(0)

        running_loss += loss.item() * batch_size
        total_samples += batch_size

    mean_loss = running_loss / total_samples

    return mean_loss


# =============================================================================
# Validation
# =============================================================================

def validate_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    loss_function: nn.Module,
    device: torch.device,
) -> float:
    """
    Evaluate the model and return mean validation MAE.
    """

    model.eval()

    running_loss = 0.0
    total_samples = 0

    with torch.no_grad():
        for images, targets in dataloader:
            images = images.to(device)
            targets = targets.to(device)

            predictions = model(images).squeeze(1)

            loss = loss_function(predictions, targets)

            batch_size = images.size(0)

            running_loss += loss.item() * batch_size
            total_samples += batch_size

    mean_loss = running_loss / total_samples

    return mean_loss


# =============================================================================
# Checkpoint
# =============================================================================

def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    validation_mae: float,
    checkpoint_path: Path,
) -> None:
    """
    Save the best model checkpoint and related training state.
    """

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "validation_mae": validation_mae,
        "random_seed": RANDOM_SEED,
    }

    torch.save(checkpoint, checkpoint_path)


# =============================================================================
# Training Pipeline
# =============================================================================

def train_model() -> None:
    """
    Run the complete VGG16 baseline training pipeline.
    """

    set_seed(RANDOM_SEED)
    create_output_directories()

    pin_memory = DEVICE.type == "cuda"

    train_loader, val_loader, _ = create_dataloaders(
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        num_workers=NUM_WORKERS,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        random_seed=RANDOM_SEED,
        pin_memory=pin_memory,
    )

    model = build_vgg16_regression_model()
    model = model.to(DEVICE)

    loss_function = nn.L1Loss()

    trainable_parameters = [
        parameter
        for parameter in model.parameters()
        if parameter.requires_grad
    ]

    optimizer = Adam(
        trainable_parameters,
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
    )

    best_validation_mae = float("inf")

    print("=" * 70)
    print("VGG16 Fog Visibility Regression Training")
    print("=" * 70)
    print(f"Device                : {DEVICE}")
    print(f"Training images       : {len(train_loader.dataset)}")
    print(f"Validation images     : {len(val_loader.dataset)}")
    print(f"Batch size            : {BATCH_SIZE}")
    print(f"Epochs                : {NUM_EPOCHS}")
    print(f"Learning rate         : {LEARNING_RATE}")
    print(f"Random seed           : {RANDOM_SEED}")
    print(f"Frozen backbone       : {FREEZE_BACKBONE}")
    print(f"Checkpoint path       : {VGG16_CHECKPOINT_PATH}")
    print("=" * 70)

    for epoch in range(1, NUM_EPOCHS + 1):
        training_mae = train_one_epoch(
            model=model,
            dataloader=train_loader,
            loss_function=loss_function,
            optimizer=optimizer,
            device=DEVICE,
        )

        validation_mae = validate_one_epoch(
            model=model,
            dataloader=val_loader,
            loss_function=loss_function,
            device=DEVICE,
        )

        print(
            f"Epoch [{epoch:02d}/{NUM_EPOCHS}] "
            f"| Train MAE: {training_mae:.4f} m "
            f"| Validation MAE: {validation_mae:.4f} m"
        )

        if validation_mae < best_validation_mae:
            best_validation_mae = validation_mae

            save_checkpoint(
                model=model,
                optimizer=optimizer,
                epoch=epoch,
                validation_mae=validation_mae,
                checkpoint_path=VGG16_CHECKPOINT_PATH,
            )

            print(
                "  -> Best checkpoint saved "
                f"(Validation MAE: {best_validation_mae:.4f} m)"
            )

    print("=" * 70)
    print("Training completed.")
    print(f"Best validation MAE: {best_validation_mae:.4f} m")
    print(f"Best model saved to: {VGG16_CHECKPOINT_PATH}")
    print("=" * 70)


def main() -> None:
    train_model()


if __name__ == "__main__":
    main()