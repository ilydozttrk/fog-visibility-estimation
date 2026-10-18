# Initial VGG16 + CBAM Training Log

- Experiment ID: VGG16_CBAM_20260913_230546
- Date: 2026-09-13 23:44:46
- Model: VGG16 + CBAM
- Pretrained weights: ImageNet
- Frozen backbone: True
- Device: cpu
- Image size: 224 x 224
- Batch size: 16
- Epoch count: 20
- Optimizer: Adam
- Learning rate: 0.0001
- Weight decay: 1e-05
- Loss function: L1Loss / Mean Absolute Error
- Random seed: 42
- CBAM reduction ratio: 16
- CBAM spatial kernel size: 7
- CBAM integration point: after VGG16 conv5_3 and before final MaxPool

## Epoch Results

| Epoch | Training MAE (m) | Validation MAE (m) |
|---:|---:|---:|
| 1 | 267.8913 | 258.7876 |
| 2 | 230.8050 | 189.9272 |
| 3 | 164.6005 | 154.0964 |
| 4 | 148.3180 | 144.7604 |
| 5 | 135.7440 | 135.0698 |
| 6 | 124.7086 | 124.7375 |
| 7 | 115.8776 | 115.8241 |
| 8 | 101.2188 | 105.6936 |
| 9 | 91.3170 | 97.6088 |
| 10 | 82.4766 | 88.2836 |
| 11 | 77.4688 | 83.2882 |
| 12 | 70.3482 | 81.2921 |
| 13 | 63.9028 | 76.7301 |
| 14 | 58.9256 | 78.1578 |
| 15 | 52.7865 | 73.7326 |
| 16 | 52.0578 | 73.4611 |
| 17 | 47.8197 | 69.3274 |
| 18 | 44.3514 | 73.6024 |
| 19 | 45.3199 | 69.7572 |
| 20 | 41.0328 | 76.0531 |

## Best Result

- Best epoch: 17
- Best validation MAE: 69.3274 m
- Checkpoint: `results/checkpoints/vgg16_attention_best.pth`

## Initial Observation

The VGG16 + CBAM training pipeline completed successfully. The checkpoint corresponding to the lowest validation MAE was saved for subsequent independent evaluation and comparison with the VGG16 baseline.