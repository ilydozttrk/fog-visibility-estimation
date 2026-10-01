# FVEI Real-World Evaluation Report

## Proje

**Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi**

TÜBİTAK 2209-A kapsamında sentetik FRIDA/FRIDA2 deneylerinden sonra seçilen VGG16 baseline modelinin gerçek dünya verisine adaptasyonu FVEI veri seti üzerinde gerçekleştirilmiştir.

Bu aşamanın amacı:

- sentetik ortamda seçilen VGG16 baseline modelini gerçek dünya görüntülerine adapte etmek,
- model seçimini yalnızca validation performansı üzerinden yapmak,
- held-out test kümesini model seçimi sırasında kullanmamak,
- final performansı bağımsız FVEI test kümesinde ölçmek,
- 500 m grubunu exact-label regresyon metriklerinden ayrı değerlendirmektir.

---

# 1. Başlangıç Modeli

FVEI fine-tuning için başlangıç noktası olarak sentetik FRIDA/FRIDA2 deneylerinde seçilen VGG16 baseline checkpoint'i kullanılmıştır.

Sentetik VGG16 baseline:

| Metrik | Değer |
|---|---:|
| Best Epoch | 18 |
| Validation MAE | 69.9705 m |
| Test MAE | 66.7227 m |

CBAM ve SE attention deneyleri sentetik test MAE açısından baseline VGG16'yı iyileştirmediği için gerçek dünya adaptasyonunun başlangıç modeli olarak VGG16 baseline korunmuştur.

---

# 2. FVEI Veri Audit'i

Yazar tarafından sağlanan orijinal FVEI ZIP dosyası doğrudan audit edilmiştir.

Kaynak dosya:

`fog open data.zip`

Kaynak SHA256:

`07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d`

Audit sonrasında:

| Kategori | Örnek |
|---|---:|
| Retained total | 4109 |
| Exact-label | 3209 |
| Level-4 / 500 m analysis group | 900 |
| Conflicting duplicate images rejected | 229 |
| Outside level range rejected | 32 |
| Redundant identical images removed | 130 |

Görüntü doğrulamasında kullanılan temel koşullar:

- JPEG formatı
- 1920 × 1080 çözünürlük
- dosya adından visibility label çıkarımı
- SHA256 tabanlı exact duplicate kontrolü
- visibility-level aralık kontrolü

Exact-label visibility aralıkları:

| Level | Visibility Range |
|---|---:|
| Level 0 | 0–49 m |
| Level 1 | 50–99 m |
| Level 2 | 100–199 m |
| Level 3 | 200–499 m |

Audit pipeline'ında Level-4 / 500 m örnekleri exact-label regresyon metriğine dahil edilmemiş, ayrı analiz grubu olarak tutulmuştur.

Not: Level-4 / 500 m etiketinin ceiling/censored semantiği final yayın öncesinde veri setinin kaynak dokümantasyonu veya veri sağlayıcısından ayrıca doğrulanmalıdır.

---

# 3. Veri Bölme Stratejisi

Exact-label örnekler visibility level bazında stratified şekilde ayrılmıştır.

Temel ayarlar:

- Random seed: 42
- Train target ratio: 70%
- Validation target ratio: 15%
- Test target ratio: 15%

İlk split sonrasında pre-training similarity screening uygulanmıştır.

Strict cross-split benzerlik kontrolünde validation tarafında bulunan iki örnek potansiyel near-duplicate riski nedeniyle çıkarılmıştır:

- `fog open data/0/0-381-47.jpg`
- `fog open data/1/1-00073-62.jpg`

Test kümesi değiştirilmemiştir.

Final split:

| Split | Örnek |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Held-out Test | 482 |
| Excluded Similarity | 2 |
| Level-4 / 500 m Analysis | 900 |

Exact-label level dağılımı:

| Split | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---:|---:|---:|---:|
| Train | 549 | 592 | 555 | 549 |
| Validation | 117 | 126 | 119 | 118 |
| Test | 118 | 127 | 119 | 118 |

Held-out test split model seçimi veya hyperparameter tuning için kullanılmamıştır.

---

# 4. FVEI DataLoader

FVEI görüntüleri orijinal ZIP arşivinden doğrudan okunmuştur.

Pipeline:

Original ZIP  
→ Split Manifest  
→ RGB Conversion  
→ Resize 224 × 224  
→ ToTensor  
→ ImageNet Normalization  
→ VGG16

ImageNet normalization:

- Mean: `[0.485, 0.456, 0.406]`
- Std: `[0.229, 0.224, 0.225]`

Final DataLoader doğrulaması:

- Train: 2245
- Validation: 480
- Test: 482
- Level-4 / 500 m analysis: 900

---

# 5. Fine-Tuning Stratejisi

Model:

**VGG16 baseline → FVEI fine-tuning**

Initialization:

`vgg16_baseline_best.pth`

Fine-tuning sırasında:

- VGG16 Blocks 1–4 frozen
- VGG16 Block 5 trainable
- Regression head trainable

Trainable parameter counts:

| Parametre Grubu | Sayı |
|---|---:|
| Block 5 | 7,079,424 |
| Regression Head | 12,911,361 |

Training configuration:

| Ayar | Değer |
|---|---:|
| Epoch | 20 |
| Batch Size | 16 |
| Block 5 Learning Rate | 1e-5 |
| Regression Head Learning Rate | 1e-4 |
| Weight Decay | 1e-5 |
| Loss | L1Loss / MAE |
| Random Seed | 42 |

Model development sırasında yalnızca train ve validation split'leri kullanılmıştır.

Held-out FVEI test split training pipeline tarafından instantiate edilmemiştir.

---

# 6. CUDA Reproducibility Notu

GPU eğitimi sırasında PyTorch'un:

`adaptive_avg_pool2d_backward_cuda`

operasyonu için strict deterministic CUDA implementation bulunmadığı görülmüştür.

Bu nedenle:

`torch.use_deterministic_algorithms(True, warn_only=True)`

kullanılmıştır.

Böylece:

- random seed 42 korunmuştur,
- cuDNN deterministic mode korunmuştur,
- cuDNN benchmark kapalı tutulmuştur,
- desteklenen deterministic operasyonlar deterministic kalmıştır,
- desteklenmeyen CUDA operasyonlarında eğitim durdurulmak yerine warning üretilmiştir.

Bu nedenle GPU eğitimlerinin bit-bit identical olması garanti edilmemektedir.

---

# 7. FVEI Fine-Tuning Sonuçları

20 epoch eğitim tamamlanmıştır.

| Epoch | Train MAE | Validation MAE |
|---:|---:|---:|
| 1 | 36.2769 m | 32.2482 m |
| 2 | 29.6925 m | 30.8165 m |
| 3 | 27.8267 m | 28.3073 m |
| 4 | 27.3721 m | 27.9038 m |
| 5 | 26.0067 m | 27.8876 m |
| 6 | 25.0751 m | 28.4745 m |
| 7 | 23.9177 m | 26.8564 m |
| 8 | 23.7444 m | 27.8244 m |
| 9 | 22.4987 m | 28.3680 m |
| 10 | 21.2353 m | 27.8311 m |
| 11 | 21.3657 m | 28.2669 m |
| **12** | **21.9587 m** | **26.4428 m** |
| 13 | 20.8836 m | 27.3586 m |
| 14 | 20.0084 m | 26.8907 m |
| 15 | 19.8957 m | 26.9281 m |
| 16 | 19.9092 m | 26.9374 m |
| 17 | 19.2767 m | 26.5604 m |
| 18 | 19.0097 m | 28.0043 m |
| 19 | 18.3570 m | 27.8942 m |
| 20 | 17.1478 m | 28.5279 m |

En iyi checkpoint validation MAE üzerinden seçilmiştir:

- Best Epoch: **12**
- Best Validation MAE: **26.4428 m**

Final checkpoint:

`vgg16_fvei_block5_best.pth`

Epoch 12 sonrasında training MAE düşmeye devam ederken validation MAE kalıcı olarak iyileşmemiştir. Bu davranış hafif overfitting başlangıcı ile uyumludur.

Bu nedenle final model olarak epoch 20 yerine validation-selected epoch 12 checkpoint'i kullanılmıştır.

---

# 8. Locked Held-Out Test Evaluation

Model seçimi tamamlandıktan sonra epoch 12 checkpoint'i daha önce model selection sırasında kullanılmamış olan 482 örneklik held-out FVEI test split'i üzerinde değerlendirilmiştir.

Final exact-label test sonuçları:

| Metrik | Sonuç |
|---|---:|
| Test Samples | 482 |
| MAE | **25.1347 m** |
| RMSE | **38.4440 m** |
| R² | **0.894442** |
| Mean Signed Error / Bias | **+3.4534 m** |

Validation MAE:

**26.4428 m**

Test MAE:

**25.1347 m**

Validation ve test MAE değerlerinin birbirine yakın olması, mevcut split koşullarında validation-selected modelin held-out test üzerinde benzer hata düzeyini koruduğunu göstermektedir.

Test sonucu görüldükten sonra checkpoint selection veya hyperparameter tuning yapılmamıştır.

---

# 9. Level-Wise Test Sonuçları

| Level | N | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|
| Level 0 | 118 | 11.1879 m | 14.2664 m | +7.5328 m |
| Level 1 | 127 | 12.5699 m | 15.7690 m | -3.7466 m |
| Level 2 | 119 | 21.8013 m | 29.4082 m | +8.4794 m |
| Level 3 | 118 | 55.9664 m | 68.5106 m | +2.0548 m |

Level 3, mevcut held-out test sonuçlarında en yüksek MAE ve RMSE değerini üretmiştir.

