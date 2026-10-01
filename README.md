# Fog Visibility Estimation using Transfer Learning

TÜBİTAK 2209-A kapsamında yürütülen bu araştırma projesi, sisli hava koşullarında görüntü tabanlı **sürekli görüş mesafesi tahmini** için transfer öğrenme tabanlı CNN mimarilerini incelemektedir.

Çalışmada:

- VGG16 ve ResNet50 sentetik FRIDA/FRIDA2 verisi üzerinde karşılaştırıldı.
- VGG16 üzerinde CBAM ve SE attention mekanizmaları değerlendirildi.
- Sentetik aşamada seçilen VGG16 baseline modeli gerçek dünya FVEI verisi üzerinde fine-tune edildi.
- Validation ile seçilen final model bağımsız held-out FVEI test setinde değerlendirildi.
- CIDET ve Benchmark-Visibility deneyleri yardımcı / B-plan domain-shift ve cross-dataset çalışmaları olarak korundu.
- Final FVEI modeli Flask tabanlı web prototipine entegre edildi.

---

# TÜBİTAK 2209-A Araştırma Projesi

## Proje Başlığı

> **Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi**

## Temel Amaçlar

- Görüntülerden metre cinsinden sürekli görüş mesafesi tahmini yapmak
- Transfer öğrenme ile VGG16 ve ResNet50 mimarilerini karşılaştırmak
- Attention mekanizmalarının katkısını incelemek
- Sentetik ve gerçek dünya görüntüleri arasındaki domain shift'i araştırmak
- Gerçek dünya verisi üzerinde kontrollü fine-tuning gerçekleştirmek
- Modeli bağımsız held-out veri üzerinde değerlendirmek
- Eğitilmiş modeli Flask tabanlı çalışan bir prototipe entegre etmek

Birincil model seçim metriği:

> **Mean Absolute Error — MAE**

---

# Güncel Araştırma Akışı

