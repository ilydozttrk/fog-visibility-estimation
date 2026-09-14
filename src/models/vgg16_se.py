"""
vgg16_se.py

SE-enhanced VGG16 regression architecture
for fog visibility estimation.

Architecture:
    Frozen VGG16 convolutional backbone
    -> SE Block
    -> Final MaxPool
    -> Adaptive Average Pool
    -> Regression Head

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import torch
import torch.nn as nn
from torchvision.models import VGG16_Weights, vgg16

from src.models.attention import SEBlock


class VGG16SERegressor(nn.Module):
    """
    VGG16-based visibility regression model enhanced with
    Squeeze-and-Excitation (SE) channel attention.

    SE is inserted after the final convolutional block and before
    the last VGG16 max-pooling operation.

    For 224x224 input images:

        Input
            -> VGG16 convolutional features
            -> [B, 512, 14, 14]
            -> SE Block
            -> [B, 512, 14, 14]
            -> Final MaxPool
            -> [B, 512, 7, 7]
            -> AdaptiveAvgPool
            -> Flatten
            -> Regression Head
            -> [B, 1]
    """

    def __init__(
        self,
        freeze_backbone: bool = True,
        regression_hidden_dim_1: int = 512,
        regression_hidden_dim_2: int = 128,
        dropout_rate: float = 0.30,
        se_reduction_ratio: int = 16,
    ) -> None:
        super().__init__()

        weights = VGG16_Weights.DEFAULT
        vgg_model = vgg16(weights=weights)

        # ---------------------------------------------------------
        # VGG16 Feature Extractor
        # ---------------------------------------------------------

        self.feature_extractor = nn.Sequential(
            *list(vgg_model.features.children())[:-1]
        )

        self.final_max_pool = list(
            vgg_model.features.children()
        )[-1]

        self.avg_pool = vgg_model.avgpool

        # ---------------------------------------------------------
        # Freeze Pretrained Backbone
        # ---------------------------------------------------------

        if freeze_backbone:
            for parameter in self.feature_extractor.parameters():
                parameter.requires_grad = False

            for parameter in self.final_max_pool.parameters():
                parameter.requires_grad = False

        # ---------------------------------------------------------
        # Squeeze-and-Excitation Attention
        # ---------------------------------------------------------

        self.attention = SEBlock(
            channels=512,
            reduction_ratio=se_reduction_ratio,
        )

        # ---------------------------------------------------------
        # Regression Head
        # ---------------------------------------------------------
        #
        # The regression head is intentionally kept identical to
        # the VGG16 baseline and VGG16 + CBAM experiments.
        #
        # This keeps the attention mechanism as the primary
        # architectural variable in the comparison.
        #

        classifier_input_features = (
            vgg_model.classifier[0].in_features
        )

        self.regression_head = nn.Sequential(
            nn.Linear(
                classifier_input_features,
                regression_hidden_dim_1,
            ),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate),
            nn.Linear(
                regression_hidden_dim_1,
                regression_hidden_dim_2,
            ),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout_rate),
            nn.Linear(
                regression_hidden_dim_2,
                1,
            ),
        )

    def forward(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """
        Perform a forward pass through the SE-enhanced VGG16 model.
        """

        features = self.feature_extractor(images)

        features = self.attention(features)

        features = self.final_max_pool(features)

        features = self.avg_pool(features)

        features = torch.flatten(
            features,
            start_dim=1,
        )

        predictions = self.regression_head(features)

        return predictions


def build_vgg16_se_regression_model(
    freeze_backbone: bool = True,
    regression_hidden_dim_1: int = 512,
    regression_hidden_dim_2: int = 128,
    dropout_rate: float = 0.30,
    se_reduction_ratio: int = 16,
) -> nn.Module:
    """
    Build and return the SE-enhanced VGG16 regression model.
    """

    return VGG16SERegressor(
        freeze_backbone=freeze_backbone,
        regression_hidden_dim_1=regression_hidden_dim_1,
        regression_hidden_dim_2=regression_hidden_dim_2,
        dropout_rate=dropout_rate,
        se_reduction_ratio=se_reduction_ratio,
    )