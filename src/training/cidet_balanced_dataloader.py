"""
cidet_balanced_dataloader.py

Balanced training DataLoader for CIDET visibility estimation.

The training split is sampled using inverse-frequency weights over
predefined visibility ranges. Validation and test distributions are
left unchanged.

Visibility bins:
- <500 m
- 500-999 m
- 2000-2999 m
- >=3000 m

The 1000-1999 m range is absent from the CIDET temporal training split
and is therefore not artificially synthesized.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import torch
from torch.utils.data import DataLoader, WeightedRandomSampler

from src.training.cidet_dataloader import (
    CIDETVisibilityDataset,
    TEST_CSV,
    TRAIN_CSV,
    VALIDATION_CSV,
    build_image_index,
    get_cidet_transforms,
)
from src.training.config import (
    BATCH_SIZE,
    IMAGE_SIZE,
    NUM_WORKERS,
    RANDOM_SEED,
)


def assign_visibility_bin(target: float) -> str:
    """Assign a CIDET visibility target to its sampling bin."""
    if target < 500.0:
        return "<500"

    if target < 1000.0:
        return "500-999"

    if target < 2000.0:
        return "1000-1999"

    if target < 3000.0:
        return "2000-2999"

    return ">=3000"


def create_sampling_weights(
    train_dataset: CIDETVisibilityDataset,
) -> tuple[torch.Tensor, dict[str, int]]:
    """
    Create inverse-bin-frequency sampling weights.

    Each observed visibility bin receives approximately equal expected
    sampling probability, while individual samples inside a bin remain
    equally likely.
    """
    targets = (
        train_dataset.data[
            CIDETVisibilityDataset.TARGET_COLUMN
        ]
        .astype(float)
        .tolist()
    )

    sample_bins = [
        assign_visibility_bin(target)
        for target in targets
    ]

    bin_counts: dict[str, int] = {}

    for bin_name in sample_bins:
        bin_counts[bin_name] = (
            bin_counts.get(bin_name, 0) + 1
        )

    weights = [
        1.0 / bin_counts[bin_name]
        for bin_name in sample_bins
    ]

    return (
        torch.tensor(
            weights,
            dtype=torch.double,
        ),
        bin_counts,
    )


def create_cidet_balanced_dataloaders(
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
    Create balanced-training CIDET DataLoaders.

    Only the training sampling strategy changes.
    Validation and test loaders preserve their original distributions.
    """
    image_index = build_image_index()

    transform = get_cidet_transforms(
        image_size=image_size
    )

    train_dataset = CIDETVisibilityDataset(
        csv_path=TRAIN_CSV,
        image_index=image_index,
        transform=transform,
    )

    validation_dataset = CIDETVisibilityDataset(
        csv_path=VALIDATION_CSV,
        image_index=image_index,
        transform=transform,
    )

    test_dataset = CIDETVisibilityDataset(
        csv_path=TEST_CSV,
        image_index=image_index,
        transform=transform,
    )

    sampling_weights, bin_counts = (
        create_sampling_weights(
            train_dataset
        )
    )

    generator = torch.Generator()
    generator.manual_seed(random_seed)

    sampler = WeightedRandomSampler(
        weights=sampling_weights,
        num_samples=len(train_dataset),
        replacement=True,
        generator=generator,
    )

    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        sampler=sampler,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )

    validation_loader = DataLoader(
        dataset=validation_dataset,
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

    print(
        "\n--- CIDET BALANCED SAMPLING ---"
    )

    for bin_name in [
        "<500",
        "500-999",
        "1000-1999",
        "2000-2999",
        ">=3000",
    ]:
        print(
            f"{bin_name:10s}: "
            f"{bin_counts.get(bin_name, 0)} "
            "original samples"
        )

    print(
        f"Samples drawn per epoch: "
        f"{len(train_dataset)}"
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
    ) = create_cidet_balanced_dataloaders()

    print(
        "\n=== BALANCED CIDET DATALOADER TEST ==="
    )

    print(
        f"Train dataset size:      "
        f"{len(train_loader.dataset)}"
    )

    print(
        f"Validation dataset size: "
        f"{len(validation_loader.dataset)}"
    )

    print(
        f"Test dataset size:       "
        f"{len(test_loader.dataset)}"
    )

    sampled_counts = {
        "<500": 0,
        "500-999": 0,
        "1000-1999": 0,
        "2000-2999": 0,
        ">=3000": 0,
    }

    for sampled_index in train_loader.sampler:
        target = float(
            train_loader.dataset.data.iloc[
                sampled_index
            ][
                CIDETVisibilityDataset.TARGET_COLUMN
            ]
        )

        bin_name = assign_visibility_bin(
            target
        )

        sampled_counts[bin_name] += 1

    print(
        "\n--- ONE SEEDED SAMPLING EPOCH ---"
    )

    for bin_name, count in sampled_counts.items():
        print(
            f"{bin_name:10s}: {count}"
        )

    expected_counts = (
        685,
        147,
        145,
    )

    actual_counts = (
        len(train_loader.dataset),
        len(validation_loader.dataset),
        len(test_loader.dataset),
    )

    if actual_counts != expected_counts:
        raise ValueError(
            "Unexpected CIDET split counts. "
            f"Expected {expected_counts}, "
            f"found {actual_counts}."
        )

    print(
        "\nBalanced CIDET DataLoaders "
        "created successfully."
    )


if __name__ == "__main__":
    main()
