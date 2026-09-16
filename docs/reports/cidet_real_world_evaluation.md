# CIDET Real-World Evaluation Report

## 1. Purpose

This stage evaluates the transfer of the synthetic-data-trained VGG16 visibility regression model to a real-world visibility estimation domain and investigates controlled adaptation strategies using CIDET.

The synthetic baseline was previously trained and selected using FRIDA/FRIDA2. VGG16 achieved the lowest synthetic test MAE among the evaluated baseline and attention variants and was therefore selected as the synthetic baseline for subsequent real-world adaptation experiments.

CIDET is used to investigate:

1. zero-shot synthetic-to-real transfer,
2. proposal-aligned regression-head fine-tuning,
3. controlled partial-backbone adaptation,
4. alternative sampling and loss strategies using the training and validation subsets,
5. visibility-dependent and condition-dependent error behavior.

The CIDET-adapted configurations are treated as real-world adaptation experiments rather than final independent generalization results.

---

## 2. CIDET Dataset

Dataset:

**Estimation of Atmospheric Visibility by Deep Learning Model Using Multimodal Dataset**

Zenodo DOI:

**10.5281/zenodo.15494899**

License:

**CC BY 4.0**

CIDET contains RGB images captured by a fixed surveillance camera together with meteorological information and manually estimated visibility distances.

The tabular data include:

- absolute pressure,
- temperature,
- relative humidity,
- dew point,
- wet-bulb temperature,
- average wind speed,
- high wind speed,
- rainfall,
- solar radiation,
- UV index,
- visibility estimates from two observers,
- average visibility estimate.

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

These values indicate that annotation uncertainty should be considered when interpreting regression errors, particularly relative to the project target of MAE < 100 m.

---

## 3. Temporal Split Strategy

CIDET provides an official train/validation/test split.

However, an audit identified substantial temporal proximity between samples belonging to different official subsets.

Observed date overlap:

- Train-validation overlapping dates: 97
- Train-test overlapping dates: 99
- Validation-test overlapping dates: 51

Cross-split temporal proximity analysis also identified many samples captured within short time intervals of samples assigned to another subset.

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

## 5. Proposal-Aligned Regression-Head Fine-Tuning

The synthetic VGG16 checkpoint was subsequently adapted using the CIDET temporal training subset.

To remain consistent with the detailed transfer-learning methodology, the convolutional feature extractor was frozen and only the regression classifier was optimized.

Training configuration:

- Initialization: synthetic VGG16 checkpoint
- Backbone: completely frozen
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

**446.5714 m**

This configuration serves as the proposal-aligned real-world adaptation baseline.

---

## 6. Regression-Head Fine-Tuned Test Performance

The best validation-selected regression-head checkpoint was evaluated on the temporal test subset.

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

The large improvement demonstrates the importance of real-world domain adaptation when transferring the synthetic visibility model to CIDET.

However, the resulting MAE remains above the project target of less than 100 m.

The <100 m criterion therefore remains an unmet research target rather than being redefined or removed.

---

## 7. Initial Test-Set Error Analysis

Post-hoc analysis of the regression-head model's temporal test predictions produced the following results:

| True Visibility | n | MAE | RMSE | Median AE | Bias |
|---|---:|---:|---:|---:|---:|
| <500 m | 3 | 1331.93 m | 1339.50 m | 1396.62 m | +1331.93 m |
| 500-999 m | 27 | 1182.74 m | 1285.31 m | 1197.72 m | +1182.74 m |
| 1000-1999 m | 0 | N/A | N/A | N/A | N/A |
| 2000-2999 m | 28 | 529.11 m | 589.94 m | 617.72 m | +361.10 m |
| >=3000 m | 87 | 340.37 m | 467.41 m | 198.25 m | -262.88 m |

The regression-head model strongly overestimated low-visibility samples.

No samples in the temporal test subset fall within the 1000-1999 m interval. Therefore, no performance conclusion can be made for that visibility range.

