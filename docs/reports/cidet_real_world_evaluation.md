@'
# CIDET Real-World Evaluation Report

## 1. Purpose

This experiment evaluates the transfer of the synthetic-data-trained VGG16 visibility regression model to a real-world visibility estimation domain.

The synthetic baseline was previously trained and selected using FRIDA/FRIDA2. VGG16 achieved the lowest synthetic test MAE among the evaluated baseline and attention variants and was therefore selected as the synthetic baseline for subsequent real-world adaptation experiments.

CIDET is used here to measure:

1. zero-shot synthetic-to-real transfer,
2. real-world adaptation through regression-head fine-tuning,
3. generalization on a temporally separated CIDET test set,
4. visibility-dependent error behavior.

The CIDET-adapted model is not treated as the final project model at this stage.

---

## 2. CIDET Dataset

Dataset:

Estimation of Atmospheric Visibility by Deep Learning Model Using Multimodal Dataset

Zenodo DOI:

10.5281/zenodo.15494899

License:

CC BY 4.0

CIDET contains RGB images captured by a fixed surveillance camera together with meteorological information and manually estimated visibility distances.

Visibility annotations were produced using fixed reference points and two independent observers.

The downloaded image archive contained 1000 JPG images.

The annotation table contained 980 annotated records.

After validating image/annotation availability, the official split files contained 977 usable image-annotation pairs.

Observer agreement analysis on the 977 usable samples showed:

- Mean absolute observer disagreement: 158.04 m
- Median absolute disagreement: 0.00 m
- 95th percentile disagreement: 524.00 m
- Maximum disagreement: 746.00 m
- Pearson correlation between observers: 0.9808

These values indicate that annotation uncertainty should be considered when interpreting regression errors.

---

## 3. Temporal Split Strategy

CIDET provides an official train/validation/test split.

However, an audit identified substantial temporal proximity between samples belonging to different official subsets.

Observed date overlap:

- Train-validation overlapping dates: 97
- Train-test overlapping dates: 99
- Validation-test overlapping dates: 51

Cross-split temporal proximity analysis also found many samples captured within short time intervals of samples in another subset.

To obtain a stricter estimate of temporal generalization, a deterministic calendar-day-grouped split was therefore created.

All images from the same calendar date are assigned to exactly one subset.

The split was generated using seed 42 and a deterministic multi-start search designed to approximately preserve the requested 70/15/15 proportions while balancing visibility distributions.

Final temporal split:

| Split | Samples | Percentage | Unique Dates |
|---|---:|---:|---:|
| Train | 685 | 70.11% | 188 |
| Validation | 147 | 15.05% | 42 |
| Test | 145 | 14.84% | 47 |

Calendar-date overlap between all subsets is zero.

The test subset was excluded from model training and checkpoint selection.

---

## 4. Synthetic-to-Real Zero-Shot Evaluation

The selected synthetic VGG16 baseline was first evaluated directly on the CIDET temporal test subset without CIDET training.

Results:

- Test samples: 145
- MAE: 2258.89 m
- RMSE: 2472.92 m
- Median absolute error: 2778.41 m
- Mean signed error: -2258.89 m
- Maximum absolute error: 3463.21 m
- Target range: 345-3915 m
- Prediction range: 279.53-486.53 m

The synthetic model strongly underestimated real-world visibility.

This result demonstrates a substantial synthetic-to-real domain and target-range shift.

The FRIDA/FRIDA2 synthetic training target range was limited to 50-800 m, whereas CIDET contains substantially larger visibility distances.

Therefore, the zero-shot CIDET result should not be directly compared with the synthetic test MAE as if both evaluations represented the same target distribution and difficulty.

---

## 5. CIDET Regression-Head Fine-Tuning

The synthetic VGG16 checkpoint was subsequently adapted using the CIDET temporal training subset.

To remain consistent with the transfer-learning methodology, the convolutional feature extractor was frozen and only the regression classifier was optimized.

Training configuration:

- Initialization: synthetic VGG16 checkpoint
- Backbone: frozen
- Trainable component: regression classifier
- Loss: L1 / MAE
- Optimizer: Adam
- Learning rate: 1e-4
- Weight decay: 1e-5
- Batch size: 16
- Maximum epochs: 20
- Random seed: 42
- Model selection criterion: validation MAE

