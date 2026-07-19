"""
dataloader.py

PyTorch Dataset and DataLoader implementation for
Fog Visibility Estimation.

Author: Ilayda Ozturk
Project: TÜBİTAK 2209-A
"""

from pathlib import Path

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

# =============================================================================
# Configuration
# =============================================================================

IMAGE_SIZE = 224
BATCH_SIZE = 16

DATA_ROOT = Path("data/generated")
CSV_PATH = DATA_ROOT / "labels.csv"


# =============================================================================
# Image Transform
# =============================================================================

def get_transforms():
    """
    ImageNet preprocessing for transfer learning models.
    Compatible with VGG16 and ResNet50.
    """

    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


# =============================================================================
# Dataset
# =============================================================================

class FogVisibilityDataset(Dataset):
    """
    Dataset class for fog visibility estimation.
    """

    def __init__(self, csv_file=CSV_PATH, transform=None):

        self.data = pd.read_csv(csv_file)

        self.transform = transform

    def __len__(self):

        return len(self.data)

    def __getitem__(self, index):

        row = self.data.iloc[index]

        image_path = DATA_ROOT / row["filename"]

        image = Image.open(image_path).convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        visibility = torch.tensor(
            row["visibility_m"],
            dtype=torch.float32
        )

        return image, visibility


# =============================================================================
# DataLoader Factory
# =============================================================================

def create_dataloader(
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0):

    dataset = FogVisibilityDataset(
        transform=get_transforms()
    )

    loader = DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=True
    )

    return loader


# =============================================================================
# Test
# =============================================================================

def main():

    loader = create_dataloader()

    print("=" * 60)
    print("Fog Visibility DataLoader Test")
    print("=" * 60)

    print(f"Dataset Size : {len(loader.dataset)}")

    images, labels = next(iter(loader))

    print(f"\nImage Batch Shape : {images.shape}")
    print(f"Label Shape       : {labels.shape}")

    print("\nLabels")

    print(labels)

    print("\nMin Visibility :", labels.min().item())
    print("Max Visibility :", labels.max().item())

    print("\nDataLoader created successfully.")


if __name__ == "__main__":
    main()