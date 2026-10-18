# Initial VGG16 Training Log

- Experiment ID: VGG16_20260721_142833
- Date: 2026-07-21 14:55:54
- Model: VGG16
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

## Epoch Results

| Epoch | Training MAE (m) | Validation MAE (m) |
|---:|---:|---:|
| 1 | 261.0132 | 241.3220 |
| 2 | 204.3121 | 170.6629 |
| 3 | 159.2718 | 154.2670 |
| 4 | 148.9872 | 145.1631 |
| 5 | 137.5579 | 134.5635 |
| 6 | 122.3133 | 122.6332 |
| 7 | 110.7579 | 112.9991 |
| 8 | 102.4721 | 103.6436 |
| 9 | 92.4561 | 98.4740 |
| 10 | 85.1748 | 91.3189 |
| 11 | 79.3323 | 86.6129 |
| 12 | 71.2913 | 83.0369 |
| 13 | 67.6843 | 79.9300 |
| 14 | 64.1581 | 79.1710 |
| 15 | 60.8906 | 79.1584 |
| 16 | 56.9364 | 74.9453 |
| 17 | 53.2926 | 71.1596 |
| 18 | 51.8818 | 69.9705 |
| 19 | 48.3109 | 70.7949 |
| 20 | 46.7393 | 70.0777 |

## Best Result

- Best epoch: 18
- Best validation MAE: 69.9705 m
- Checkpoint: `results/checkpoints/vgg16_baseline_best.pth`

## Initial Observation

The VGG16 baseline training pipeline completed successfully. The checkpoint corresponding to the lowest validation MAE was saved for subsequent evaluation and model comparison.