# VGG16 + SE Evaluation Report

## Model

- Architecture: VGG16 + SE
- Pretrained weights: ImageNet
- Frozen backbone: True
- SE reduction ratio: 16
- SE integration point: after VGG16 conv5_3 and before final MaxPool

## Checkpoint

- Best checkpoint epoch: 19
- Validation MAE at checkpoint: 70.6083 m

## Test Results

- Test samples: 112
- Test MAE: 72.4412 m
- Mean signed error: -12.9774 m
- Minimum absolute error: 0.1255 m
- Maximum absolute error: 423.1353 m

## Interpretation

The VGG16 + SE model was evaluated on the same independent scene-based test split used for the VGG16 baseline and VGG16 + CBAM experiments. The resulting metrics can therefore be directly compared under the current synthetic FRIDA/FRIDA2 experimental setup.