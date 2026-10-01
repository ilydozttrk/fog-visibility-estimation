# Fog Visibility Estimation using Transfer Learning

TÜBİTAK 2209-A kapsamında yürütülen bu araştırma projesi, sisli hava koşullarında görüntü tabanlı **sürekli görüş mesafesi tahmini** için transfer öğrenme tabanlı CNN mimarilerini incelemektedir.

> **Project Status: Core research and software development completed.**

Çalışma kapsamında VGG16 ve ResNet50 mimarileri karşılaştırılmış, CBAM ve SE attention mekanizmaları değerlendirilmiş, seçilen VGG16 modeli gerçek dünya FVEI verisi üzerinde fine-tune edilmiş ve validation ile seçilen nihai model bağımsız held-out test setinde değerlendirilmiştir.

Final model Flask tabanlı web prototipine entegre edilmiştir.

---

# TÜBİTAK 2209-A Research Project

## Project Title

> **Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi**

## Project Status

**Teknik geliştirme tamamlandı.**

Tamamlanan ana aşamalar:

- FRIDA / FRIDA2 veri hazırlama
- VGG16 baseline
- ResNet50 baseline
- Baseline comparison
- CBAM attention
- SE attention
- CIDET auxiliary real-world experiments
- Benchmark-Visibility stress test
- FVEI dataset audit
- FVEI similarity screening
- FVEI reproducible split
- FVEI fine-tuning
- Validation-based checkpoint selection
- Locked held-out FVEI test
- Level-wise error analysis
- Flask API
- Web interface
- Checkpoint-independent automated API tests
- Real-checkpoint end-to-end inference test
- Final result tables
- Final result figures
- Research journal
- Weekly progress documentation
- Final results summary
- TÜBİTAK final report drafts
- Repository-wide quality control

Proje şu anda **final raporlama, danışman kontrolü ve yayın hazırlığı** aşamasındadır.

---

# Final Model

Final real-world inference model:

> **VGG16 FVEI Block5 Fine-Tuned**

Checkpoint:

```text
vgg16_fvei_block5_best.pth
```

Selected epoch:

**12**

## Final FVEI Results

| Metric | Result |
|---|---:|
| Validation MAE | **26.4428 m** |
| Held-Out Test MAE | **25.1347 m** |
| Held-Out Test RMSE | **38.4440 m** |
| Held-Out Test R² | **0.894442** |
| Held-Out Test Bias | **+3.4534 m** |
| Test Samples | **482** |

The held-out test split was not used during checkpoint selection or hyperparameter tuning.

No additional model tuning was performed after observing the final test results.

---

# Research Objectives

The main objectives of the project were:

1. Estimate continuous visibility distance from foggy images.
2. Adapt VGG16 and ResNet50 using transfer learning.
3. Compare the architectures using MAE.
4. Evaluate attention mechanisms on the selected baseline.
5. Examine synthetic-to-real domain shift.
6. Fine-tune the selected model using real-world data.
7. Evaluate the final model on an independent held-out test set.
8. Integrate the final model into a functional Flask prototype.

Primary model-selection metric:

> **Mean Absolute Error — MAE**

---

# Research Workflow

```text
FRIDA / FRIDA2
        ↓
Synthetic Dataset Preparation
        ↓
Scene-Based Split
        ↓
VGG16 Baseline
        ↓
ResNet50 Baseline
        ↓
Baseline Comparison
        ↓
Selected Synthetic Baseline: VGG16
        ↓
CBAM Attention
        ↓
SE Attention
        ↓
VGG16 Baseline Retained
        ↓
CIDET / Benchmark Auxiliary Experiments
        ↓
FVEI Dataset Audit
        ↓
FVEI Similarity Screening
        ↓
FVEI Train / Validation / Locked Test Split
        ↓
VGG16 Block5 + Regression Head Fine-Tuning
        ↓
Validation-Based Checkpoint Selection
        ↓
Locked FVEI Final Test
        ↓
Final FVEI Model
        ↓
Flask Inference Prototype
```

---

# 1. Synthetic Dataset — FRIDA / FRIDA2

The controlled architecture comparison was performed using synthetic fog images derived from FRIDA and FRIDA2.

| Property | Value |
|---|---:|
| FRIDA Base Scenes | 18 |
| FRIDA2 Base Scenes | 66 |
| Total Scenes | 84 |
| Visibility Levels | 8 |
| Total Images | 672 |

