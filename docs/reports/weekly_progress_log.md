# Haftalık İlerleme Günlüğü

**Proje Adı:** Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Destek Programı:** TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı

---

# Amaç

Bu doküman, proje süresince gerçekleştirilen çalışmaların haftalık ve aşama bazlı ilerleme özetini içermektedir.

Ayrıntılı teknik kayıtlar araştırma günlüğü ve ilgili deney raporlarında tutulmaktadır.

Ana araştırma akışı:

```text
FRIDA / FRIDA2
        ↓
Sentetik Veri Hazırlama
        ↓
VGG16 ve ResNet50 Baseline
        ↓
Baseline Karşılaştırması
        ↓
VGG16 Baseline Seçimi
        ↓
CBAM ve SE Attention Deneyleri
        ↓
CIDET / Benchmark Yardımcı Gerçek Dünya Deneyleri
        ↓
FVEI Dataset Audit
        ↓
FVEI Split ve Similarity Screening
        ↓
FVEI Fine-Tuning
        ↓
Validation-Based Model Selection
        ↓
Locked FVEI Test Evaluation
        ↓
Final FVEI Model
        ↓
Flask Web Prototipi
```

---

# Genel İlerleme

| Aşama | Durum |
|---|:---:|
| FRIDA / FRIDA2 Veri Hazırlama | Tamamlandı |
| Preprocessing Pipeline | Tamamlandı |
| Scene-Based Split | Tamamlandı |
| VGG16 Baseline | Tamamlandı |
| ResNet50 Baseline | Tamamlandı |
| Baseline Karşılaştırması | Tamamlandı |
| Sentetik Baseline Seçimi | Tamamlandı |
| CBAM Attention | Tamamlandı |
| SE Attention | Tamamlandı |
| Attention Karşılaştırması | Tamamlandı |
| CIDET Yardımcı Gerçek Dünya Deneyleri | Tamamlandı |
| Benchmark-Visibility Stress Test | Tamamlandı |
| Flask İlk Prototipi | Tamamlandı |
| FVEI Dataset Audit | Tamamlandı |
| FVEI Similarity Screening | Tamamlandı |
| FVEI Train / Validation / Test Split | Tamamlandı |
| FVEI DataLoader | Tamamlandı |
| FVEI Fine-Tuning | Tamamlandı |
| FVEI Model Selection | Tamamlandı |
| Locked FVEI Test Evaluation | Tamamlandı |
| Level-Wise Error Analysis | Tamamlandı |
| Level-4 / 500 m Separate Analysis | Tamamlandı |
| Final FVEI Flask Entegrasyonu | Tamamlandı |
| FVEI Araştırma Raporu | Tamamlandı |
| README Güncellemesi | Tamamlandı |
| Araştırma Günlüğü Güncellemesi | Tamamlandı |
| Final TÜBİTAK Raporu | Bekliyor |
| Publication-Oriented Manuscript | Bekliyor |

---

# Hafta 1 — Veri Hazırlama ve Araştırma Altyapısı

**Durum:** Tamamlandı

## Gerçekleştirilen Çalışmalar

- FRIDA ve FRIDA2 veri setleri incelendi.
- Sentetik sis görüntüleri ve ilgili veri yapıları analiz edildi.
- Sürekli görüş mesafesi regresyonu için veri hazırlama pipeline'ı oluşturuldu.
- Aynı sahnenin farklı sis seviyelerinin farklı split'lere dağılmasını önlemek amacıyla scene-based splitting geliştirildi.
- PyTorch Dataset ve DataLoader altyapısı hazırlandı.
- Ortak preprocessing pipeline oluşturuldu.
- Reproducibility için random seed 42 kullanıldı.
- Proje klasör yapısı ve temel dokümantasyon oluşturuldu.

## Temel Çıktılar

| Özellik | Sonuç |
|---|---:|
| Toplam Sahne | 84 |
| Toplam Görüntü | 672 |
| Visibility Seviyesi | 8 |
| Train | 464 |
| Validation | 96 |
| Test | 112 |

Visibility seviyeleri:

**50, 80, 100, 150, 200, 300, 500 ve 800 metre**

## Hafta Sonu Durumu

Sentetik veri pipeline'ı tamamlandı ve transfer öğrenme tabanlı CNN modellerinin kontrollü biçimde karşılaştırılabileceği deney altyapısı oluşturuldu.

---

# Hafta 2 — VGG16 Baseline

