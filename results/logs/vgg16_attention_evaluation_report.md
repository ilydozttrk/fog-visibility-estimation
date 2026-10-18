# VGG16 + CBAM Evaluation Report

## Model

- Architecture: VGG16 + CBAM
- Pretrained weights: ImageNet
- Frozen backbone: True
- CBAM reduction ratio: 16
- CBAM spatial kernel size: 7

## Checkpoint

- Best checkpoint epoch: 17
- Validation MAE at checkpoint: 69.3274 m

## Test Results

- Test samples: 112
- Test MAE: 67.6214 m
- Mean signed error: -10.8501 m
- Minimum absolute error: 0.4317 m
- Maximum absolute error: 439.5097 m

## Interpretation

The VGG16 + CBAM model was evaluated on the same independent scene-based test split used for the baseline models. The resulting metrics can therefore be directly compared with the VGG16 baseline under the current synthetic FRIDA/FRIDA2 experimental setup.