Visibility levels:

**50, 80, 100, 150, 200, 300, 500 and 800 metres**

A **scene-based split** was used to reduce the risk of different fog variants of the same scene appearing in different dataset partitions.

## Synthetic Split

| Split | Images |
|---|---:|
| Train | 464 |
| Validation | 96 |
| Test | 112 |

Random seed:

**42**

---

# 2. VGG16 vs ResNet50

ImageNet-pretrained VGG16 and ResNet50 architectures were adapted to continuous visibility regression.

## Baseline Results

| Model | Best Validation MAE | Test MAE |
|---|---:|---:|
| **VGG16** | **69.9705 m** | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

Under the current FRIDA/FRIDA2 experimental configuration, VGG16 produced the lower held-out test MAE.

Selected synthetic baseline:

> **VGG16**

The initial research hypothesis expected ResNet50 to produce the lower error because of its residual architecture. The experimental results did **not** support this hypothesis under the current dataset and training configuration.

This result should not be interpreted as a general claim that VGG16 is superior to ResNet50.

---

# 3. Attention Experiments

Two attention approaches were evaluated on the selected VGG16 baseline:

- **CBAM — Convolutional Block Attention Module**
- **SE — Squeeze-and-Excitation**

## Synthetic Test Results

| Model | Validation MAE | Test MAE |
|---|---:|---:|
| **VGG16 Baseline** | 69.9705 m | **66.7227 m** |
| VGG16 + CBAM | **69.3274 m** | 67.6214 m |
| VGG16 + SE | 70.6083 m | 72.4412 m |
| ResNet50 Baseline | 121.8414 m | 124.6181 m |

CBAM slightly reduced validation MAE but did not improve the held-out synthetic test MAE.

SE also did not improve the baseline result.

Therefore, the original VGG16 baseline checkpoint was retained as the starting point for real-world adaptation.

---

# 4. Synthetic Model Comparison Figure

![Synthetic model comparison](figures/synthetic_model_test_mae_comparison.png)

---

# 5. Auxiliary Real-World Experiments

Before the final FVEI workflow was available, CIDET and Benchmark-Visibility were used as auxiliary real-world experiments.

These experiments were retained because they provide useful evidence about synthetic-to-real domain shift and cross-dataset target-range sensitivity.

They were **not** used to select the final FVEI checkpoint.

## CIDET Zero-Shot Evaluation

Synthetic VGG16 zero-shot MAE:

> **2258.8934 m**

This result showed a substantial domain and target-range shift between the synthetic training setup and CIDET.

## CIDET Fine-Tuning

| Strategy | Validation MAE |
|---|---:|
| Head-only + L1 | 446.5714 m |
| Block5 + L1 | 326.6640 m |
| Block5 + Balanced Sampling + L1 | 334.9808 m |
| Block5 + Huber | **324.1948 m** |

---

# 6. Benchmark-Visibility Stress Test

The CIDET development model was additionally evaluated on Benchmark-Visibility without further adaptation.

| Metric | Result |
|---|---:|
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Mean Signed Error | -11310.9893 m |
| Pearson Correlation | 0.585183 |
| Prediction Range | 97.43–1308.30 m |
| Target Range | 112–20000 m |

The experiment showed substantial prediction-range compression and systematic underestimation under a much broader target range.

This negative result was retained as a cross-dataset generalization finding and was not used for final FVEI model tuning.

---

# 7. FVEI Dataset Audit

After access to FVEI was obtained, a dedicated audit and preparation pipeline was developed for the original ZIP archive.

Source ZIP SHA256:

```text
07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d
```

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

> **Methodological note:** the precise ceiling/censored semantics of the 500 m group should be independently verified from the official dataset documentation before publication.

---

# 8. FVEI Split Strategy

Exact-label samples were split using visibility-level stratification.

Initial target proportions:

```text
Train       70%
Validation  15%
Test        15%
```

Random seed:

**42**

Strict pre-training cross-split similarity screening identified two suspicious validation-side samples:

```text
fog open data/0/0-381-47.jpg
fog open data/1/1-00073-62.jpg
```

These two validation samples were excluded.

The test split was not changed.

## Final FVEI Split

| Split | Samples |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Locked Test | 482 |
| Similarity Exclusions | 2 |
| Level-4 / 500 m Analysis | 900 |