**Durum:** Tamamlandı

## Gerçekleştirilen Çalışmalar

- ImageNet pretrained VGG16 modeli regresyon problemine uyarlandı.
- Classification head yerine sürekli görüş mesafesi üreten regression head geliştirildi.
- VGG16 feature extractor donduruldu.
- Training ve validation pipeline'ı geliştirildi.
- Checkpoint sistemi oluşturuldu.
- Model 20 epoch eğitildi.
- En iyi checkpoint validation MAE üzerinden seçildi.
- Bağımsız sentetik test değerlendirmesi gerçekleştirildi.
- Actual vs Predicted ve prediction error grafikleri üretildi.

## Temel Sonuçlar

| Metrik | Sonuç |
|---|---:|
| Best Epoch | 18 |
| Validation MAE | 69.9705 m |
| Test MAE | 66.7227 m |
| Mean Signed Error | -17.3877 m |
| Test Samples | 112 |

## Hafta Sonu Durumu

VGG16 sentetik baseline başarıyla tamamlandı.

Bu sonuç daha sonraki ResNet50 ve attention deneyleri için referans baseline olarak kaydedildi.

---

# Hafta 3 — ResNet50 Baseline ve Baseline Karşılaştırması

**Durum:** Tamamlandı

## Gerçekleştirilen Çalışmalar

- ImageNet pretrained ResNet50 regresyon mimarisi geliştirildi.
- VGG16 ile aynı temel veri split'i ve eğitim bütçesi kullanıldı.
- ResNet50 modeli 20 epoch eğitildi.
- Validation-based checkpoint selection uygulandı.
- Bağımsız test değerlendirmesi yapıldı.
- Prediction-range compression ve yüksek visibility underestimation davranışı incelendi.
- VGG16 ve ResNet50 resmi baseline karşılaştırması tamamlandı.

## ResNet50 Sonuçları

| Metrik | Sonuç |
|---|---:|
| Best Epoch | 20 |
| Validation MAE | 121.8414 m |
| Test MAE | 124.6181 m |
| Mean Signed Error | -77.3460 m |
| Maximum Absolute Error | 602.6687 m |

## Baseline Karşılaştırması

| Model | Validation MAE | Test MAE |
|---|---:|---:|
| VGG16 | 69.9705 m | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

VGG16 mevcut sentetik FRIDA/FRIDA2 deney koşullarında daha düşük test MAE üretmiştir.

Bu nedenle sentetik aşama için:

**Selected Baseline: VGG16**

olarak belirlenmiştir.

Bu sonuç mimarilerin genel üstünlüğüne ilişkin bir iddia olarak değil, mevcut veri ve deney düzenine özgü model-selection sonucu olarak değerlendirilmiştir.

---

# Hafta 4 — Attention Mekanizmaları

**Durum:** Tamamlandı

## CBAM Deneyi

VGG16 baseline üzerine Convolutional Block Attention Module entegre edildi.

CBAM:

- Channel Attention
- Spatial Attention

bileşenlerini birlikte kullanmaktadır.

Model baseline ile aynı temel split ve eğitim koşullarında eğitildi.

Sonuç:

| Metrik | Sonuç |
|---|---:|
| Best Epoch | 17 |
| Validation MAE | 69.3274 m |
| Test MAE | 67.6214 m |

CBAM validation MAE değerinde küçük bir iyileşme üretmiş ancak bağımsız test MAE açısından VGG16 baseline'ı geçememiştir.

## SE Deneyi

Proje risk yönetimi kapsamında alternatif attention yaklaşımı olarak Squeeze-and-Excitation mekanizması denendi.

Sonuç:

| Metrik | Sonuç |
|---|---:|
| Best Epoch | 19 |
| Validation MAE | 70.6083 m |
| Test MAE | 72.4412 m |

## Nihai Sentetik Model Karşılaştırması

| Model | Validation MAE | Test MAE |
|---|---:|---:|
| VGG16 Baseline | 69.9705 m | **66.7227 m** |
| VGG16 + CBAM | **69.3274 m** | 67.6214 m |
| VGG16 + SE | 70.6083 m | 72.4412 m |
| ResNet50 | 121.8414 m | 124.6181 m |

## Hafta Sonu Kararı

CBAM ve SE mekanizmaları teknik olarak başarıyla uygulanmış ancak mevcut sentetik test koşullarında VGG16 baseline test MAE değerini iyileştirmemiştir.

