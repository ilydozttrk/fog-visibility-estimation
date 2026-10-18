"""
regression_models.py

Shared construction and partial fine-tuning helpers for the two
transfer-learning backbones compared in the project.

The helpers keep VGG16 and ResNet50 on an equal protocol:

    VGG16    : Blocks 1-4 frozen, Block 5 (features[24:]) trainable
    ResNet50 : conv1 + layer1-3 frozen, layer4 trainable

In both cases the regression head is trainable and the last
convolutional stage is trained with a lower learning rate than the
head. This mirrors the strategy used for the final VGG16 FVEI model.

BatchNorm (ResNet50 only)
-------------------------
During the synthetic stage every BatchNorm layer was kept in eval
mode because the backbone was frozen. The same rule is applied here:
running statistics are never updated (small batches of 16 would give
noisy estimates), while the affine BatchNorm parameters inside layer4
remain trainable.

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from __future__ import annotations

from collections import OrderedDict

import torch.nn as nn
from torchvision.models import ResNet50_Weights, resnet50

from src.training.config import (
    DROPOUT_RATE,
    REGRESSION_HIDDEN_DIM_1,
    REGRESSION_HIDDEN_DIM_2,
)
from src.models.attention import CBAM, SEBlock
from src.training.train_vgg16 import build_vgg16_regression_model


# Backbones used for the architecture comparison and FVEI fine-tuning.
BASE_ARCHITECTURES = ("vgg16", "resnet50")

# ResNet50 + attention variants (synthetic multi-seed only). They mirror
# the VGG16 CBAM / SE experiments: the attention module is applied to
# the output of the last convolutional stage (ResNet50 layer4, 2048
# channels; VGG16: last conv block, 512 channels), the backbone stays
# frozen and only the attention module and the regression head train.
# CBAM: reduction ratio 16, spatial kernel 7. SE: reduction ratio 16.
ATTENTION_ARCHITECTURES = ("resnet50_cbam", "resnet50_se")

SUPPORTED_ARCHITECTURES = BASE_ARCHITECTURES + ATTENTION_ARCHITECTURES

ATTENTION_REDUCTION_RATIO = 16
CBAM_SPATIAL_KERNEL_SIZE = 7

VGG16_BLOCK5_START_INDEX = 24

DISPLAY_NAMES = {
    "vgg16": "VGG16",
    "resnet50": "ResNet50",
    "resnet50_cbam": "ResNet50 + CBAM",
    "resnet50_se": "ResNet50 + SE",
}

LAST_BLOCK_NAMES = {
    "vgg16": "VGG16 Block 5",
    "resnet50": "ResNet50 layer4",
}


def _check_arch(arch: str) -> None:
    if arch not in SUPPORTED_ARCHITECTURES:
        raise ValueError(
            f"Unsupported architecture '{arch}'. "
            f"Expected one of {SUPPORTED_ARCHITECTURES}."
        )


def _regression_head(input_features: int) -> nn.Sequential:
    """
    Same head as in train_vgg16.py / train_resnet50.py, so that the
    saved state_dict keys stay compatible.
    """

    return nn.Sequential(
        nn.Linear(input_features, REGRESSION_HIDDEN_DIM_1),
        nn.ReLU(inplace=True),
        nn.Dropout(DROPOUT_RATE),
        nn.Linear(REGRESSION_HIDDEN_DIM_1, REGRESSION_HIDDEN_DIM_2),
        nn.ReLU(inplace=True),
        nn.Dropout(DROPOUT_RATE),
        nn.Linear(REGRESSION_HIDDEN_DIM_2, 1),
    )


def build_regression_model(arch: str, pretrained: bool = True) -> nn.Module:
    """
    Build an (optionally ImageNet-pretrained) regression model.

    Use pretrained=False when a complete project checkpoint is loaded
    immediately afterwards; this avoids an unnecessary weight download.
    """

    _check_arch(arch)

    if arch == "vgg16":
        return build_vgg16_regression_model(pretrained=pretrained)

    model = resnet50(weights=ResNet50_Weights.DEFAULT if pretrained else None)
    channels = model.fc.in_features
    model.fc = _regression_head(channels)

    if arch in ATTENTION_ARCHITECTURES:
        if arch == "resnet50_cbam":
            attention = CBAM(
                channels=channels,
                reduction_ratio=ATTENTION_REDUCTION_RATIO,
                spatial_kernel_size=CBAM_SPATIAL_KERNEL_SIZE,
            )
        else:
            attention = SEBlock(
                channels=channels,
                reduction_ratio=ATTENTION_REDUCTION_RATIO,
            )

        model.layer4 = nn.Sequential(
            OrderedDict(block=model.layer4, attention=attention)
        )

    return model


def get_attention(model: nn.Module, arch: str) -> nn.Module | None:
    _check_arch(arch)
    return model.layer4.attention if arch in ATTENTION_ARCHITECTURES else None


def get_head(model: nn.Module, arch: str) -> nn.Module:
    _check_arch(arch)
    return model.classifier if arch == "vgg16" else model.fc


def get_last_block(model: nn.Module, arch: str) -> nn.Module:
    _check_arch(arch)

    if arch == "vgg16":
        return model.features[VGG16_BLOCK5_START_INDEX:]

    if arch in ATTENTION_ARCHITECTURES:
        return model.layer4.block

    return model.layer4


def freeze_all_but_head(model: nn.Module, arch: str) -> None:
    """
    Synthetic-stage protocol: frozen backbone, trainable head
    (plus the attention module for the attention variants).
    """

    for parameter in model.parameters():
        parameter.requires_grad = False

    for parameter in get_head(model, arch).parameters():
        parameter.requires_grad = True

    attention = get_attention(model, arch)
    if attention is not None:
        for parameter in attention.parameters():
            parameter.requires_grad = True


def configure_last_block_finetuning(model: nn.Module, arch: str) -> None:
    """Freeze everything except the last convolutional stage and head."""

    if arch not in BASE_ARCHITECTURES:
        raise ValueError("Last-block fine-tuning is defined for vgg16 and resnet50 only.")

    freeze_all_but_head(model, arch)

    for parameter in get_last_block(model, arch).parameters():
        parameter.requires_grad = True


def verify_last_block_finetuning(model: nn.Module, arch: str) -> dict:
    """
    Raise if the trainable-parameter layout is not the intended one.
    Returns parameter counts for logging.
    """

    head_ids = {id(p) for p in get_head(model, arch).parameters()}
    block_ids = {id(p) for p in get_last_block(model, arch).parameters()}

    if not block_ids:
        raise RuntimeError("No last-block parameters found.")

    counts = {"last_block": 0, "head": 0, "frozen": 0}

    for parameter in model.parameters():
        if id(parameter) in head_ids or id(parameter) in block_ids:
            if not parameter.requires_grad:
                raise RuntimeError(
                    "Last block and head parameters must be trainable."
                )
            key = "head" if id(parameter) in head_ids else "last_block"
            counts[key] += parameter.numel()
        else:
            if parameter.requires_grad:
                raise RuntimeError(
                    "Only the last block and the head may be trainable."
                )
            counts["frozen"] += parameter.numel()

    return counts


def last_block_parameter_groups(
    model: nn.Module,
    arch: str,
    last_block_lr: float,
    head_lr: float,
) -> list[dict]:
    return [
        {
            "params": [
                p for p in get_last_block(model, arch).parameters()
                if p.requires_grad
            ],
            "lr": last_block_lr,
        },
        {
            "params": [
                p for p in get_head(model, arch).parameters()
                if p.requires_grad
            ],
            "lr": head_lr,
        },
    ]


def set_train_mode(model: nn.Module) -> None:
    """
    model.train() while keeping every BatchNorm layer in eval mode
    (no-op for VGG16, which has no BatchNorm).
    """

    model.train()

    for module in model.modules():
        if isinstance(module, nn.modules.batchnorm._BatchNorm):
            module.eval()
