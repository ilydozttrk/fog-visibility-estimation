# ResNet50 Baseline Evaluation Report

## Model Information

- Model: ResNet50
- Pretrained weights: ImageNet
- Checkpoint path: `results/checkpoints/resnet50_baseline_best.pth`
- Best checkpoint epoch: 20
- Best validation MAE: 121.8414 m

## Test Dataset

- Split: Held-out test set
- Test image count: 112
- Random seed: 42

## Evaluation Results

- Test MAE: 124.6181 m
- Mean signed error: -77.3460 m
- Minimum absolute error: 0.7323 m
- Maximum absolute error: 602.6687 m
- Test-validation MAE difference: 2.7767 m

## Interpretation

The test MAE is close to the validation MAE. This indicates that the model preserves similar performance on previously unseen scenes and demonstrates good generalization capability.

The project target of achieving a Mean Absolute Error (MAE) below 100 metres was not achieved under the current baseline configuration.

This result represents the initial ResNet50 baseline trained and evaluated under the same dataset split, preprocessing pipeline, training duration, optimization strategy, and evaluation methodology used for the VGG16 baseline, ensuring a fair and reproducible comparison.

The obtained results indicate that the baseline pipeline is stable and reproducible. Although the ResNet50 baseline did not outperform the VGG16 baseline under the current experimental settings, it provides a reliable reference point for the subsequent attention mechanism integration and comparative analysis.

## Generated Outputs

- `results/evaluation/resnet50_test_predictions.csv`
- `results/evaluation/resnet50_evaluation_summary.json`
- `results/plots/resnet50_actual_vs_predicted.png`
- `results/plots/resnet50_prediction_error_histogram.png`
- `results/logs/resnet50_evaluation_report.md`

## Next Stage

The next stage is to perform a comprehensive comparison between the VGG16 and ResNet50 baseline models using validation MAE, test MAE, signed-error behaviour, absolute-error distributions, and prediction plots.

Based on the independent test performance, the most suitable baseline model will be selected as the reference architecture for the attention mechanism integration planned in the project methodology.

Following the baseline comparison, the attention mechanism will be integrated into the selected model, and the resulting architecture will be evaluated under the same experimental conditions to determine whether it provides a measurable improvement in fog visibility estimation performance.