Bu nedenle gerçek dünya adaptasyonunun başlangıç checkpoint'i olarak:

**VGG16 Baseline**

korunmuştur.

---

# Hafta 5 — Yardımcı Gerçek Dünya Deneyleri ve Flask Prototipi

**Durum:** Tamamlandı

## CIDET

FVEI erişimi sağlanmadan önce gerçek dünya adaptasyon yöntemlerini geliştirebilmek amacıyla CIDET üzerinde yardımcı / B-plan deneyleri gerçekleştirildi.

Synthetic VGG16 modelinin CIDET zero-shot değerlendirmesi güçlü domain ve target-range shift gösterdi.

Zero-shot sonuç:

**MAE: 2258.8934 m**

Fine-tuning stratejileri:

| Strateji | Validation MAE |
|---|---:|
| Head-only + L1 | 446.5714 m |
| Block5 + L1 | 326.6640 m |
| Block5 + Balanced Sampling | 334.9808 m |
| Block5 + Huber | **324.1948 m** |

CIDET development deneylerinde en düşük validation MAE Block5 + Huber ile elde edildi.

## Benchmark-Visibility

CIDET üzerinde seçilen model ayrı bir Benchmark-Visibility veri setinde ek fine-tuning yapılmadan stress test'e tabi tutuldu.

| Metrik | Sonuç |
|---|---:|
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Mean Signed Error | -11310.9893 m |
| Pearson Correlation | 0.585183 |
| Prediction Range | 97.43–1308.30 m |
| Target Range | 112–20000 m |

Sonuç geniş target range değişiminde belirgin prediction-range compression ve yüksek-visibility underestimation gösterdi.

Bu sonuç model tuning amacıyla kullanılmadı.

CIDET ve Benchmark deneyleri final FVEI model seçim sürecinden ayrı, yardımcı domain-shift ve cross-dataset deneyleri olarak korunmaktadır.

## Flask İlk Prototipi

Aynı aşamada Flask tabanlı araştırma prototipi geliştirildi.

Endpoint'ler:

```text
GET  /
GET  /health
POST /predict
```

Arayüzde:

- görüntü yükleme,
- önizleme,
- model inference,
- metre cinsinden visibility prediction

özellikleri geliştirildi.

İlk prototip CIDET development checkpoint'i kullanıyordu.

---

# Hafta 6 — FVEI Dataset Audit ve Split

**Durum:** Tamamlandı

## Dataset Audit

FVEI verisine erişim sağlandıktan sonra orijinal ZIP arşivi üzerinde ayrı bir audit pipeline'ı geliştirildi.

Kaynak SHA256:

```text
07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d
```

Audit sonuçları:

| Kategori | Örnek |
|---|---:|
| Retained | 4109 |
| Exact-label | 3209 |
| Level-4 / 500 m analysis group | 900 |
| Conflicting duplicate rejected | 229 |
| Outside level range rejected | 32 |
| Redundant identical removed | 130 |

Exact-label dağılımı:

| Level | N | Observed Range |
|---|---:|---:|
| Level 0 | 785 | 12–49 m |
| Level 1 | 846 | 51–99 m |
| Level 2 | 793 | 101–199 m |
| Level 3 | 785 | 201–499 m |

Level-4 / 500 m grubu exact-label regresyon değerlendirmesinden ayrı tutuldu.

Bu grubun ceiling/censored semantiğinin final bilimsel yayın öncesinde veri kaynağının resmi dokümantasyonundan ayrıca doğrulanması gerektiği kaydedildi.

## Split Strategy

Exact-label örnekler visibility level bazında stratified olarak ayrıldı.

Random seed:

**42**

İlk split:

- Train: 2245
- Validation: 482
- Test: 482
- Level-4 analysis: 900

## Similarity Screening

Cross-split near-duplicate riskini azaltmak amacıyla ek similarity screening gerçekleştirildi.

dHash ve PCA tabanlı yaklaşımların scene identity için yeterince güvenilir olmadığı görüldü.

Strict similarity kontrolü sonucunda validation tarafındaki iki şüpheli örnek çıkarıldı.

Test seti değiştirilmedi.

## Final FVEI Split

| Split | Örnek |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Locked Test | 482 |
| Excluded Similarity | 2 |
| Level-4 Analysis | 900 |

Split yeniden oluşturulduğunda:

**0 split mismatch**

elde edilerek reproducibility doğrulandı.

---

