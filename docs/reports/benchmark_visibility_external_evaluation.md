# Benchmark-Visibility Independent External Evaluation

## 1. Purpose

This experiment evaluates whether the real-world visibility model selected
during CIDET development generalizes to an independent real-world dataset
without any additional adaptation.

Benchmark-Visibility was used strictly as an external evaluation dataset.

No Benchmark-Visibility sample was used for:

- training,
- fine-tuning,
- calibration,
- hyperparameter tuning,
- checkpoint selection,
- or model selection.

The evaluated checkpoint was fixed before Benchmark-Visibility inference.

---

## 2. Evaluated Model

The evaluated model was:

**VGG16 + Block 5 fine-tuning + Huber loss (beta = 200)**

Checkpoint:

`results/checkpoints/vgg16_cidet_block5_huber_best.pth`

The checkpoint was selected using the CIDET validation split only.

Checkpoint epoch:

**12**

CIDET validation MAE:

**324.1948 m**

This checkpoint represented the lowest validation MAE observed among the
controlled CIDET adaptation experiments before external evaluation.

Benchmark-Visibility results were not used to choose this checkpoint.

---

## 3. Benchmark-Visibility Dataset

Benchmark-Visibility is an independent traffic-road visibility dataset
released with the work:

Y. Wang, L. Zhou, and Z. Xu,
"Traffic Road Visibility Retrieval in the Internet of Video Things through
Physical Feature Based Learning Network,"
IEEE Transactions on Intelligent Transportation Systems,
vol. 26, no. 3, pp. 3629-3642, March 2025.

The released dataset contains traffic-camera frames and corresponding
visibility measurements.

The repository source code identifies the visibility ground truth in metres
and applies an upper visibility threshold of 20,000 m.

The released MATLAB code states that the material is intended for nonprofit
use and requests citation of the associated publication.

### Dataset audit

The downloaded release was audited before evaluation.

- Days: 29
- Images per day: 64
- Total images: 1856
- Total ground-truth values: 1856
- Image/ground-truth count agreement: complete
- Ground-truth variable: `vis_data`
- Ground-truth unit: metres

For every day:

- 64 JPG frames were present,
- `vis_data` contained 64 values,
- the released response file contained 64 values,
- the released feature matrix contained 64 temporal positions,
- and the response values were exactly equal to the raw ground-truth values.

A canonical manifest containing 1856 image/target pairs was generated and
validated before model inference.

Manifest integrity checks confirmed:

- 1856 unique image paths,
- zero missing images,
- 29 dates,
- 64 frames per date,
- frame indices 0-63 for every date,
- monotonically ordered timestamps within each date,
- no duplicate timestamps,
- and finite positive ground-truth values.

---

## 4. Ground-Truth Distribution

The Benchmark-Visibility target distribution was:

| Statistic | Visibility |
|---|---:|
| Minimum | 112.0 m |
| Q1 | 6122.0 m |
| Median | 12562.5 m |
| Mean | 11860.9661 m |
| Q3 | 19046.0 m |
| Maximum | 20000.0 m |

A total of **398 / 1856 samples** were exactly 20,000 m.

The released evaluation code uses 20,000 m as an upper visibility threshold.
Therefore, samples at exactly 20,000 m should be interpreted with awareness
of this ceiling.

---

## 5. Evaluation Protocol

The Benchmark-Visibility images were evaluated using exactly the same image
preprocessing used by the CIDET and synthetic transfer-learning experiments:

1. resize to 224 x 224,
2. convert to tensor,
3. apply ImageNet normalization.

ImageNet normalization:

- mean = `[0.485, 0.456, 0.406]`
- standard deviation = `[0.229, 0.224, 0.225]`

No Benchmark-specific image preprocessing or augmentation was introduced.

The model was executed in evaluation mode without gradient computation.

Evaluation metrics were:

- Mean Absolute Error (MAE),
- Root Mean Squared Error (RMSE),
- Median Absolute Error,
- mean signed error (bias),
- maximum absolute error,
- Pearson correlation,
- visibility-range-specific error,
- and separate analysis of the 20,000 m ceiling samples.

---

## 6. Overall External Evaluation Results

The fixed CIDET-selected model produced:

| Metric | Result |
|---|---:|
| Samples | 1856 |
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Median Absolute Error | 11981.6470 m |
| Mean Signed Error | -11310.9893 m |
| Maximum Absolute Error | 19646.0398 m |
| Pearson Correlation | 0.585183 |

Target range:

**112.0000 - 20000.0000 m**

Prediction range:

**97.4342 - 1308.2968 m**

The strongly negative mean signed error demonstrates systematic
underestimation on this external dataset.

Most importantly, the prediction range remained below approximately 1.31 km
even though Benchmark-Visibility contains ground-truth values up to 20 km.

---

## 7. Error by Visibility Range

| Ground-truth range | n | MAE | Median AE | Bias |
|---|---:|---:|---:|---:|
| <1000 m | 178 | 222.83 m | 169.81 m | -183.30 m |
| 1000-2999 m | 118 | 1513.49 m | 1504.03 m | -1513.49 m |
| 3000-4999 m | 83 | 3604.32 m | 3567.51 m | -3604.32 m |
| 5000-9999 m | 374 | 7172.26 m | 7413.49 m | -7172.26 m |
| 10000-19999 m | 705 | 14318.83 m | 14316.01 m | -14318.83 m |
| 20000 m | 398 | 19360.86 m | 19391.37 m | -19360.86 m |

