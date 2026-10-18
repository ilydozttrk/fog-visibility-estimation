# VGG16 Baseline Evaluation Report

## Model Information

- Model: VGG16
- Pretrained weights: ImageNet
- Checkpoint path: `results/checkpoints/vgg16_baseline_best.pth`
- Best checkpoint epoch: 18
- Best validation MAE: 69.9705 m

## Test Dataset

- Split: Held-out test set
- Test image count: 112
- Random seed: 42

## Evaluation Results

- Test MAE: 66.7227 m
- Mean signed error: -17.3877 m
- Minimum absolute error: 0.8415 m
- Maximum absolute error: 392.8829 m
- Test-validation MAE difference: -3.2478 m

## Interpretation

The test MAE is close to the validation MAE. This indicates that the model preserves similar performance on previously unseen scenes.

The project target of MAE below 100 metres was achieved.

## Generated Outputs

- `results/evaluation/vgg16_test_predictions.csv`
- `results/evaluation/vgg16_evaluation_summary.json`
- `results/plots/vgg16_actual_vs_predicted.png`
- `results/plots/vgg16_prediction_error_histogram.png`

## Next Stage

The next stage is to implement and train the ResNet50 baseline under the same dataset split, preprocessing pipeline, evaluation metrics, and reproducibility settings. The VGG16 and ResNet50 results will then be compared using validation MAE, test MAE, error distributions, and prediction behaviour.