# Hafta 7 — FVEI Fine-Tuning ve Model Selection

**Durum:** Tamamlandı

## DataLoader

FVEI için ZIP arşivinden doğrudan okuma yapan PyTorch DataLoader geliştirildi.

Doğrulanan veri sayıları:

| Split | Örnek |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Test | 482 |
| Level-4 Analysis | 900 |

## Fine-Tuning Strategy

Başlangıç checkpoint'i:

```text
vgg16_baseline_best.pth
```

Model:

```text
VGG16 Blocks 1–4 → Frozen
VGG16 Block 5     → Trainable
Regression Head   → Trainable
```

Training configuration:

| Ayar | Değer |
|---|---:|
| Epoch | 20 |
| Batch Size | 16 |
| Block5 LR | 1e-5 |
| Head LR | 1e-4 |
| Weight Decay | 1e-5 |
| Loss | L1Loss / MAE |
| Seed | 42 |

Held-out test split model development sırasında kullanılmadı.

## GPU Environment

Fine-tuning NVIDIA GeForce GTX 1650 üzerinde gerçekleştirildi.

Kullanılan ortam:

- Torch 2.13.0+cu126
- Torchvision 0.28.0+cu126
- CUDA available: True

Batch size 16 için peak allocated GPU memory yaklaşık:

**1391.01 MiB**

olarak ölçüldü.

Strict deterministic implementation sunmayan CUDA operasyonları nedeniyle:

```python
torch.use_deterministic_algorithms(True, warn_only=True)
```

kullanıldı.

## Model Selection

20 epoch eğitim tamamlandı.

En iyi model validation MAE üzerinden seçildi:

| Metrik | Sonuç |
|---|---:|
| Best Epoch | **12** |
| Train MAE at Epoch 12 | 21.9587 m |
| Validation MAE | **26.4428 m** |

Epoch 20'de:

- Train MAE: 17.1478 m
- Validation MAE: 28.5279 m

oldu.

Training error düşmeye devam ederken validation error kalıcı biçimde iyileşmediği için epoch 12 checkpoint'i korundu.

Final checkpoint:

```text
vgg16_fvei_block5_best.pth
```

---

# Hafta 8 — Locked FVEI Test ve Final Model

**Durum:** Tamamlandı

Validation-based model selection tamamlandıktan sonra daha önce model geliştirmede kullanılmamış 482 görüntülük held-out test split açıldı.

## Final FVEI Test Sonuçları

| Metrik | Sonuç |
|---|---:|
| Test Samples | 482 |
| MAE | **25.1347 m** |
| RMSE | **38.4440 m** |
| R² | **0.894442** |
| Bias | **+3.4534 m** |

Validation MAE:

**26.4428 m**

Held-out Test MAE:

**25.1347 m**

Test sonucu görüldükten sonra checkpoint selection veya hyperparameter tuning yapılmadı.

## Level-Wise Results

| Level | N | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|
| Level 0 | 118 | 11.1879 m | 14.2664 m | +7.5328 m |
| Level 1 | 127 | 12.5699 m | 15.7690 m | -3.7466 m |
| Level 2 | 119 | 21.8013 m | 29.4082 m | +8.4794 m |
| Level 3 | 118 | 55.9664 m | 68.5106 m | +2.0548 m |

En yüksek error Level 3 grubunda gözlendi.

## Level-4 / 500 m Separate Analysis

900 örnek exact-label regresyon metriklerinden ayrı analiz edildi.

| Metrik | Sonuç |
|---|---:|
| Mean Prediction | 563.4542 m |
| Median Prediction | 559.8888 m |
| Predictions >= 500 m | 840 / 900 |
| Fraction >= 500 m | 93.33% |
| Mean Shortfall Below 500 m | 1.6444 m |

## Final Model

Final gerçek dünya modeli:

**VGG16 FVEI Block5 Fine-Tuned**

Selected epoch:

**12**

Held-out Test MAE:

**25.1347 m**

Held-out Test R²:

**0.894442**

---

# Hafta 9 — Final Flask Entegrasyonu ve Dokümantasyon

**Durum:** Tamamlandı

## Flask Güncellemesi

Flask inference pipeline'daki eski CIDET checkpoint'i final FVEI checkpoint'i ile değiştirildi.

Yeni model:

```text
VGG16 FVEI Block5 Fine-Tuned
```

Checkpoint:

```text
vgg16_fvei_block5_best.pth
```