## Exact-Label Level Distribution

| Split | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---:|---:|---:|---:|
| Train | 549 | 592 | 555 | 549 |
| Validation | 117 | 126 | 119 | 118 |
| Test | 118 | 127 | 119 | 118 |

Reliable scene/camera identifiers were not available in the current FVEI pipeline.

Therefore, residual sample dependence cannot be completely excluded even after similarity screening.

---

# 9. FVEI Fine-Tuning

Starting checkpoint:

```text
vgg16_baseline_best.pth
```

Fine-tuning strategy:

```text
VGG16 Blocks 1–4 → Frozen
VGG16 Block 5     → Trainable
Regression Head   → Trainable
```

## Training Configuration

| Parameter | Value |
|---|---:|
| Epochs | 20 |
| Batch Size | 16 |
| Block 5 Learning Rate | 1e-5 |
| Regression Head Learning Rate | 1e-4 |
| Weight Decay | 1e-5 |
| Loss | L1Loss / MAE |
| Random Seed | 42 |

Trainable parameters:

| Parameter Group | Count |
|---|---:|
| Block 5 | 7,079,424 |
| Regression Head | 12,911,361 |

Only the train and validation splits were used during development.

The locked test split remained unavailable to the training pipeline.

---

# 10. FVEI Model Selection

The checkpoint was selected using validation MAE.

| Metric | Result |
|---|---:|
| Best Epoch | **12** |
| Best Validation MAE | **26.4428 m** |

Final checkpoint:

```text
vgg16_fvei_block5_best.pth
```

Training MAE continued to decrease after epoch 12, while validation MAE did not show a sustained improvement.

This behaviour is consistent with mild overfitting after the validation-selected checkpoint.

## Fine-Tuning Curve

![FVEI fine-tuning curve](figures/fvei_finetuning_mae_curve.png)

---

# 11. Locked FVEI Test Evaluation

After checkpoint selection was completed, the validation-selected epoch 12 checkpoint was evaluated on the previously unused 482-image exact-label test split.

## Final Test Results

| Metric | Result |
|---|---:|
| Test Samples | 482 |
| **MAE** | **25.1347 m** |
| **RMSE** | **38.4440 m** |
| **R²** | **0.894442** |
| Bias / Mean Signed Error | **+3.4534 m** |

Validation MAE:

> **26.4428 m**

Held-out Test MAE:

> **25.1347 m**

No checkpoint selection, hyperparameter tuning or training-strategy modification was performed after observing the locked test results.

---

# 12. Level-Wise FVEI Test Results

| Level | N | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|
| Level 0 | 118 | 11.1879 m | 14.2664 m | +7.5328 m |
| Level 1 | 127 | 12.5699 m | 15.7690 m | -3.7466 m |
| Level 2 | 119 | 21.8013 m | 29.4082 m | +8.4794 m |
| Level 3 | 118 | 55.9664 m | 68.5106 m | +2.0548 m |

Level 3 produced the highest MAE and RMSE in the current held-out FVEI test.

The relatively small Level 3 bias compared with MAE and RMSE suggests that the larger error is not explained only by a one-direction systematic offset.

## Level-Wise Error Figure

![FVEI level-wise error comparison](figures/fvei_levelwise_error_comparison.png)

---

# 13. Level-4 / 500 m Separate Analysis

The 900 samples in this group were evaluated separately from exact-label MAE, RMSE and R².

| Metric | Result |
|---|---:|
| Samples | 900 |
| Mean Prediction | 563.4542 m |
| Median Prediction | 559.8888 m |
| Predictions ≥ 500 m | 840 / 900 |
| Fraction ≥ 500 m | 93.33% |
| Mean Shortfall Below 500 m | 1.6444 m |

These values are reported separately and are not interpreted as standard exact-label regression metrics.

---

# 14. Flask Web Prototype

The final FVEI checkpoint is integrated into a Flask-based research prototype.

## Final Inference Model

```text
VGG16 FVEI Block5 Fine-Tuned
```

## API Endpoints

```text
GET  /
GET  /health
POST /predict
```

The web application supports:

- JPG / JPEG / PNG upload
- Image preview
- Model inference
- Visibility prediction in metres
- REST-style prediction endpoint
- Health endpoint

Example `/predict` response:

