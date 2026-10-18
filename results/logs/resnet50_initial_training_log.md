# Initial ResNet50 Training Log

- Experiment ID: RESNET50_20260805_153802
- Date: 2026-08-05 15:51:20
- Model: ResNet50
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
| 1 | 271.6411 | 269.8412 |
| 2 | 266.2808 | 259.5987 |
| 3 | 250.5383 | 234.3485 |
| 4 | 220.5133 | 199.2553 |
| 5 | 192.9872 | 182.9822 |
| 6 | 179.9341 | 176.3945 |
| 7 | 174.0165 | 173.3504 |
| 8 | 170.0832 | 170.9314 |
| 9 | 166.4874 | 167.8646 |
| 10 | 163.6314 | 164.6922 |
| 11 | 160.8661 | 160.7789 |
| 12 | 157.0239 | 157.2018 |
| 13 | 152.1078 | 153.0893 |
| 14 | 150.0104 | 148.6981 |
| 15 | 145.5692 | 144.3990 |
| 16 | 141.3888 | 139.3017 |
| 17 | 135.5398 | 134.1208 |
| 18 | 130.7967 | 129.7215 |
| 19 | 126.1762 | 125.4370 |
| 20 | 122.1239 | 121.8414 |

## Best Result

- Best epoch: 20
- Best validation MAE: 121.8414 m
- Checkpoint: `results/checkpoints/resnet50_baseline_best.pth`

## Initial Observation

The ResNet50 baseline training pipeline completed successfully. The checkpoint corresponding to the lowest validation MAE was saved for subsequent evaluation and model comparison.