Model metadata:

- Epoch: 12
- Validation MAE: 26.4428 m

Web arayüzündeki CIDET ifadeleri FVEI ile güncellendi.

## API Validation

Flask API testleri yeniden çalıştırıldı.

Sonuç:

```text
4 passed
```

Ana sayfanın FVEI model bilgisi ile başarılı şekilde render edildiği doğrulandı.

## Dokümantasyon

Aşağıdaki ana dokümantasyon güncellendi:

- `docs/reports/fvei_real_world_evaluation.md`
- `README.md`
- `docs/research_notes/arastirma_gunlugu.md`
- `docs/reports/weekly_progress_log.md`

CIDET ve Benchmark-Visibility deneyleri silinmemiş, yardımcı / B-plan deneyleri olarak korunmuştur.

---

# Güncel Proje Durumu

Ana deneysel model geliştirme aşaması tamamlanmıştır.

## Sentetik Aşama

| Model | Test MAE |
|---|---:|
| VGG16 Baseline | **66.7227 m** |
| VGG16 + CBAM | 67.6214 m |
| VGG16 + SE | 72.4412 m |
| ResNet50 | 124.6181 m |

Selected synthetic baseline:

**VGG16**

## FVEI Gerçek Dünya Aşaması

| Metrik | Sonuç |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Locked Test | 482 |
| Best Epoch | 12 |
| Validation MAE | **26.4428 m** |
| Test MAE | **25.1347 m** |
| Test RMSE | **38.4440 m** |
| Test R² | **0.894442** |
| Test Bias | **+3.4534 m** |

Final model:

**VGG16 FVEI Block5 Fine-Tuned**

## Tamamlanan Ana Aşamalar

- Sentetik veri hazırlama
- VGG16 baseline
- ResNet50 baseline
- Baseline comparison
- CBAM attention
- SE attention
- Attention comparison
- CIDET auxiliary experiments
- Benchmark-Visibility stress test
- Flask prototipi
- FVEI dataset audit
- FVEI similarity screening
- FVEI reproducible split
- FVEI DataLoader
- FVEI fine-tuning
- GPU training
- Validation-based checkpoint selection
- Locked held-out test
- Level-wise error analysis
- Level-4 / 500 m separate analysis
- Final FVEI Flask integration
- FVEI research report
- README update
- Research journal update
- Weekly progress log update

---

# Kalan Çalışmalar

Ana araştırma model geliştirme aşaması büyük ölçüde tamamlanmıştır.

Kalan işler:

- Final sonuç tabloları ve görsellerinin düzenlenmesi
- TÜBİTAK final proje raporunun hazırlanması
- Publication-oriented manuscript hazırlanması
- Final repository quality-control
- Dokümantasyonun son kez tutarlılık açısından kontrol edilmesi
- FHVI erişimi sağlanması durumunda isteğe bağlı ek external evaluation

---

# Metodolojik Notlar

FVEI locked test split model selection sırasında kullanılmamıştır.

Final test sonucu görüldükten sonra mevcut checkpoint üzerinde yeni model tuning yapılmamıştır.

FVEI split visibility level bazında stratified olarak hazırlanmıştır.

Similarity screening cross-split benzerlik riskini azaltmak amacıyla uygulanmış olsa da FVEI için güvenilir scene/camera identity bilgisi mevcut pipeline'da bulunmadığından residual sample dependence tamamen dışlanamaz.

Level-4 / 500 m grubu exact-label test MAE, RMSE ve R² metriklerinden ayrı tutulmuştur.

Bu grubun ceiling/censored semantiği final bilimsel yayın öncesinde veri setinin resmi kaynak dokümantasyonuyla ayrıca doğrulanmalıdır.

CUDA training sırasında bazı operasyonların strict deterministic implementation sunmaması nedeniyle bit-bit identical GPU reproducibility garanti edilmemektedir.

Tek split ve temel random seed 42 kullanıldığı için sonuçlar hakkında istatistiksel anlamlılık iddiasında bulunulmamaktadır.

---

# Bir Sonraki Milestone

Bir sonraki ana milestone:

> **Final TÜBİTAK proje raporunun hazırlanması ve proje çıktılarının yayın formatına dönüştürülmesi**

FHVI veri erişimi sağlanırsa mevcut locked FVEI testini yeniden tuning amacıyla kullanmak yerine FHVI ayrı bir external real-world evaluation kaynağı olarak değerlendirilecektir.