```json
{
  "visibility_m": 245.31,
  "unit": "m",
  "model": "VGG16 FVEI Block5 Fine-Tuned",
  "checkpoint_epoch": 12
}
```

Automated API tests:

> **6 / 6 passed**

The automated API test suite is checkpoint-independent.

A separate local smoke test using the real final checkpoint also verified the full:

```text
upload
  ↓
image decoding
  ↓
preprocessing
  ↓
VGG16 FVEI inference
  ↓
JSON response
```

workflow successfully.

---

# 15. Running the Flask Prototype

Create and activate a Python environment, then install the project dependencies:

```bash
pip install -r requirements.txt
```

The trained checkpoint is intentionally not tracked by Git.

Place the final checkpoint at:

```text
results/checkpoints/vgg16_fvei_block5_best.pth
```

Run the application from the repository root:

```bash
python -m src.api.app
```

Default local address:

```text
http://127.0.0.1:5000
```

Health endpoint:

```text
http://127.0.0.1:5000/health
```

---

# 16. Preprocessing

Common inference pipeline:

```text
RGB Conversion
      ↓
Resize 224 × 224
      ↓
ToTensor
      ↓
ImageNet Normalization
      ↓
VGG16
      ↓
Visibility Regression
```

ImageNet normalization:

```text
Mean = [0.485, 0.456, 0.406]
Std  = [0.229, 0.224, 0.225]
```

---

# 17. Reproducibility

The primary experimental configuration uses:

> **Random Seed: 42**

Reproducibility measures include:

- fixed dataset splits
- common preprocessing
- validation-based checkpoint selection
- separate training and evaluation scripts
- explicit experiment reports
- deterministic settings where supported

During GPU training, strict deterministic execution was not available for every CUDA operation used by VGG16.

The training utilities therefore use:

```python
torch.use_deterministic_algorithms(
    True,
    warn_only=True,
)
```

Bit-for-bit identical GPU reproduction is therefore not guaranteed.

---

# 18. Technology Stack

- Python
- PyTorch
- Torchvision
- Flask
- Pillow
- NumPy
- Pandas
- SciPy
- Scikit-learn
- Matplotlib
- HTML
- CSS
- JavaScript
- Pytest

---

# 19. Repository Structure

```text
.
├── data/
│   ├── generated/
│   ├── interim/
│   ├── processed/
│   ├── raw/
│   └── splits/
├── docs/
│   ├── literature/
│   ├── research_notes/
│   └── reports/
├── figures/
├── notebooks/
├── results/
├── src/
│   ├── api/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── app.py
│   │   └── inference.py
│   ├── data/
│   ├── evaluation/
│   ├── models/
│   └── training/
├── tests/
├── README.md
└── requirements.txt
```

Datasets, checkpoints and generated experiment outputs are intentionally excluded from Git tracking.

---

# 20. Important Research Documents

## Final Project Documents

- [`final_results_summary.md`](docs/reports/final_results_summary.md)
- [`tubitak_final_report_draft.md`](docs/reports/tubitak_final_report_draft.md)
- [`tubitak_final_report_official_format.md`](docs/reports/tubitak_final_report_official_format.md)
- [`weekly_progress_log.md`](docs/reports/weekly_progress_log.md)

## Experiment Reports

- [`baseline_comparison.md`](docs/reports/baseline_comparison.md)
- [`attention_comparison.md`](docs/reports/attention_comparison.md)
- [`se_attention_comparison.md`](docs/reports/se_attention_comparison.md)
- [`fvei_real_world_evaluation.md`](docs/reports/fvei_real_world_evaluation.md)
- [`cidet_real_world_evaluation.md`](docs/reports/cidet_real_world_evaluation.md)
- [`benchmark_visibility_external_evaluation.md`](docs/reports/benchmark_visibility_external_evaluation.md)

## Research Journal

[`docs/research_notes/arastirma_gunlugu.md`](docs/research_notes/arastirma_gunlugu.md)

The final results summary, TÜBİTAK report drafts, weekly progress log and research journal are synchronized with the final technical state of the project.

---

# 21. Main Research Findings

1. VGG16 produced a lower held-out synthetic test MAE than ResNet50 under the current FRIDA/FRIDA2 experimental configuration.

2. The initial hypothesis expecting ResNet50 to outperform VGG16 was not supported.

3. VGG16 synthetic Test MAE was **66.7227 m**.

