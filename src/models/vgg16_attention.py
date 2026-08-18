"""
vgg16_attention.py

Attention-enhanced VGG16 regression architecture using CBAM
for fog visibility estimation.

Architecture:
    Frozen VGG16 convolutional backbone
    -> CBAM
    -> Final MaxPool
    -> Adaptive Average Pool
    -> Regression Head

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import torch
import torch.nn as nn
from torchvision.models import VGG16_Weights, vgg16

from src.models.attention import CBAM


class VGG16AttentionRegressor(nn.Module):
    """
    VGG16-based visibility regression model enhanced with CBAM.

    CBAM is inserted after the final convolutional block and before
    the last VGG16 max-pooling operation.

    For 224x224 input images:

        Input
            -> VGG16 convolutional features
            -> [B, 512, 14, 14]
            -> CBAM
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
        cbam_reduction_ratio: int = 16,
        cbam_spatial_kernel_size: int = 7,
    ) -> None:
        super().__init__()

        weights = VGG16_Weights.DEFAULT
        vgg_model = vgg16(weights=weights)

        # ---------------------------------------------------------
        # VGG16 Feature Extractor
        # ---------------------------------------------------------
        #
        # torchvision VGG16 features:
        #
        # features[:-1]
        #     -> all convolutional layers and ReLU activations
        #        up to the final conv block
        #
        # features[-1]
        #     -> final MaxPool2d layer
        #
        # CBAM is inserted between these two stages.
        #

        self.feature_extractor = nn.Sequential(
            *list(vgg_model.features.children())[:-1]
        )

        self.final_max_pool = list(
            vgg_model.features.children()
        )[-1]

        # Preserve the original VGG16 adaptive pooling stage.
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
        # CBAM
        # ---------------------------------------------------------

        self.attention = CBAM(
            channels=512,
            reduction_ratio=cbam_reduction_ratio,
            spatial_kernel_size=cbam_spatial_kernel_size,
        )

        # ---------------------------------------------------------
        # Regression Head
        # ---------------------------------------------------------
        #
        # The regression head is intentionally kept equivalent to
        # the VGG16 baseline so that the primary architectural
        # difference is the addition of CBAM.
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
        Perform a forward pass through the attention-enhanced VGG16 model.
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


def build_vgg16_attention_regression_model(
    freeze_backbone: bool = True,
    regression_hidden_dim_1: int = 512,
    regression_hidden_dim_2: int = 128,
    dropout_rate: float = 0.30,
    cbam_reduction_ratio: int = 16,
    cbam_spatial_kernel_size: int = 7,
) -> nn.Module:
    """
    Build and return the CBAM-enhanced VGG16 regression model.
    """

    return VGG16AttentionRegressor(
        freeze_backbone=freeze_backbone,
        regression_hidden_dim_1=regression_hidden_dim_1,
        regression_hidden_dim_2=regression_hidden_dim_2,
        dropout_rate=dropout_rate,
        cbam_reduction_ratio=cbam_reduction_ratio,
        cbam_spatial_kernel_size=cbam_spatial_kernel_size,
    )