The range-specific results reveal a clear pattern.

Performance is substantially better in the lowest visibility regime.
For targets below 1000 m, MAE is **222.83 m**.

Error then increases strongly as ground-truth visibility moves beyond the
range represented during CIDET adaptation.

---

## 8. 20,000 m Ceiling Analysis

The dataset contained:

**398 ceiling samples**

For these samples:

- MAE: **19360.8556 m**
- Bias: **-19360.8556 m**

For the remaining 1458 non-ceiling samples:

- MAE: **9118.3892 m**
- Bias: **-9113.5635 m**

The poor overall MAE is therefore not caused exclusively by the 20 km
ceiling samples. Large systematic underestimation remains present even when
those samples are excluded.

---

## 9. Cross-Dataset Target-Range Shift

The external result must be interpreted in relation to the training and
adaptation domains.

The CIDET real-world dataset used for model adaptation has visibility targets
extending to approximately 3.9 km.

Benchmark-Visibility extends to 20 km and has a median target of approximately
12.56 km.

Consequently, a large fraction of Benchmark-Visibility lies far outside the
target range represented during CIDET adaptation.

The external evaluation therefore tests not only visual domain transfer but
also substantial target-range extrapolation.

The model's prediction range of approximately 0.10-1.31 km demonstrates that
the CIDET-adapted regressor does not extrapolate its absolute visibility scale
to the substantially larger Benchmark-Visibility range.

---

## 10. Correlation versus Absolute Calibration

Despite the very large absolute errors, Pearson correlation was:

**0.585183**

This indicates a moderate positive association between predictions and
ground-truth visibility across the external dataset.

However, correlation must not be interpreted as accurate absolute visibility
estimation.

The model exhibits severe negative calibration bias and a compressed
prediction range.

Therefore, the external result suggests that some visibility-related ordering
information transfers across datasets, while absolute metric calibration does
not transfer successfully to the substantially wider Benchmark-Visibility
domain.

---

## 11. Interpretation

The Benchmark-Visibility experiment demonstrates a major limitation of the
current model.

The CIDET-selected model does not provide reliable absolute visibility
estimates across the full 112 m-20 km Benchmark-Visibility range.

The strongest evidence is:

- MAE of 11.31 km,
- mean bias of approximately -11.31 km,
- predictions restricted to approximately 97-1308 m,
- and rapidly increasing error with increasing ground-truth visibility.

At the same time, the experiment does not support the conclusion that the
model learned no transferable visibility information.

For the <1000 m subset, MAE was 222.83 m, and the full dataset retained a
Pearson correlation of 0.585.

A cautious interpretation is therefore that the CIDET-adapted model shows
partial transfer in low-visibility conditions and retains some cross-dataset
visibility ordering, but fails to generalize its absolute metric scale to a
dataset dominated by much larger visibility distances.

---

## 12. Relation to CIDET Results

Benchmark-Visibility and CIDET should not be compared using raw MAE alone.

Their target distributions differ substantially.

CIDET primarily represents visibility distances within approximately the
sub-4 km range, whereas Benchmark-Visibility extends to 20 km and contains a
large proportion of high-visibility observations.

Therefore, the Benchmark experiment is treated as an independent
cross-dataset stress test rather than a direct numerical leaderboard against
CIDET.

---

## 13. Methodological Status

Benchmark-Visibility was evaluated only after the CIDET development candidate
had been fixed.

After observing these external results:

- the Benchmark dataset will not be used to tune the existing checkpoint,
- the checkpoint will not be replaced based on Benchmark performance,
- and the reported external result will be retained as observed.

This preserves the role of Benchmark-Visibility as an independent external
evaluation dataset for the current development cycle.

If additional model development is performed later, its results must be
reported separately and must not retroactively replace this external
evaluation.

---

## 14. Limitations

Several limitations should be considered.

First, the CIDET and Benchmark-Visibility target ranges are substantially
different.

Second, the datasets originate from different cameras, environments,
acquisition conditions, and annotation or measurement procedures.

Third, Benchmark-Visibility contains a 20,000 m upper threshold, meaning the
exact physical visibility above that threshold cannot be distinguished from
the released target value.

Fourth, the current model is a single-image RGB regression model and does not
use the physics-informed features or temporal sequence information included
in the original Benchmark-Visibility methodology.

Finally, this experiment evaluates one checkpoint selected on one CIDET
validation split. It does not establish statistical significance across
multiple seeds or independent training runs.

---

## 15. Current Research Decision

The Benchmark-Visibility external evaluation is retained as a negative but
informative cross-dataset result.

The current CIDET development checkpoint remains:

**VGG16 + Block 5 fine-tuning + Huber loss (beta = 200)**

This designation reflects CIDET validation-based model development and does
not imply successful generalization across the full Benchmark-Visibility
target range.

No Benchmark-driven fine-tuning or calibration will be performed in the
current evaluation cycle.

The external result will be used to document the limitations of
cross-dataset absolute visibility estimation and the importance of
target-range and domain alignment in future work.