The best validation checkpoint occurred at epoch 20.

Best validation MAE:

446.57 m

The held-out test subset was not used for training or checkpoint selection.

---

## 6. Fine-Tuned Test Performance

The best validation-selected checkpoint was evaluated on the temporal test subset.

Results:

- Test samples: 145
- MAE: 554.19 m
- RMSE: 736.91 m
- Median absolute error: 361.87 m
- Mean signed error: +159.79 m
- Maximum absolute error: 2116.02 m
- Pearson correlation: 0.7203
- Target range: 345-3915 m
- Prediction range: 950.32-3735.42 m

Compared with the zero-shot model, CIDET adaptation reduced MAE from 2258.89 m to 554.19 m.

This corresponds to an MAE reduction of approximately 75.47%.

The large improvement confirms that real-world domain adaptation is necessary when transferring the synthetic visibility model to CIDET.

However, the current real-world MAE remains above the project target of less than 100 m.

The <100 m criterion therefore remains an unmet research target rather than being redefined or removed.

---

## 7. Error Analysis by Visibility Range

Post-hoc analysis of the locked temporal test predictions produced the following results:

| True Visibility | n | MAE | RMSE | Median AE | Bias |
|---|---:|---:|---:|---:|---:|
| <500 m | 3 | 1331.93 m | 1339.50 m | 1396.62 m | +1331.93 m |
| 500-999 m | 27 | 1182.74 m | 1285.31 m | 1197.72 m | +1182.74 m |
| 1000-1999 m | 0 | N/A | N/A | N/A | N/A |
| 2000-2999 m | 28 | 529.11 m | 589.94 m | 617.72 m | +361.10 m |
| >=3000 m | 87 | 340.37 m | 467.41 m | 198.25 m | -262.88 m |

The dominant failure mode is strong overestimation in low-visibility conditions.

Samples below 1000 m have substantially larger errors than high-visibility samples.

The >=3000 m subset performs considerably better, with an MAE of 340.37 m and median absolute error of 198.25 m.

No samples in the temporal test subset fall within the 1000-1999 m interval. Therefore, no performance conclusion can be made for that visibility range.

The prediction range remains inside the observed test target range, but the minimum prediction of approximately 950 m indicates limited sensitivity to the lowest visibility conditions.

---

## 8. Interpretation

The CIDET experiments establish three main findings.

First, the synthetic VGG16 model does not transfer directly to CIDET. The zero-shot MAE of 2258.89 m demonstrates severe domain and target-range shift.

Second, real-world regression-head adaptation substantially improves performance. Fine-tuning reduces MAE by approximately 75.47% and increases the usable prediction range.

Third, the remaining error is strongly visibility-dependent. Low-visibility conditions below 1000 m remain the principal weakness of the current model.

The current result must therefore be treated as a real-world adaptation baseline rather than the final optimized model.

---

## 9. Limitations

The experiment has several limitations:

- CIDET contains a limited number of low-visibility samples in the held-out temporal test subset.
- The 1000-1999 m interval is absent from the temporal test subset.
- Visibility labels are manually estimated and exhibit measurable inter-observer disagreement.
- Calendar-day grouping removes same-date overlap but does not guarantee complete independence between nearby dates.
- Only one deterministic seed/split is currently evaluated.
- The current adaptation freezes the complete convolutional backbone.
- Statistical significance is not claimed from the current single-split experiment.

---

## 10. Next Research Stage

The current CIDET test results are treated as locked post-hoc evaluation results and will not be used directly for hyperparameter selection.

Further controlled real-world adaptation experiments will use the training and validation subsets for development.

The next planned experiment is gradual VGG16 adaptation by unfreezing the final convolutional block while retaining a lower learning rate for transferred convolutional parameters.

The objective remains to reduce real-world validation error and investigate whether the project target of MAE < 100 m can be approached under a scientifically defensible evaluation protocol.

Independent real-world evaluation using an additional visibility dataset is planned after the CIDET adaptation stage.

The project target of MAE < 100 m remains active. If it cannot be reached, the final report will transparently document the achieved performance, dataset limitations, domain-shift effects, and error characteristics.
'@ | Set-Content -Path ".\docs\reports\cidet_real_world_evaluation.md" -Encoding UTF8