Because this post-hoc test analysis had already been inspected before subsequent adaptation experiments were designed, later development is performed using the training and validation subsets only. No subsequent model variant is selected using its CIDET test performance.

Independent external real-world evaluation is therefore important for the final generalization assessment.

---

## 8. Controlled Partial-Backbone Adaptation

A secondary adaptation experiment investigated whether allowing the final VGG16 convolutional block to adapt to CIDET could reduce the remaining real-world domain gap.

This experiment extends beyond the strict regression-head-only baseline and is therefore treated as a controlled secondary adaptation experiment rather than as an identical implementation of the original baseline protocol.

Configuration:

- Initialization: original synthetic VGG16 checkpoint
- VGG16 Blocks 1-4: frozen
- VGG16 Block 5: trainable
- Regression classifier: trainable
- Block 5 learning rate: 1e-5
- Regression-head learning rate: 1e-4
- Weight decay: 1e-5
- Loss: L1 / MAE
- Maximum epochs: 20
- Random seed: 42
- Model selection: validation MAE
- CIDET test used for selection: no

The best checkpoint occurred at epoch 11.

Best validation MAE:

**326.6640 m**

Compared with the proposal-aligned regression-head baseline of 446.5714 m, partial Block 5 adaptation reduced validation MAE by 119.9074 m, corresponding to approximately 26.85%.

This provides evidence on the current split that limited adaptation of transferred convolutional features is useful for reducing the CIDET domain gap.

---

## 9. Balanced-Sampling Experiment

The CIDET training distribution is concentrated at high visibility.

Training-set distribution:

| Visibility Range | Samples |
|---|---:|
| <500 m | 54 |
| 500-999 m | 91 |
| 1000-1999 m | 0 |
| 2000-2999 m | 137 |
| >=3000 m | 403 |

Approximately 58.8% of the training samples are in the >=3000 m range.

To test whether this imbalance was responsible for the remaining validation error, an inverse-bin-frequency weighted sampler was evaluated.

The experiment retained the same synthetic initialization, Block 5 adaptation strategy, learning rates, L1 loss, seed, and maximum number of epochs. Only the training sampler was changed.

The best checkpoint occurred at epoch 13.

Best validation MAE:

**334.9808 m**

This was 8.3168 m higher than the standard-sampling Block 5 result of 326.6640 m, corresponding to approximately 2.55% worse validation MAE.

Balanced sampling therefore did not improve the primary validation metric in this controlled experiment and was not selected as the preferred sampling strategy.

The result is retained as a negative experimental finding.

---

## 10. Huber-Loss Experiment

Validation residual analysis of the standard Block 5 model showed a median absolute error of 234.20 m together with a small number of substantially larger residuals.

A controlled loss-function experiment therefore replaced L1 loss with Smooth L1 / Huber loss using beta = 200 m.

All other major experimental conditions were retained:

- Initialization: original synthetic VGG16 checkpoint
- Blocks 1-4: frozen
- Block 5: trainable
- Regression classifier: trainable
- Block 5 learning rate: 1e-5
- Regression-head learning rate: 1e-4
- Weight decay: 1e-5
- Sampling strategy: standard
- Huber beta: 200 m
- Maximum epochs: 20
- Random seed: 42
- Checkpoint selection metric: true validation MAE
- CIDET test used for selection: no

The best checkpoint occurred at epoch 12.

Best validation MAE:

**324.1948 m**

This is 2.4692 m lower than the standard Block 5 L1 result of 326.6640 m, corresponding to approximately 0.76%.

The Huber configuration therefore produced the lowest validation MAE observed among the controlled CIDET adaptation experiments so far.

However, the difference from standard Block 5 L1 is small and comes from a single deterministic split and seed. No statistical-significance or general-superiority claim is made.

---

## 11. Validation Comparison

The controlled CIDET adaptation experiments currently produce the following validation results:

