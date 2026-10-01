# Final Results Summary

**Project:** Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Program:** TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı

---

# 1. Purpose

This document consolidates the final experiment results that will be used while preparing the TÜBİTAK final report and publication-oriented outputs.

The results are divided into:

1. synthetic FRIDA/FRIDA2 model comparison,
2. auxiliary real-world domain-shift experiments,
3. FVEI real-world fine-tuning,
4. locked FVEI test evaluation,
5. final Flask prototype validation.

The FVEI held-out test results were obtained only after validation-based model selection was completed.

No additional checkpoint selection or hyperparameter tuning was performed after observing the held-out FVEI test results.

---

# 2. Synthetic FRIDA / FRIDA2 Results

The synthetic dataset contained:

| Property | Value |
|---|---:|
| Scenes | 84 |
| Images | 672 |
| Train | 464 |
| Validation | 96 |
| Test | 112 |
| Random Seed | 42 |

## Final Synthetic Model Comparison

| Model | Best Validation MAE | Test MAE |
|---|---:|---:|
| VGG16 Baseline | 69.9705 m | **66.7227 m** |
| VGG16 + CBAM | **69.3274 m** | 67.6214 m |
| VGG16 + SE | 70.6083 m | 72.4412 m |
| ResNet50 Baseline | 121.8414 m | 124.6181 m |

Under the current FRIDA/FRIDA2 experimental configuration, VGG16 baseline produced the lowest held-out synthetic Test MAE.

The attention experiments did not improve the primary Test MAE metric over the VGG16 baseline.

Selected synthetic starting model:

**VGG16 Baseline**

## Figure

![Synthetic model comparison](../../figures/synthetic_model_test_mae_comparison.png)

---

# 3. Auxiliary Real-World Experiments

CIDET and Benchmark-Visibility were used as auxiliary development and domain-shift experiments.

They were not used to select the final FVEI model.

## CIDET Development Results

| Strategy | Validation MAE |
|---|---:|
| Head-only + L1 | 446.5714 m |
| Block5 + L1 | 326.6640 m |
| Block5 + Balanced Sampling | 334.9808 m |
| Block5 + Huber | **324.1948 m** |

## Benchmark-Visibility Stress Test

| Metric | Result |
|---|---:|
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Bias | -11310.9893 m |
| Pearson Correlation | 0.585183 |
| Prediction Range | 97.43–1308.30 m |
| Target Range | 112–20000 m |

This stress test documented strong target-range mismatch and prediction-range compression under a substantially different visibility range.

---

# 4. FVEI Dataset Audit

Original FVEI ZIP SHA256:

`07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d`

## Audit Summary

| Category | Samples |
|---|---:|
| Retained | 4109 |
| Exact-label | 3209 |
| Level-4 / 500 m analysis group | 900 |
| Conflicting duplicates rejected | 229 |
| Outside-level-range rejected | 32 |
| Redundant identical images removed | 130 |

## Exact-Label Distribution

| Level | Samples | Observed Range |
|---|---:|---:|
| Level 0 | 785 | 12–49 m |
| Level 1 | 846 | 51–99 m |
| Level 2 | 793 | 101–199 m |
| Level 3 | 785 | 201–499 m |

The 900 images carrying the 500 m label were kept separate from exact-label regression metrics.

Their precise ceiling/censored label semantics should be verified from the official dataset documentation before publication.

---

# 5. Final FVEI Split

Random seed:

**42**

After similarity screening:

| Split | Samples |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Locked Test | 482 |
| Similarity Exclusions | 2 |
| Level-4 / 500 m Analysis | 900 |

Two validation-side samples were excluded after strict cross-split similarity screening.

The held-out test set was not changed.

Reliable scene/camera identifiers were not available in the current FVEI pipeline, so residual sample dependence cannot be completely excluded.

---

# 6. FVEI Fine-Tuning

Initialization checkpoint:

`vgg16_baseline_best.pth`

Training strategy:

| Component | State |
|---|---|
| VGG16 Blocks 1–4 | Frozen |
| VGG16 Block 5 | Trainable |
| Regression Head | Trainable |

## Training Configuration

| Parameter | Value |
|---|---:|
| Epochs | 20 |
| Batch Size | 16 |
| Block5 LR | 1e-5 |
| Head LR | 1e-4 |
| Weight Decay | 1e-5 |
| Loss | L1Loss / MAE |
| Seed | 42 |

## Model Selection

Best epoch:

**12**

Best Validation MAE:

**26.4428 m**

Final checkpoint:

`vgg16_fvei_block5_best.pth`