```text
FRIDA / FRIDA2
        ↓
Synthetic Dataset Preparation
        ↓
VGG16 vs ResNet50 Baseline Comparison
        ↓
Synthetic Baseline Selection: VGG16
        ↓
CBAM + SE Attention Experiments
        ↓
VGG16 Baseline Retained
        ↓
FVEI Dataset Audit and Leakage Screening
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

CIDET ve Benchmark-Visibility deneyleri ayrıca yardımcı gerçek dünya ve cross-dataset genelleme çalışmaları olarak repository'de korunmaktadır.

---

# 1. Sentetik Veri — FRIDA / FRIDA2

Kontrollü mimari karşılaştırması FRIDA ve FRIDA2 tabanlı sentetik sis görüntüleri üzerinde gerçekleştirilmiştir.

## Veri Kümesi

| Özellik | Değer |
|---|---:|
| FRIDA temel sahne | 18 |
| FRIDA2 temel sahne | 66 |
| Toplam sahne | 84 |
| Görüş mesafesi seviyesi | 8 |
| Toplam görüntü | 672 |

Görüş mesafesi seviyeleri:

**50, 80, 100, 150, 200, 300, 500 ve 800 metre**

Aynı temel sahneye ait farklı sis seviyelerinin farklı veri split'lerine dağılmasını önlemek için **scene-based splitting** uygulanmıştır.

| Split | Görüntü |
|---|---:|
| Train | 464 |
| Validation | 96 |
| Test | 112 |

Random seed:

**42**

---

# 2. Synthetic Baseline Comparison

ImageNet üzerinde önceden eğitilmiş VGG16 ve ResNet50 modelleri sürekli görüş mesafesi regresyonuna uyarlanmıştır.

## Sonuçlar

| Model | Best Validation MAE | Test MAE |
|---|---:|---:|
| **VGG16** | **69.9705 m** | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

VGG16 mevcut sentetik veri, split ve deney koşullarında daha düşük MAE üretmiştir.

Bu nedenle:

> **Selected Synthetic Baseline: VGG16**

olarak belirlenmiştir.

Bu sonuç VGG16'nın genel olarak ResNet50'den üstün olduğu anlamına gelmemektedir.

---

# 3. Attention Experiments

VGG16 baseline üzerinde iki attention yaklaşımı değerlendirilmiştir:

- **CBAM — Convolutional Block Attention Module**
- **SE — Squeeze-and-Excitation**

## Sentetik Test Sonuçları

| Model | Test MAE |
|---|---:|
| **VGG16 Baseline** | **66.7227 m** |
| VGG16 + CBAM | 67.6214 m |
| VGG16 + SE | 72.4412 m |
| ResNet50 Baseline | 124.6181 m |

Attention mekanizmaları teknik olarak başarıyla uygulanmış olsa da mevcut sentetik test koşullarında VGG16 baseline test MAE değerini iyileştirmemiştir.

Bu nedenle gerçek dünya adaptasyonunun başlangıç checkpoint'i olarak VGG16 baseline korunmuştur.

---

# 4. FVEI Real-World Dataset

FVEI verisine erişim sağlandıktan sonra orijinal ZIP arşivi için ayrı bir audit ve hazırlama pipeline'ı geliştirilmiştir.

## Dataset Audit

| Kategori | Örnek |
|---|---:|
| Retained total | 4109 |
| Exact-label samples | 3209 |
| Level-4 / 500 m analysis group | 900 |
| Conflicting duplicate images rejected | 229 |
| Outside level range rejected | 32 |
| Redundant identical images removed | 130 |

Kaynak ZIP SHA256:

```text
07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d
```

Exact-label visibility seviyeleri:

| Level | Visibility |
|---|---:|
| 0 | 0–49 m |
| 1 | 50–99 m |
| 2 | 100–199 m |
| 3 | 200–499 m |

Level-4 / 500 m örnekleri exact-label regresyon metriklerinden ayrı tutulmaktadır.

> **Not:** Level-4 / 500 m etiketinin ceiling/censored semantiği final bilimsel yayın öncesinde kaynak dokümantasyondan ayrıca doğrulanmalıdır.

---

# 5. FVEI Split Strategy

Exact-label örneklerde visibility-level stratified split uygulanmıştır.

Temel ayarlar:

- Random seed: **42**
- Train target: **70%**
- Validation target: **15%**
- Test target: **15%**

Pre-training similarity screening sonucunda validation tarafındaki iki potansiyel near-duplicate örnek çıkarılmıştır:

- `fog open data/0/0-381-47.jpg`
- `fog open data/1/1-00073-62.jpg`

Test seti değiştirilmemiştir.

## Final Split

| Split | Örnek |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Locked Test | 482 |
| Similarity Exclusions | 2 |
| Level-4 / 500 m Analysis | 900 |

### Exact-Label Level Distribution

| Split | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---:|---:|---:|---:|
| Train | 549 | 592 | 555 | 549 |
| Validation | 117 | 126 | 119 | 118 |
| Test | 118 | 127 | 119 | 118 |

Held-out test split model selection veya hyperparameter tuning sırasında kullanılmamıştır.

---

# 6. FVEI Fine-Tuning

Başlangıç modeli:

```text
vgg16_baseline_best.pth
```

Fine-tuning stratejisi:

```text
VGG16 Blocks 1–4 → Frozen
VGG16 Block 5     → Trainable
Regression Head   → Trainable
```

## Training Configuration

| Ayar | Değer |
|---|---:|
| Epoch | 20 |
| Batch Size | 16 |
| Block 5 Learning Rate | 1e-5 |
| Regression Head Learning Rate | 1e-4 |
| Weight Decay | 1e-5 |
| Loss | L1Loss / MAE |
| Random Seed | 42 |

Trainable parameters:

| Parametre Grubu | Sayı |
|---|---:|
| Block 5 | 7,079,424 |
| Regression Head | 12,911,361 |

Model development sırasında yalnızca FVEI train ve validation split'leri kullanılmıştır.

Held-out test split training pipeline tarafından açılmamıştır.

---

# 7. FVEI Model Selection

20 epoch eğitim sonunda en iyi checkpoint validation MAE üzerinden seçilmiştir.

| Metrik | Sonuç |
|---|---:|
| Best Epoch | **12** |
| Best Validation MAE | **26.4428 m** |

Final checkpoint:

```text
vgg16_fvei_block5_best.pth
```

Epoch 12 sonrasında training MAE düşmeye devam ederken validation MAE kalıcı biçimde iyileşmemiştir.

Bu nedenle final model olarak epoch 20 yerine validation-selected **epoch 12** checkpoint'i kullanılmıştır.

---

# 8. Locked FVEI Test Evaluation

Model seçimi tamamlandıktan sonra epoch 12 checkpoint'i daha önce model selection sırasında kullanılmamış olan 482 görüntülük held-out test split'i üzerinde değerlendirilmiştir.

## Final Test Results

| Metrik | Sonuç |
|---|---:|
| Test Samples | 482 |
| **MAE** | **25.1347 m** |
| **RMSE** | **38.4440 m** |
| **R²** | **0.894442** |
| Bias / Mean Signed Error | **+3.4534 m** |

Validation MAE:

**26.4428 m**

Held-out Test MAE:

**25.1347 m**

Validation ve test MAE değerlerinin birbirine yakın olması, mevcut split koşullarında validation-selected modelin held-out test üzerinde benzer hata düzeyini koruduğunu göstermektedir.

Test sonucu görüldükten sonra model seçimi veya hyperparameter tuning yapılmamıştır.

---

# 9. Level-Wise FVEI Test Results

| Level | N | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|
| Level 0 | 118 | 11.1879 m | 14.2664 m | +7.5328 m |
| Level 1 | 127 | 12.5699 m | 15.7690 m | -3.7466 m |
| Level 2 | 119 | 21.8013 m | 29.4082 m | +8.4794 m |
| Level 3 | 118 | 55.9664 m | 68.5106 m | +2.0548 m |

Level 3 mevcut FVEI held-out testinde en yüksek hata seviyesini üretmiştir.

Level 3 bias değerinin düşük olmasına rağmen MAE ve RMSE değerlerinin yüksek olması, temel problemin yalnızca tek yönlü sistematik bias değil, örnekler arası hata yayılımının artması olduğunu göstermektedir.

---

# 10. Level-4 / 500 m Separate Analysis

900 adet Level-4 / 500 m örneği exact-label MAE, RMSE veya R² hesaplarına dahil edilmemiştir.

| Metrik | Sonuç |
|---|---:|
| Samples | 900 |
| Mean Prediction | 563.4542 m |
| Median Prediction | 559.8888 m |
| Predictions ≥ 500 m | 840 / 900 |
| Fraction ≥ 500 m | 93.33% |
| Mean Shortfall Below 500 m | 1.6444 m |

Bu bölüm separate analysis olarak tutulmaktadır.

Bu grup exact 500 m regression ground truth olarak değerlendirilmemiştir.

---

# 11. Auxiliary / B-Plan Real-World Experiments

FVEI veri erişimi sağlanmadan önce CIDET ve Benchmark-Visibility üzerinde ek deneyler gerçekleştirilmiştir.

Bu çalışmalar silinmemiş ve araştırmanın domain-shift / cross-dataset bulguları olarak korunmuştur.

## CIDET

Synthetic VGG16 modelinin CIDET üzerinde zero-shot aktarımı ciddi domain ve target-range shift göstermiştir.

### CIDET Fine-Tuning Validation Results

| Strateji | Validation MAE |
|---|---:|
| Head-only + L1 | 446.5714 m |
| Block5 + L1 | 326.6640 m |
| Block5 + Balanced Sampling + L1 | 334.9808 m |
| Block5 + Huber | 324.1948 m |

CIDET deneyleri artık final Flask checkpoint seçimi için kullanılmamaktadır.

---

# 12. Benchmark-Visibility Stress Test

CIDET validation aşamasında seçilmiş Block5 + Huber modeli bağımsız Benchmark-Visibility veri setinde ek adaptasyon yapılmadan değerlendirilmiştir.

| Metrik | Sonuç |
|---|---:|
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Mean Signed Error | -11310.9893 m |
| Pearson Correlation | 0.585183 |
| Prediction Range | 97.43–1308.30 m |
| Target Range | 112–20000 m |

Sonuç, geniş target-range değişiminde prediction-range compression ve ciddi sistematik underestimation davranışı göstermiştir.

Bu negatif sonuç model tuning için kullanılmamış, cross-dataset generalization bulgusu olarak korunmuştur.

---

# 13. Final Model

Projenin güncel gerçek dünya inference modeli:

> **VGG16 + FVEI Block5 Fine-Tuning**

Checkpoint:

```text
vgg16_fvei_block5_best.pth
```

Selected Epoch:

**12**

Validation MAE:

**26.4428 m**

Held-Out Test MAE:

**25.1347 m**

Held-Out Test R²:

**0.894442**

---

# 14. Flask Web Prototype

Final FVEI modeli Flask tabanlı web prototipine entegre edilmiştir.

Web uygulaması:

- JPG / JPEG / PNG görüntü yükleme
- Görüntü önizleme
- Model inference
- Metre cinsinden visibility prediction
- REST-style prediction endpoint
- Health endpoint

özelliklerini desteklemektedir.

## Kullanılan Model

```text
VGG16 FVEI Block5 Fine-Tuned
```

## API Endpoints

```text
GET  /
GET  /health
POST /predict
```

`POST /predict` multipart form üzerinden `image` alanı kabul eder.

Örnek response:

```json
{
  "visibility_m": 245.31,
  "unit": "m",
  "model": "VGG16 FVEI Block5 Fine-Tuned",
  "checkpoint_epoch": 12
}
```

Flask API testleri:

```text
4 passed
```

---

# 15. Preprocessing

Ortak inference pipeline:

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

# 16. Reproducibility

Temel random seed:

**42**

Kontrollü deneylerde mümkün olduğu ölçüde:

- sabit veri split'leri
- aynı preprocessing pipeline
- validation-based checkpoint selection
- ayrı training ve evaluation scriptleri
- ayrı checkpoint'ler
- sabit random seed

kullanılmıştır.

GPU eğitimi sırasında VGG16'nın `AdaptiveAvgPool2d` backward CUDA operasyonunun strict deterministic implementation sunmaması nedeniyle:

```python
torch.use_deterministic_algorithms(
    True,
    warn_only=True,
)
```

kullanılmıştır.

Dolayısıyla desteklenen deterministic işlemler korunmuş olsa da GPU training run'larının bit-bit identical olması garanti edilmemektedir.

---

# 17. Technology Stack

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
- OpenCV
- HTML
- CSS
- JavaScript
- Pytest

---

# 18. Repository Structure

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

---

# 19. Important Research Reports

Detaylı araştırma kayıtları `docs/reports/` altında tutulmaktadır.

Önemli raporlar:

- `docs/reports/baseline_comparison.md`
- `docs/reports/attention_comparison.md`
- `docs/reports/se_attention_comparison.md`
- `docs/reports/fvei_real_world_evaluation.md`
- `docs/reports/cidet_real_world_evaluation.md`
- `docs/reports/benchmark_visibility_external_evaluation.md`

Araştırma günlüğü:

```text
docs/research_notes/arastirma_gunlugu.md
```

---

# 20. Current Research Findings

1. VGG16 mevcut sentetik FRIDA/FRIDA2 koşullarında ResNet50'den daha düşük test MAE üretmiştir.

2. Sentetik VGG16 baseline test MAE değeri **66.7227 m**'dir.

3. CBAM ve SE attention mekanizmaları teknik olarak uygulanmış ancak mevcut sentetik test MAE'sini iyileştirmemiştir.

4. Bu nedenle sentetik aşamada VGG16 baseline korunmuştur.

5. FVEI üzerinde Block5 + regression head fine-tuning uygulanmıştır.

6. En iyi FVEI checkpoint validation MAE üzerinden epoch 12'de seçilmiştir.

7. FVEI validation MAE **26.4428 m**'dir.

8. Locked FVEI test MAE **25.1347 m**'dir.

9. Locked FVEI test RMSE **38.4440 m** ve R² **0.894442**'dir.

10. FVEI testinde en yüksek hata Level 3 grubunda gözlenmiştir.

11. CIDET deneyleri sentetik → gerçek dünya domain shift'in güçlü olabileceğini göstermiştir.

12. Benchmark-Visibility deneyleri büyük target-range değişiminde cross-dataset calibration problemini göstermiştir.

13. Final Flask prototipi artık CIDET checkpoint'i yerine **FVEI final checkpoint'ini** kullanmaktadır.

---

# 21. Completed Work

- [x] Literature review
- [x] FRIDA / FRIDA2 analysis
- [x] Synthetic fog dataset preparation
- [x] Scene-based splitting
- [x] VGG16 baseline
- [x] ResNet50 baseline
- [x] Baseline comparison
- [x] Synthetic model selection
- [x] CBAM implementation and evaluation
- [x] SE implementation and evaluation
- [x] Attention comparison
- [x] CIDET auxiliary real-world experiments
- [x] Benchmark-Visibility external stress test
- [x] FVEI dataset audit
- [x] FVEI duplicate and similarity screening
- [x] FVEI reproducible split
- [x] FVEI DataLoader
- [x] FVEI fine-tuning pipeline
- [x] GPU fine-tuning
- [x] Validation-based FVEI model selection
- [x] Locked FVEI final test
- [x] Level-wise FVEI error analysis
- [x] Level-4 / 500 m separate analysis
- [x] Final FVEI inference wrapper
- [x] Flask inference API
- [x] Web interface
- [x] Flask API tests
- [x] FVEI research report

---

# 22. Remaining Work

Ana deneysel model geliştirme aşaması tamamlanmıştır.

Kalan temel çalışmalar:

- [ ] Araştırma günlüğünü final FVEI aşamasına kadar güncellemek
- [ ] Weekly progress documentation'ı güncellemek
- [ ] Final TÜBİTAK project report
- [ ] Final result tables and figures
- [ ] Publication-oriented manuscript
- [ ] Final repository documentation polish

FHVI verisine ek erişim sağlanması durumunda ayrı bir external real-world evaluation gelecekte eklenebilir.

---

# 23. Methodological Notes

Sonuçlar yorumlanırken:

- Sentetik ve gerçek dünya MAE değerleri doğrudan aynı veri dağılımının performansı olarak karşılaştırılmamalıdır.
- FVEI test seti model selection sırasında kullanılmamıştır.
- FVEI test sonucu görüldükten sonra checkpoint veya hyperparameter tuning yapılmamıştır.
- FVEI split'i visibility level bazında stratified olarak oluşturulmuştur.
- Güvenilir scene/camera identity bilgisi mevcut FVEI pipeline'ında kullanılabilir durumda değildir.
- Similarity screening uygulanmış olsa da residual sample dependence tamamen dışlanamaz.
- İki validation örneği similarity screening sonucunda çıkarılmış, test split değiştirilmemiştir.
- Tek temel split ve seed kullanılmıştır.
- Bazı CUDA operasyonları strict deterministic değildir.
- Level-4 / 500 m semantiği final yayın öncesinde kaynak dokümantasyonla ayrıca doğrulanmalıdır.
- CIDET ve Benchmark sonuçları FVEI final model seçimini etkilememektedir.

---

# 24. Disclaimer

Bu repository, TÜBİTAK 2209-A kapsamında geliştirilen akademik bir araştırma projesidir.

Model performansı kullanılan veri dağılımına, kamera koşullarına ve visibility range'e bağlıdır.

Flask prototipi bir araştırma demonstrasyonudur ve sertifikalı meteorolojik görüş sensörünün yerine geçmez.

Repository'de raporlanan MAE, RMSE ve R² değerleri ilgili deney veri setlerinin toplu performans metrikleridir; tek bir yüklenen görüntü için garanti edilen hata payı değildir.

---

# License and Dataset Usage

Bu proje TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı kapsamında akademik araştırma amacıyla geliştirilmektedir.

Üçüncü taraf veri setlerinin kendi lisans, kullanım ve atıf koşulları geçerlidir.

Repository kapsamında proje için özgün olarak geliştirilen yazılım ve dokümantasyon **MIT License** altında lisanslanmıştır.

Üçüncü taraf veri setleri, pretrained model bileşenleri ve diğer harici kaynaklar MIT License kapsamında yeniden lisanslanmamaktadır.