| Configuration | Best Epoch | Validation MAE |
|---|---:|---:|
| Regression head only + L1 | 20 | 446.5714 m |
| Block 5 + L1 + standard sampling | 11 | 326.6640 m |
| Block 5 + L1 + balanced sampling | 13 | 334.9808 m |
| Block 5 + Huber beta=200 + standard sampling | 12 | **324.1948 m** |

The largest observed improvement resulted from partially unfreezing VGG16 Block 5.

Balanced sampling did not improve validation MAE.

Huber loss produced an additional but comparatively small reduction in validation MAE.

The Huber configuration is therefore retained as the current CIDET development candidate because it has the lowest observed validation MAE, not because superiority has been established statistically.

---

## 12. Huber Validation Error Analysis

The validation-selected Huber checkpoint was analyzed on the 147-sample validation subset.

Results:

- MAE: 324.1948 m
- RMSE: 490.3078 m
- Median absolute error: 211.4893 m
- Mean signed error: -53.6124 m
- Pearson correlation: 0.897810
- Target range: 345-3915 m
- Prediction range: 240.54-3903.39 m

Visibility-range results:

| True Visibility | n | MAE | Median AE | Bias |
|---|---:|---:|---:|---:|
| <500 m | 6 | 110.38 m | 120.29 m | +110.38 m |
| 500-999 m | 24 | 306.05 m | 214.51 m | +99.63 m |
| 1000-1999 m | 0 | N/A | N/A | N/A |
| 2000-2999 m | 30 | 428.03 m | 391.27 m | +176.36 m |
| >=3000 m | 87 | 308.14 m | 193.41 m | -186.50 m |

Compared with the standard Block 5 L1 configuration, Huber loss reduced overall validation MAE from 326.6640 m to 324.1948 m and reduced median absolute error from 234.1956 m to 211.4893 m.

However, RMSE increased slightly from 484.9354 m to 490.3078 m.

Therefore, Huber loss improved typical residual magnitude but did not eliminate the largest validation outliers.

---

## 13. Temporal and Qualitative Failure Analysis

Validation errors were also aggregated by calendar date.

The largest day-level error occurred on 2023-12-03:

- Samples: 3
- Mean target visibility: 3752.67 m
- Mean predicted visibility: 1820.02 m
- MAE: 1932.65 m
- Mean signed error: -1932.65 m

Other dates also exhibited substantial systematic errors in either direction.

Examples include:

- 2023-11-25: MAE 912.11 m, bias -912.11 m
- 2023-12-20: MAE 675.35 m, bias +544.88 m
- 2023-12-07: MAE 597.49 m, bias -597.49 m
- 2023-09-02: MAE 537.18 m, bias +530.96 m
- 2023-11-13: MAE 528.55 m, bias +491.81 m

This indicates that residuals are not uniformly distributed across calendar conditions.

A qualitative comparison between high-error and low-error validation images showed that the model is capable of accurately estimating both high-visibility and severe low-visibility scenes.

For example, one validation image with a target visibility of 345 m was predicted at approximately 353 m.

Conversely, several visually clear high-visibility winter scenes from 2023-12-03 were substantially underestimated.

The inspected high-error images include variations in snow cover, illumination, cloud conditions, scene contrast, and seasonal appearance.

These observations suggest that environmental and appearance-related factors may act as visual confounders.

However, the qualitative analysis is exploratory and does not establish a causal relationship between any specific visual condition and model error.

---

## 14. Meteorological Association Analysis

CIDET provides meteorological measurements aligned with the camera observations.

All 147 Huber validation predictions were successfully matched with meteorological records.

Spearman correlations with absolute error were:

| Variable | Spearman rho |
|---|---:|
| Average wind speed | +0.2810 |
| High wind speed | +0.2098 |
| Humidity | +0.1904 |
| Temperature | -0.1681 |
| Wet-bulb temperature | -0.1664 |
| Solar radiation | -0.1576 |
| Dew point | -0.1555 |
| UV index | -0.1543 |
| Rain | +0.1325 |
| Absolute pressure | +0.0323 |