Training MAE continued to decrease after epoch 12 while validation MAE did not produce a sustained improvement.

This pattern is consistent with mild overfitting after the validation-selected checkpoint.

## Figure

![FVEI fine-tuning curve](../../figures/fvei_finetuning_mae_curve.png)

---

# 7. Locked FVEI Test Evaluation

The final validation-selected checkpoint was evaluated once on the held-out exact-label test split.

Test samples:

**482**

## Final Test Metrics

| Metric | Result |
|---|---:|
| MAE | **25.1347 m** |
| RMSE | **38.4440 m** |
| R² | **0.894442** |
| Bias | **+3.4534 m** |

No model or hyperparameter tuning was performed after these test results were observed.

---

# 8. Level-Wise FVEI Results

| Level | N | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|
| Level 0 | 118 | 11.1879 m | 14.2664 m | +7.5328 m |
| Level 1 | 127 | 12.5699 m | 15.7690 m | -3.7466 m |
| Level 2 | 119 | 21.8013 m | 29.4082 m | +8.4794 m |
| Level 3 | 118 | 55.9664 m | 68.5106 m | +2.0548 m |

Level 3 produced the largest MAE and RMSE.

The relatively small Level 3 mean bias compared with its MAE and RMSE indicates that the larger error cannot be described only as a one-direction systematic offset.

## Figure

![FVEI level-wise errors](../../figures/fvei_levelwise_error_comparison.png)

---

# 9. Level-4 / 500 m Separate Analysis

The 900 images in this group were not included in exact-label MAE, RMSE, or R².

| Metric | Result |
|---|---:|
| Samples | 900 |
| Mean Prediction | 563.4542 m |
| Median Prediction | 559.8888 m |
| Predictions >= 500 m | 840 / 900 |
| Fraction >= 500 m | 93.33% |
| Mean Shortfall Below 500 m | 1.6444 m |

These values are reported separately and should not be interpreted as standard exact-label regression metrics unless the dataset's 500 m label semantics are independently verified.

---

# 10. Final Model

Final real-world model:

**VGG16 FVEI Block5 Fine-Tuned**

Checkpoint:

`vgg16_fvei_block5_best.pth`

Selected epoch:

**12**

Validation MAE:

**26.4428 m**

Held-out Test MAE:

**25.1347 m**

Held-out Test RMSE:

**38.4440 m**

Held-out Test R²:

**0.894442**

Held-out Test Bias:

**+3.4534 m**

---

# 11. Flask Prototype

The Flask prototype uses the final validation-selected FVEI checkpoint.

Model identifier:

**VGG16 FVEI Block5 Fine-Tuned**

Endpoints:

- `GET /`
- `GET /health`
- `POST /predict`

Current automated API test result:

**6 passed**

The API test suite is checkpoint-independent through a deterministic fake predictor, while separate local smoke tests verify inference using the real final checkpoint.

---

# 12. Reproducibility Notes

Random seed 42 was used for the primary experiment configuration.

CUDA training used deterministic settings where supported.

Because `adaptive_avg_pool2d_backward_cuda` does not provide a strict deterministic implementation in the current environment, training uses:

`torch.use_deterministic_algorithms(True, warn_only=True)`

Therefore bit-for-bit identical CUDA reproduction is not guaranteed.

Model checkpoints, datasets, and generated training outputs are intentionally excluded from Git tracking.

---

# 13. Main Final Findings

1. Under the current synthetic FRIDA/FRIDA2 configuration, VGG16 baseline achieved the lowest Test MAE among the evaluated architectures.

2. CBAM slightly reduced validation MAE but did not improve held-out synthetic Test MAE over the VGG16 baseline.

3. SE did not improve either validation or held-out Test MAE over the VGG16 baseline.

4. Auxiliary CIDET and Benchmark-Visibility experiments demonstrated substantial domain and target-range sensitivity.

5. FVEI fine-tuning substantially reduced the error observed in the real-world adaptation experiments.

6. Validation-based selection identified epoch 12 as the final FVEI checkpoint.

7. The locked FVEI exact-label test produced:
   - MAE: **25.1347 m**
   - RMSE: **38.4440 m**
   - R²: **0.894442**
   - Bias: **+3.4534 m**

8. Level 3 remained the most difficult exact-label FVEI visibility group.

9. The final Flask prototype successfully serves the validation-selected FVEI model.

---

# 14. Reporting Status

This document is the consolidated numerical and figure reference for:

- TÜBİTAK final report preparation,
- final presentation material,
- publication-oriented manuscript preparation,
- repository documentation consistency checks.

It does not replace the official TÜBİTAK final report.
