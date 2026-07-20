"""
dataloader.py

PyTorch Dataset and DataLoader implementation for
Fog Visibility Estimation.

The dataset is divided at scene level to prevent images generated
from the same base scene from appearing in different data subsets.

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


# =============================================================================
# Configuration
# =============================================================================

DATA_ROOT = Path("data/generated")
CSV_PATH = DATA_ROOT / "labels.csv"


# =============================================================================
# Image Transform
# =============================================================================

def get_transforms(image_size: int = 224) -> transforms.Compose:
    """
    Return ImageNet-compatible preprocessing transformations.

    These transformations are compatible with pretrained
    VGG16 and ResNet50 models.
    """

    return transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


# =============================================================================
# Dataset
# =============================================================================

class FogVisibilityDataset(Dataset):
    """
    Dataset class for fog visibility estimation.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        data_root: Path = DATA_ROOT,
        transform: Optional[transforms.Compose] = None,
    ) -> None:
        self.data = dataframe.reset_index(drop=True)
        self.data_root = data_root
        self.transform = transform

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        row = self.data.iloc[index]

        image_path = self.data_root / row["filename"]

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        with Image.open(image_path) as image_file:
            image = image_file.convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        visibility = torch.tensor(
            row["visibility_m"],
            dtype=torch.float32,
        )

        return image, visibility


# =============================================================================
# Scene-Based Dataset Split
# =============================================================================

def split_dataframe_by_scene(
    csv_path: Path = CSV_PATH,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split the metadata into train, validation, and test sets by scene.

    All visibility variants derived from the same base scene remain
    within the same subset, preventing data leakage.
    """

    ratio_sum = train_ratio + val_ratio + test_ratio

    if abs(ratio_sum - 1.0) > 1e-8:
        raise ValueError(
            "TRAIN_RATIO, VAL_RATIO and TEST_RATIO must sum to 1.0."
        )

    dataframe = pd.read_csv(csv_path)

    required_columns = {
        "filename",
        "visibility_m",
        "scene_id",
        "source_dataset",
    }

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns in labels.csv: {sorted(missing_columns)}"
        )

    # A numeric scene_id may occur in both FRIDA and FRIDA2.
    # Therefore, source_dataset and scene_id are combined.
    dataframe["scene_key"] = (
        dataframe["source_dataset"].astype(str)
        + "_"
        + dataframe["scene_id"].astype(str)
    )

    unique_scenes = dataframe["scene_key"].drop_duplicates()

    shuffled_scenes = unique_scenes.sample(
        frac=1.0,
        random_state=random_seed,
    ).tolist()

    total_scenes = len(shuffled_scenes)

    train_end = int(total_scenes * train_ratio)
    val_end = train_end + int(total_scenes * val_ratio)

    train_scenes = set(shuffled_scenes[:train_end])
    val_scenes = set(shuffled_scenes[train_end:val_end])
    test_scenes = set(shuffled_scenes[val_end:])

    train_dataframe = dataframe[
        dataframe["scene_key"].isin(train_scenes)
    ].copy()

    val_dataframe = dataframe[
        dataframe["scene_key"].isin(val_scenes)
    ].copy()

    test_dataframe = dataframe[
        dataframe["scene_key"].isin(test_scenes)
    ].copy()

    return train_dataframe, val_dataframe, test_dataframe


# =============================================================================
# DataLoader Factory
# =============================================================================

def create_dataloaders(
    image_size: int = 224,
    batch_size: int = 16,
    num_workers: int = 0,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_seed: int = 42,
    pin_memory: bool = False,
) -> tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create reproducible train, validation, and test DataLoaders.
    """

    train_dataframe, val_dataframe, test_dataframe = (
        split_dataframe_by_scene(
            train_ratio=train_ratio,
            val_ratio=val_ratio,
            test_ratio=test_ratio,
            random_seed=random_seed,
        )
    )

    transform = get_transforms(image_size=image_size)

    train_dataset = FogVisibilityDataset(
        dataframe=train_dataframe,
        transform=transform,
    )

    val_dataset = FogVisibilityDataset(
        dataframe=val_dataframe,
        transform=transform,
    )

    test_dataset = FogVisibilityDataset(
        dataframe=test_dataframe,
        transform=transform,
    )

    generator = torch.Generator()
    generator.manual_seed(random_seed)

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
        generator=generator,
    )

    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    return train_loader, val_loader, test_loader


# =============================================================================
# Test
# =============================================================================

def main() -> None:
    train_loader, val_loader, test_loader = create_dataloaders()

    print("=" * 60)
    print("Fog Visibility DataLoader Test")
    print("=" * 60)

    print(f"Train images     : {len(train_loader.dataset)}")
    print(f"Validation images: {len(val_loader.dataset)}")
    print(f"Test images      : {len(test_loader.dataset)}")

    train_images, train_labels = next(iter(train_loader))

    print(f"\nTrain image batch shape: {train_images.shape}")
    print(f"Train label shape      : {train_labels.shape}")

    print(f"\nMinimum visibility: {train_labels.min().item():.2f} m")
    print(f"Maximum visibility: {train_labels.max().item():.2f} m")

    print("\nScene-based DataLoaders created successfully.")


if __name__ == "__main__":
    main()