The strongest observed association with absolute error was average wind speed at rho = 0.2810, which is not sufficiently strong to identify a single meteorological explanation for the model failures.

Signed error showed somewhat stronger associations with several variables, including:

- Dew point: +0.3658
- Average wind speed: -0.3396
- Temperature: +0.3369
- Wet-bulb temperature: +0.3360
- High wind speed: -0.3242

These associations indicate that meteorological conditions may be related to the direction of prediction error.

However, the meteorological variables are not independent, and correlation does not establish causation. These findings are therefore treated as exploratory error analysis rather than evidence that a specific meteorological variable causes model failure.

---

## 15. Interpretation

The CIDET stage currently supports several findings.

First, direct synthetic-to-real transfer is inadequate. The synthetic VGG16 model produced a zero-shot CIDET MAE of 2258.89 m, demonstrating substantial domain and target-range shift.

Second, real-world adaptation is essential. Proposal-aligned regression-head fine-tuning substantially reduced error relative to zero-shot transfer.

Third, allowing controlled adaptation of the final VGG16 convolutional block produced the largest subsequent validation improvement, reducing validation MAE from 446.5714 m to 326.6640 m.

Fourth, inverse-bin-frequency balanced sampling did not improve validation MAE under the evaluated configuration.

Fifth, Huber loss produced the lowest validation MAE observed so far at 324.1948 m, but its improvement over standard Block 5 L1 training was only 2.4692 m. This small difference is not interpreted as evidence of statistically significant superiority.

Finally, the remaining errors are condition-dependent rather than being explained solely by visibility range. Large residuals cluster on particular dates and occur in both positive and negative directions. Qualitative and meteorological analyses suggest possible environmental confounding, but no causal mechanism has been established.

---

## 16. Evaluation-Protocol Considerations

The regression-head CIDET test set was evaluated once and subsequently subjected to post-hoc error analysis.

That analysis informed the broader investigation of real-world adaptation weaknesses.

For this reason, subsequent Block 5, balanced-sampling, and Huber experiments are developed and compared using the CIDET training and validation subsets only.

Their CIDET test performance has not been used for model selection.

The current Huber checkpoint should therefore be described as the lowest-validation-MAE CIDET development candidate observed so far, rather than as a definitively superior final model.

Independent external real-world evaluation is preferred for the final assessment of generalization.

---

## 17. Limitations

The current experiments have several limitations:

- CIDET is relatively small for deep-learning adaptation.
- Visibility values are strongly concentrated in the >=3000 m range.
- The 1000-1999 m interval is absent from the temporal validation and test subsets.
- Visibility labels are manually estimated and exhibit measurable inter-observer disagreement.
- Calendar-day grouping removes same-date overlap but does not guarantee complete independence between nearby dates.
- Only one deterministic seed/split has been evaluated.
- The Huber beta value was selected after inspecting validation residual characteristics.
- Multiple development decisions have therefore been informed by the same validation subset.
- The initial regression-head test results were inspected before later adaptation experiments were designed.
- Meteorological correlation and qualitative image inspection are exploratory and do not establish causality.
- Statistical significance is not claimed from the current experiments.

---

## 18. Current Research Decision

The Block 5 + Huber beta=200 configuration is retained as the current CIDET development candidate because it achieved the lowest observed validation MAE:

**324.1948 m**

No additional CIDET model variant is introduced immediately.

This decision limits further adaptation to the same validation subset and reduces the risk of repeatedly optimizing against validation-specific characteristics.

The CIDET test subset remains unused for evaluation of the later Block 5, balanced-sampling, and Huber variants.

Independent real-world evaluation using an additional visibility dataset is planned for the final generalization stage.

The project target of MAE < 100 m remains active.

The current CIDET validation result does not meet that target.

If the target cannot be reached under a scientifically defensible protocol, the final report will transparently document the achieved performance, annotation uncertainty, domain-shift effects, and observed failure modes.
