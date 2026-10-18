# Initial VGG16 + SE Training Log

- Experiment ID: VGG16_SE_20260914_164628
- Date: 2026-09-14 17:10:36
- Model: VGG16 + SE
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
- SE reduction ratio: 16
- SE integration point: after VGG16 conv5_3 and before final MaxPool
- Experimental role: risk-management alternative defined in the accepted proposal after CBAM failed to improve test MAE

## Epoch Results

| Epoch | Training MAE (m) | Validation MAE (m) |
|---:|---:|---:|
| 1 | 266.7582 | 257.1333 |
| 2 | 234.4882 | 202.2583 |
| 3 | 173.9657 | 160.1625 |
| 4 | 154.9086 | 151.8765 |
| 5 | 145.4441 | 143.7902 |
| 6 | 134.4391 | 134.2508 |
| 7 | 126.8667 | 126.0397 |
| 8 | 114.1404 | 115.1241 |
| 9 | 104.3398 | 107.3020 |
| 10 | 96.5903 | 100.6104 |
| 11 | 85.4510 | 94.4071 |
| 12 | 83.1759 | 92.7204 |
| 13 | 74.8621 | 87.0896 |
| 14 | 71.6234 | 85.1999 |
| 15 | 65.6736 | 80.1442 |
| 16 | 65.3482 | 75.8461 |
| 17 | 57.2878 | 73.7280 |
| 18 | 56.5222 | 71.5401 |
| 19 | 54.9758 | 70.6083 |
| 20 | 50.1878 | 70.7658 |

## Best Result

- Best epoch: 19
- Best validation MAE: 70.6083 m
- Checkpoint: `results/checkpoints/vgg16_se_best.pth`

## Initial Observation

The VGG16 + SE training pipeline completed successfully. The checkpoint corresponding to the lowest validation MAE was saved for subsequent independent test evaluation and comparison with the VGG16 baseline and VGG16 + CBAM experiments.