Level 3 bias değerinin düşük kalmasına rağmen MAE ve RMSE'nin yüksek olması, temel problemin tek yönlü sistematik bias yerine örnekler arası hata yayılımının artması olduğunu göstermektedir.

---

# 10. Level-4 / 500 m Separate Analysis

Level-4 / 500 m grubu exact-label test MAE, RMSE veya R² hesaplarına dahil edilmemiştir.

Separate analysis:

| Metrik | Sonuç |
|---|---:|
| Samples | 900 |
| Mean Prediction | 563.4542 m |
| Median Prediction | 559.8888 m |
| Predictions >= 500 m | 840 / 900 |
| Fraction >= 500 m | 93.33% |
| Mean Shortfall Below 500 m | 1.6444 m |

Bu sonuçlar yalnızca ayrı Level-4 / 500 m analiz grubunun model çıktısını tanımlamak için kullanılmaktadır.

Bu grup exact 500 m regression ground truth olarak değerlendirilmemiştir.

---

# 11. Final FVEI Model

Final gerçek dünya FVEI modeli:

> **VGG16 + Block 5 Fine-Tuning + Regression Head**

Checkpoint:

`vgg16_fvei_block5_best.pth`

Selected Epoch:

**12**

Validation MAE:

**26.4428 m**

Held-Out Test MAE:

**25.1347 m**

Held-Out Test R²:

**0.894442**

Bu checkpoint Flask inference prototipinin güncel modeli olarak kullanılmaktadır.

---

# 12. CIDET ve Benchmark Deneylerinin Konumu

FVEI veri erişimi sağlanmadan önce CIDET üzerinde gerçek dünya adaptasyon deneyleri ve Benchmark-Visibility üzerinde cross-dataset stress test gerçekleştirilmiştir.

Bu deneyler silinmemiştir.

CIDET ve Benchmark çalışmaları:

- yardımcı / B-plan gerçek dünya deneyleri,
- domain-shift analizi,
- target-range shift analizi,
- cross-dataset generalization gözlemleri

olarak korunmaktadır.

Final proposal-aligned gerçek dünya model akışında FVEI ana veri kaynağı olarak kullanılmaktadır.

---

# 13. Metodolojik Sınırlamalar

Sonuçlar yorumlanırken:

- FVEI exact-label split level-stratified olarak oluşturulmuştur.
- Orijinal veri içinde güvenilir scene/camera identity bilgisi mevcut pipeline'da kullanılabilir durumda değildir.
- Pre-training similarity screening uygulanmış olsa da residual dependence tamamen dışlanamaz.
- İki validation örneği strict similarity screening sonucunda çıkarılmıştır.
- Test split değiştirilmemiştir.
- Held-out test yalnızca model selection tamamlandıktan sonra açılmıştır.
- Test sonucuna göre model tuning yapılmamıştır.
- Tek split ve tek temel seed kullanılmıştır.
- CUDA üzerinde bazı operasyonlar strict deterministic değildir.
- Level-4 / 500 m etiket semantiği final yayın öncesinde kaynak dokümantasyon ile ayrıca doğrulanmalıdır.

Bu nedenle sonuçlar mevcut veri, split ve deney protokolü kapsamında yorumlanmalıdır.

---

# 14. Üretilen Kod ve Çıktılar

Kod:

- `src/data/prepare_fvei.py`
- `src/data/split_fvei.py`
- `src/training/fvei_dataloader.py`
- `src/training/finetune_vgg16_fvei.py`
- `src/evaluation/evaluate_vgg16_fvei_final.py`

Local generated outputs:

- `results/checkpoints/vgg16_fvei_block5_best.pth`
- `results/fvei/vgg16_fvei_block5_history.csv`
- `results/fvei/vgg16_fvei_block5_summary.json`
- `results/fvei/vgg16_fvei_final_test_predictions.csv`
- `results/fvei/vgg16_fvei_ceiling_predictions.csv`
- `results/fvei/vgg16_fvei_final_evaluation.json`

Dataset manifests and result artifacts `.gitignore` politikası gereği repository'ye commit edilmemektedir.

---

# 15. Sonuç

Sentetik FRIDA/FRIDA2 deneylerinde seçilen VGG16 baseline modelinin FVEI gerçek dünya verisi üzerinde kontrollü şekilde fine-tune edilmesi sonucunda:

- validation MAE **26.4428 m**,
- held-out test MAE **25.1347 m**,
- held-out test RMSE **38.4440 m**,
- held-out test R² **0.894442**

elde edilmiştir.

Mevcut deney protokolünde FVEI fine-tuning, sentetik başlangıç modelinin gerçek dünya veri dağılımına başarılı biçimde adapte olabildiğini göstermektedir.

En belirgin hata artışı Level 3 visibility aralığında gözlenmiştir.

Final model:

**VGG16 FVEI Block5 Fine-Tuned — Epoch 12**

olarak belirlenmiştir.