4. CBAM slightly improved validation MAE but did not improve held-out test MAE.

5. SE did not improve the VGG16 baseline.

6. CIDET experiments demonstrated substantial synthetic-to-real domain shift.

7. Benchmark-Visibility demonstrated major target-range sensitivity and prediction-range compression.

8. FVEI fine-tuning selected epoch 12 using validation MAE.

9. FVEI Validation MAE was **26.4428 m**.

10. Locked FVEI Test MAE was **25.1347 m**.

11. Locked FVEI Test RMSE was **38.4440 m**.

12. Locked FVEI Test R² was **0.894442**.

13. Level 3 was the most difficult exact-label FVEI group.

14. The final Flask prototype uses the validation-selected FVEI checkpoint.

15. The project target of **MAE < 100 m** was achieved in both the selected synthetic baseline and final FVEI evaluation.

---

# 22. Completed Work

- [x] Literature review
- [x] FRIDA / FRIDA2 analysis
- [x] Synthetic dataset preparation
- [x] Scene-based splitting
- [x] VGG16 baseline
- [x] ResNet50 baseline
- [x] Baseline comparison
- [x] Synthetic model selection
- [x] CBAM implementation and evaluation
- [x] SE implementation and evaluation
- [x] Attention comparison
- [x] CIDET auxiliary experiments
- [x] Benchmark-Visibility stress test
- [x] FVEI dataset audit
- [x] Duplicate and similarity screening
- [x] Reproducible FVEI split
- [x] FVEI DataLoader
- [x] FVEI fine-tuning pipeline
- [x] GPU fine-tuning
- [x] Validation-based model selection
- [x] Locked FVEI final test
- [x] Level-wise error analysis
- [x] Level-4 / 500 m separate analysis
- [x] Final FVEI inference wrapper
- [x] Flask API
- [x] Web interface
- [x] Checkpoint-independent Flask tests
- [x] Real-checkpoint inference smoke test
- [x] Final result tables
- [x] Final result figures
- [x] Final results summary
- [x] Research journal update
- [x] Weekly progress log
- [x] Repository quality control
- [x] TÜBİTAK final report content draft
- [x] TÜBİTAK official-format report draft

> **Core research and software development are complete.**

---

# 23. Remaining Work

The remaining tasks are related to **submission and publication preparation**, not core software development.

- [ ] Complete the TÜBİTAK expenditure section using official BİDEB records
- [ ] Complete final date and signature fields
- [ ] Apply advisor revisions
- [ ] Prepare final DOCX / PDF submission files
- [ ] Prepare publication-oriented manuscript

Optional future work:

- [ ] Perform an additional external real-world evaluation if FHVI access becomes available

The current locked FVEI test set should not be reused for future model tuning while still being described as an independent final test set.

---

# 24. Methodological Notes

Results should be interpreted with the following limitations in mind:

- Synthetic and real-world MAE values belong to different data distributions and should not be treated as directly equivalent performance measurements.
- The FVEI locked test split was not used during model selection.
- No additional tuning was performed after observing the locked test result.
- The FVEI split is stratified by visibility level.
- Reliable FVEI scene/camera identity information was not available in the current pipeline.
- Similarity screening reduces but cannot completely eliminate residual sample dependence.
- Two suspicious validation samples were excluded; the test split was not modified.
- The main experiments use one primary split and random seed 42.
- Statistical significance between architectures is not claimed.
- Some CUDA operations are not strictly deterministic.
- Level-4 / 500 m label semantics require independent source verification before publication.
- CIDET and Benchmark results did not influence final FVEI checkpoint selection.

---

# 25. Disclaimer

This repository contains an academic research project developed within the scope of the **TÜBİTAK 2209-A University Students Research Projects Support Program**.

Model performance depends on dataset distribution, camera characteristics, environmental conditions and visibility range.

The Flask application is a research prototype and does not replace a certified meteorological visibility sensor.

Reported MAE, RMSE and R² values represent aggregate dataset-level performance and should not be interpreted as a guaranteed error bound for an individual uploaded image.

---

# License and Dataset Usage

Software and documentation originally developed for this repository are distributed under the **MIT License**.

Third-party datasets, pretrained model components and external resources remain subject to their own licenses, terms of use and citation requirements.

Dataset files and trained checkpoints are not redistributed through this repository.
