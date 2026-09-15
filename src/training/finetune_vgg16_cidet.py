"""
finetune_vgg16_cidet.py

Fine-tune the synthetic-trained VGG16 regression baseline on the
CIDET real-world training split.

Protocol:
- initialize from synthetic VGG16 checkpoint
- keep convolutional backbone frozen
- train regression head only
- select best checkpoint using CIDET validation MAE
- do not evaluate on the test split during training

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader

from src.training.cidet_dataloader import (
    create_cidet_dataloaders,
)
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
from src.training.train_vgg16 import (
    build_vgg16_regression_model,
)
from src.training.utils import set_seed


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CIDET_CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_cidet_finetuned_best.pth"
)


def load_synthetic_checkpoint() -> nn.Module:
    """
    Build the VGG16 regression model and initialize it from the
    best synthetic-domain checkpoint.
    """
    if not VGG16_CHECKPOINT_PATH.exists():
        raise FileNotFoundError(
            "Synthetic VGG16 checkpoint not found: "
            f"{VGG16_CHECKPOINT_PATH}"
        )

    model = (
        build_vgg16_regression_model()
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
        checkpoint[
            "model_state_dict"
        ]
    )

    return model


def verify_trainable_parameters(
    model: nn.Module,
) -> None:
    """
    Confirm that the convolutional backbone is frozen and that the
    regression head remains trainable.
    """
    feature_parameters = list(
        model.features.parameters()
    )

    classifier_parameters = list(
        model.classifier.parameters()
    )

    frozen_feature_count = sum(
        not parameter.requires_grad
        for parameter
        in feature_parameters
    )

    trainable_feature_count = sum(
        parameter.requires_grad
        for parameter
        in feature_parameters
    )

    trainable_classifier_count = sum(
        parameter.requires_grad
        for parameter
        in classifier_parameters
    )

    if trainable_feature_count != 0:
        raise RuntimeError(
            "VGG16 convolutional backbone is not fully frozen."
        )

    if trainable_classifier_count == 0:
        raise RuntimeError(
            "Regression head has no trainable parameters."
        )

    print(
        "\n--- TRAINABLE PARAMETER CHECK ---"
    )

    print(
        "Frozen feature parameter tensors: "
        f"{frozen_feature_count}"
    )

    print(
        "Trainable feature parameter tensors: "
        f"{trainable_feature_count}"
    )

    print(
        "Trainable classifier parameter tensors: "
        f"{trainable_classifier_count}"
    )


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    loss_function: nn.Module,
    optimizer: torch.optim.Optimizer,
) -> float:
    """
    Train for one epoch and return mean MAE.
    """
    model.train()

    running_loss = 0.0
    total_samples = 0

    for images, targets in dataloader:
        images = images.to(
            DEVICE
        )

        targets = targets.to(
            DEVICE
        )

        optimizer.zero_grad()

        predictions = (
            model(images)
            .squeeze(1)
        )

        loss = loss_function(
            predictions,
            targets,
        )

        loss.backward()

        optimizer.step()

        batch_size = images.size(
            0
        )

        running_loss += (
            loss.item()
            * batch_size
        )

        total_samples += (
            batch_size
        )

    return (
        running_loss
        / total_samples
    )


def validate_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    loss_function: nn.Module,
) -> float:
    """
    Evaluate on the validation set and return mean MAE.
    """
    model.eval()

    running_loss = 0.0
    total_samples = 0

    with torch.no_grad():
        for images, targets in dataloader:
            images = images.to(
                DEVICE
            )

            targets = targets.to(
                DEVICE
            )

            predictions = (
                model(images)
                .squeeze(1)
            )

            loss = loss_function(
                predictions,
                targets,
            )

            batch_size = (
                images.size(0)
            )

            running_loss += (
                loss.item()
                * batch_size
            )

            total_samples += (
                batch_size
            )

    return (
        running_loss
        / total_samples
    )


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    validation_mae: float,
    training_mae: float,
) -> None:
    """
    Save the best CIDET-adapted model.
    """
    CIDET_CHECKPOINT_PATH.parent.mkdir(
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
        "training_mae": (
            training_mae
        ),
        "validation_mae": (
            validation_mae
        ),
        "random_seed": (
            RANDOM_SEED
        ),
        "source_checkpoint": str(
            VGG16_CHECKPOINT_PATH
        ),
        "dataset": "CIDET",
        "split": (
            "calendar-day-grouped temporal split"
        ),
        "backbone_frozen": True,
    }

    torch.save(
        checkpoint,
        CIDET_CHECKPOINT_PATH,
    )


def main() -> None:
    set_seed(
        RANDOM_SEED
    )

    (
        train_loader,
        validation_loader,
        _,
    ) = (
        create_cidet_dataloaders(
            batch_size=BATCH_SIZE,
            num_workers=NUM_WORKERS,
            random_seed=RANDOM_SEED,
            pin_memory=(
                DEVICE.type == "cuda"
            ),
        )
    )

    model = (
        load_synthetic_checkpoint()
    )

    verify_trainable_parameters(
        model
    )

    model = model.to(
        DEVICE
    )

    loss_function = (
        nn.L1Loss()
    )

    trainable_parameters = [
        parameter
        for parameter
        in model.parameters()
        if parameter.requires_grad
    ]

    optimizer = Adam(
        trainable_parameters,
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
    )

    best_validation_mae = float(
        "inf"
    )

    best_epoch = 0

    print(
        "\n=== CIDET VGG16 FINE-TUNING ==="
    )

    print(
        f"Device:              {DEVICE}"
    )

    print(
        f"Training samples:    "
        f"{len(train_loader.dataset)}"
    )

    print(
        f"Validation samples:  "
        f"{len(validation_loader.dataset)}"
    )

    print(
        f"Epochs:              {NUM_EPOCHS}"
    )

    print(
        f"Learning rate:       {LEARNING_RATE}"
    )

    print(
        f"Weight decay:        {WEIGHT_DECAY}"
    )

    print(
        f"Source checkpoint:   "
        f"{VGG16_CHECKPOINT_PATH}"
    )

    print(
        f"Output checkpoint:   "
        f"{CIDET_CHECKPOINT_PATH}"
    )

    print(
        "Backbone frozen:     True"
    )

    print(
        "\nIMPORTANT:"
    )

    print(
        "CIDET test split is not used "
        "during training or model selection."
    )

    for epoch in range(
        1,
        NUM_EPOCHS + 1,
    ):
        training_mae = (
            train_one_epoch(
                model=model,
                dataloader=train_loader,
                loss_function=loss_function,
                optimizer=optimizer,
            )
        )

        validation_mae = (
            validate_one_epoch(
                model=model,
                dataloader=validation_loader,
                loss_function=loss_function,
            )
        )

        print(
            f"Epoch "
            f"[{epoch:02d}/{NUM_EPOCHS}] "
            f"| Train MAE: "
            f"{training_mae:.4f} m "
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
                validation_mae=(
                    validation_mae
                ),
                training_mae=(
                    training_mae
                ),
            )

            print(
                "  -> Best CIDET checkpoint saved."
            )

    print(
        "\n=== FINE-TUNING COMPLETE ==="
    )

    print(
        f"Best epoch:          "
        f"{best_epoch}"
    )

    print(
        f"Best validation MAE: "
        f"{best_validation_mae:.4f} m"
    )

    print(
        f"Checkpoint:          "
        f"{CIDET_CHECKPOINT_PATH}"
    )

    print(
        "\nTest split remains untouched."
    )


if __name__ == "__main__":
    main()