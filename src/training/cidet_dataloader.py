"""
cidet_dataloader.py

PyTorch Dataset and DataLoader implementation for CIDET real-world
visibility estimation.

Uses the leakage-resistant calendar-day-grouped temporal split:

- train.csv
- validation.csv
- test.csv

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from pathlib import Path
from typing import Optional

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from src.training.config import (
    BATCH_SIZE,
    IMAGE_SIZE,
    NUM_WORKERS,
    RANDOM_SEED,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CIDET_INTERIM_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "cidet"
)

CIDET_SPLIT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cidet"
    / "temporal_split"
)

TRAIN_CSV = (
    CIDET_SPLIT_DIR
    / "train.csv"
)

VALIDATION_CSV = (
    CIDET_SPLIT_DIR
    / "validation.csv"
)

TEST_CSV = (
    CIDET_SPLIT_DIR
    / "test.csv"
)


def get_cidet_transforms(
    image_size: int = IMAGE_SIZE,
) -> transforms.Compose:
    """
    Return ImageNet-compatible preprocessing.

    The preprocessing is intentionally identical to the synthetic
    VGG16/ResNet50 experiments so that transfer-learning conditions
    remain consistent.
    """
    return transforms.Compose(
        [
            transforms.Resize(
                (
                    image_size,
                    image_size,
                )
            ),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[
                    0.485,
                    0.456,
                    0.406,
                ],
                std=[
                    0.229,
                    0.224,
                    0.225,
                ],
            ),
        ]
    )


def build_image_index() -> dict[str, Path]:
    """
    Build a filename -> image path index once.

    This avoids recursively searching the CIDET directory for every
    sample during training.
    """
    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
    }

    image_paths = [
        path
        for path in CIDET_INTERIM_DIR.rglob("*")
        if (
            path.is_file()
            and path.suffix.lower()
            in image_extensions
        )
    ]

    if not image_paths:
        raise FileNotFoundError(
            "No CIDET images found under: "
            f"{CIDET_INTERIM_DIR}"
        )

    image_index: dict[str, Path] = {}

    duplicates = []

    for image_path in image_paths:
        filename = image_path.name

        if filename in image_index:
            duplicates.append(
                filename
            )
        else:
            image_index[
                filename
            ] = image_path

    if duplicates:
        raise RuntimeError(
            "Duplicate CIDET image filenames detected: "
            f"{sorted(set(duplicates))[:10]}"
        )

    return image_index


class CIDETVisibilityDataset(Dataset):
    """
    CIDET real-world visibility regression dataset.
    """

    TARGET_COLUMN = (
        "visibility estimation average"
    )

    def __init__(
        self,
        csv_path: Path,
        image_index: dict[str, Path],
        transform: Optional[
            transforms.Compose
        ] = None,
    ) -> None:
        if not csv_path.exists():
            raise FileNotFoundError(
                f"CIDET split CSV not found: {csv_path}"
            )

        self.data = pd.read_csv(
            csv_path
        )

        required_columns = {
            "image_name",
            self.TARGET_COLUMN,
            "date",
        }

        missing_columns = (
            required_columns
            - set(
                self.data.columns
            )
        )

        if missing_columns:
            raise ValueError(
                "Missing CIDET columns: "
                f"{sorted(missing_columns)}"
            )

        self.image_index = (
            image_index
        )

        self.transform = transform

        missing_images = [
            filename
            for filename
            in self.data[
                "image_name"
            ].astype(str)
            if filename
            not in self.image_index
        ]

        if missing_images:
            raise FileNotFoundError(
                "CIDET split references missing images: "
                f"{missing_images[:10]}"
            )

    def __len__(self) -> int:
        return len(
            self.data
        )

    def __getitem__(
        self,
        index: int,
    ) -> tuple[
        torch.Tensor,
        torch.Tensor,
    ]:
        row = self.data.iloc[
            index
        ]

        filename = str(
            row[
                "image_name"
            ]
        )

        image_path = (
            self.image_index[
                filename
            ]
        )

        with Image.open(
            image_path
        ) as image_file:
            image = (
                image_file
                .convert("RGB")
            )

        if self.transform is not None:
            image = self.transform(
                image
            )

        visibility = torch.tensor(
            float(
                row[
                    self.TARGET_COLUMN
                ]
            ),
            dtype=torch.float32,
        )

        return (
            image,
            visibility,
        )


def create_cidet_dataloaders(
    image_size: int = IMAGE_SIZE,
    batch_size: int = BATCH_SIZE,
    num_workers: int = NUM_WORKERS,
    random_seed: int = RANDOM_SEED,
    pin_memory: bool = False,
) -> tuple[
    DataLoader,
    DataLoader,
    DataLoader,
]:
    """
    Create CIDET temporal train, validation and test DataLoaders.
    """
    image_index = (
        build_image_index()
    )

    transform = (
        get_cidet_transforms(
            image_size=image_size
        )
    )

    train_dataset = (
        CIDETVisibilityDataset(
            csv_path=TRAIN_CSV,
            image_index=image_index,
            transform=transform,
        )
    )

    validation_dataset = (
        CIDETVisibilityDataset(
            csv_path=VALIDATION_CSV,
            image_index=image_index,
            transform=transform,
        )
    )

    test_dataset = (
        CIDETVisibilityDataset(
            csv_path=TEST_CSV,
            image_index=image_index,
            transform=transform,
        )
    )

    generator = (
        torch.Generator()
    )

    generator.manual_seed(
        random_seed
    )

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
        generator=generator,
    )

    validation_loader = (
        DataLoader(
            dataset=validation_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=pin_memory,
        )
    )

    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    return (
        train_loader,
        validation_loader,
        test_loader,
    )


def main() -> None:
    (
        train_loader,
        validation_loader,
        test_loader,
    ) = create_cidet_dataloaders()

    print(
        "\n=== CIDET DATALOADER TEST ==="
    )

    print(
        f"Train samples:      "
        f"{len(train_loader.dataset)}"
    )

    print(
        f"Validation samples: "
        f"{len(validation_loader.dataset)}"
    )

    print(
        f"Test samples:       "
        f"{len(test_loader.dataset)}"
    )

    images, targets = next(
        iter(
            train_loader
        )
    )

    print(
        "\n--- FIRST TRAIN BATCH ---"
    )

    print(
        f"Image tensor shape: "
        f"{images.shape}"
    )

    print(
        f"Target tensor shape: "
        f"{targets.shape}"
    )

    print(
        f"Target minimum: "
        f"{targets.min().item():.4f} m"
    )

    print(
        f"Target maximum: "
        f"{targets.max().item():.4f} m"
    )

    expected_counts = (
        685,
        147,
        145,
    )

    actual_counts = (
        len(
            train_loader.dataset
        ),
        len(
            validation_loader.dataset
        ),
        len(
            test_loader.dataset
        ),
    )

    if (
        actual_counts
        != expected_counts
    ):
        raise ValueError(
            "Unexpected CIDET temporal "
            "split counts. "
            f"Expected {expected_counts}, "
            f"found {actual_counts}."
        )

    print(
        "\nCIDET temporal DataLoaders "
        "created successfully."
    )

    print(
        "=== TEST COMPLETE ==="
    )


if __name__ == "__main__":
    main()