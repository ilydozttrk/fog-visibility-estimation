"""
attention.py

CBAM (Convolutional Block Attention Module) components
for the fog visibility estimation project.

The module contains:
- ChannelAttention
- SpatialAttention
- CBAM

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

import torch
import torch.nn as nn


# =============================================================================
# Channel Attention
# =============================================================================

class ChannelAttention(nn.Module):
    """
    Channel attention module used in CBAM.

    The module learns which feature channels are more important by using
    both global average pooling and global max pooling.

    Expected input shape:
        [batch_size, channels, height, width]

    Output shape:
        Same as the input shape.
    """

    def __init__(
        self,
        channels: int,
        reduction_ratio: int = 16,
    ) -> None:
        super().__init__()

        if channels <= 0:
            raise ValueError("channels must be greater than zero.")

        if reduction_ratio <= 0:
            raise ValueError(
                "reduction_ratio must be greater than zero."
            )

        reduced_channels = max(
            channels // reduction_ratio,
            1,
        )

        self.average_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        self.shared_mlp = nn.Sequential(
            nn.Conv2d(
                channels,
                reduced_channels,
                kernel_size=1,
                bias=False,
            ),
            nn.ReLU(inplace=True),
            nn.Conv2d(
                reduced_channels,
                channels,
                kernel_size=1,
                bias=False,
            ),
        )

        self.sigmoid = nn.Sigmoid()

    def forward(
        self,
        feature_map: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply channel attention to the input feature map.
        """

        average_features = self.average_pool(
            feature_map
        )

        max_features = self.max_pool(
            feature_map
        )

        average_attention = self.shared_mlp(
            average_features
        )

        max_attention = self.shared_mlp(
            max_features
        )

        attention_weights = self.sigmoid(
            average_attention + max_attention
        )

        return feature_map * attention_weights


# =============================================================================
# Spatial Attention
# =============================================================================

class SpatialAttention(nn.Module):
    """
    Spatial attention module used in CBAM.

    The module learns which spatial regions of a feature map are more
    important by combining channel-wise average and maximum projections.

    Expected input shape:
        [batch_size, channels, height, width]

    Output shape:
        Same as the input shape.
    """

    def __init__(
        self,
        kernel_size: int = 7,
    ) -> None:
        super().__init__()

        if kernel_size not in (3, 7):
            raise ValueError(
                "kernel_size must be either 3 or 7."
            )

        padding = kernel_size // 2

        self.convolution = nn.Conv2d(
            in_channels=2,
            out_channels=1,
            kernel_size=kernel_size,
            padding=padding,
            bias=False,
        )

        self.sigmoid = nn.Sigmoid()

    def forward(
        self,
        feature_map: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply spatial attention to the input feature map.
        """

        average_projection = torch.mean(
            feature_map,
            dim=1,
            keepdim=True,
        )

        max_projection, _ = torch.max(
            feature_map,
            dim=1,
            keepdim=True,
        )

        combined_projection = torch.cat(
            [
                average_projection,
                max_projection,
            ],
            dim=1,
        )

        attention_weights = self.sigmoid(
            self.convolution(
                combined_projection
            )
        )

        return feature_map * attention_weights


# =============================================================================
# CBAM
# =============================================================================

class CBAM(nn.Module):
    """
    Convolutional Block Attention Module.

    CBAM sequentially applies:

        1. Channel Attention
        2. Spatial Attention

    The module preserves the spatial and channel dimensions of the
    input tensor.

    Expected input shape:
        [batch_size, channels, height, width]

    Output shape:
        Same as the input shape.
    """

    def __init__(
        self,
        channels: int,
        reduction_ratio: int = 16,
        spatial_kernel_size: int = 7,
    ) -> None:
        super().__init__()

        self.channel_attention = ChannelAttention(
            channels=channels,
            reduction_ratio=reduction_ratio,
        )

        self.spatial_attention = SpatialAttention(
            kernel_size=spatial_kernel_size,
        )

    def forward(
        self,
        feature_map: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply channel attention followed by spatial attention.
        """

        feature_map = self.channel_attention(
            feature_map
        )

        feature_map = self.spatial_attention(
            feature_map
        )

        return feature_map