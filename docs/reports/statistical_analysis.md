# İstatistiksel Analiz

Bu rapor `src/evaluation/statistical_analysis.py` tarafından otomatik olarak üretilir; elle düzenlenmemelidir.

Analiz yalnızca kaydedilmiş tahmin dosyalarını kullanır. Hiçbir model yeniden eğitilmemiş ve test kümeleri hiçbir seçim kararında kullanılmamıştır.

## 1. Sentetik FRIDA/FRIDA2 Test Kümesi

- Test görüntüsü: **112**, sahne: **14**
- Aynı sahnenin 8 sis seviyesi bağımsız olmadığından analiz birimi **sahne**dir.
- Güven aralıkları sahne düzeyinde küme bootstrap ile (10000 yeniden örnekleme) hesaplanmıştır.

### 1.1 Model Bazında Test MAE (95% GA)

| Model | Test MAE (m) [95% GA] |
|---|---:|
| VGG16 Baseline | 66.72 [58.37, 75.54] |
| ResNet50 Baseline | 124.62 [115.27, 134.01] |
| VGG16 + CBAM | 67.62 [57.45, 78.21] |
| VGG16 + SE | 72.44 [63.08, 82.16] |

### 1.2 VGG16 Baseline ile Eşleştirilmiş Karşılaştırmalar

Fark = MAE(model) − MAE(VGG16 Baseline). Pozitif değer VGG16 Baseline'ın daha düşük hata ürettiğini gösterir.

| Model | MAE Farkı (m) [95% GA] | VGG16'nın daha iyi olduğu sahne | Wilcoxon p (sahne) | Holm p | Wilcoxon p (görüntü, ek) | Anlamlı (α=0.05, Holm) |
|---|---:|---:|---:|---:|---:|:---:|
| ResNet50 Baseline | 57.90 [48.84, 67.29] | 14/14 | 1.22e-04 | 3.66e-04 | 2.86e-07 | Evet |
| VGG16 + CBAM | 0.90 [-3.24, 5.39] | 8/14 | 0.7609 | 0.7609 | 0.7297 | Hayır |
| VGG16 + SE | 5.72 [3.29, 7.95] | 13/14 | 0.0012 | 0.0024 | 2.04e-06 | Evet |

### 1.3 Hipotezin Değerlendirilmesi

Öneride ResNet50'nin VGG16'ya göre istatistiksel olarak anlamlı düzeyde daha düşük MAE üreteceği öngörülmüştü.

Gözlenen fark **VGG16 lehine**: ResNet50'nin MAE değeri VGG16'dan 57.90 m (95% GA 48.84–67.29 m) daha yüksektir. Sahne düzeyinde Wilcoxon testi için Holm düzeltmeli p = 3.66e-04.

Bu sonuç tek bir sahne ayrımı ve tek eğitim tohumu (seed 42) için geçerlidir. Tohum değişkenliği için bkz. Bölüm 3.

## 2. FVEI Kilitli Test Kümesi

- Güvenilir sahne/kamera kimliği bulunmadığından bootstrap görüntü düzeyinde, görüş seviyesine göre tabakalı yapılmıştır.
- Sınırlılık: Görüntüler aynı kamera veya sahneyi paylaşabilir; bu nedenle görüntü düzeyindeki güven aralıkları gerçek belirsizlikten bir miktar dar olabilir.

| Çalıştırma | N | MAE (m) [95% GA] | RMSE (m) [95% GA] | R² [95% GA] |
|---|---:|---:|---:|---:|
| VGG16 FVEI Block5 (final) | 482 | 25.13 [23.12, 27.20] | 38.44 [34.52, 42.32] | 0.8944 [0.8677, 0.9167] |
| resnet50_fvei_synthetic_lastblock_s42 | 482 | 27.48 [25.41, 29.66] | 41.38 [37.34, 45.56] | 0.8777 [0.8511, 0.9005] |
| vgg16_fvei_imagenet_lastblock_s42 | 482 | 24.33 [22.39, 26.32] | 37.48 [33.65, 41.28] | 0.8997 [0.8783, 0.9191] |

Fark = MAE(çalıştırma) − MAE(VGG16 FVEI Block5 (final)).

| Çalıştırma | MAE Farkı (m) [95% GA] | Wilcoxon p | Holm p | Anlamlı |
|---|---:|---:|---:|:---:|
| resnet50_fvei_synthetic_lastblock_s42 | 2.34 [0.62, 4.09] | 0.0318 | 0.0636 | Hayır |
| vgg16_fvei_imagenet_lastblock_s42 | -0.80 [-1.96, 0.38] | 0.0700 | 0.0700 | Hayır |

## 3. Çoklu Tohum (Seed) Deneyleri

Sahne ayrımı sabit (seed 42) tutulmuş, yalnızca eğitim tohumu değiştirilmiştir.

| Deney Grubu | Seed Sayısı | Test MAE Ort. ± SS (m) | Min–Maks (m) | En İyi Epoch'lar | Bütçe içinde yakınsayan seed |
|---|---:|---:|---:|---|---:|
| resnet50_e20 | 5 | 127.64 ± 3.71 | 122.94–131.45 | 20, 20, 20, 20, 20 | 0/5 |
| resnet50_e200_p20 | 5 | 81.41 ± 1.94 | 78.28–83.43 | 199, 159, 112, 137, 186 | 3/5 |
| resnet50_e50 | 5 | 86.29 ± 2.00 | 83.70–88.85 | 50, 50, 50, 50, 50 | 0/5 |
| vgg16_e20 | 5 | 63.99 ± 1.31 | 61.85–65.06 | 20, 20, 20, 19, 19 | 2/5 |
| vgg16_e200_p20 | 5 | 53.87 ± 0.81 | 52.92–54.89 | 76, 52, 49, 38, 49 | 5/5 |

Seed bazında eşleştirilmiş karşılaştırmalar. Fark = MAE(karşılaştırılan) − MAE(referans); pozitif değer referans lehinedir. Holm düzeltmesi her aile (mimari: VGG16 ↔ ResNet50; dikkat: ResNet50 ↔ ResNet50 + CBAM/SE) içinde ayrı uygulanır.

| Aile | Referans grubu | Karşılaştırılan grup | Ortak seed | Ortalama fark (m) | Referansın daha iyi olduğu seed | Fark [95% GA] (sahne, seed ortalaması) | Referansın daha iyi olduğu sahne | Holm p | Protokol kararı |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| Mimari | vgg16_e20 | resnet50_e20 | 5 | 63.65 | 5/5 | 63.65 [54.43, 72.84] | 14/14 | 3.66e-04 | VGG16 anlamlı düzeyde daha iyi (uyarı: tüm seed'ler bütçe içinde yakınsamadı) |
| Mimari | vgg16_e20 | resnet50_e50 | 5 | 22.30 | 5/5 | 22.30 [11.75, 32.42] | 12/14 | 0.0046 | VGG16 anlamlı düzeyde daha iyi (uyarı: tüm seed'ler bütçe içinde yakınsamadı) |
| Mimari | vgg16_e200_p20 | resnet50_e200_p20 | 5 | 27.53 | 5/5 | 27.53 [7.94, 48.91] | 10/14 | 0.0419 | VGG16 anlamlı düzeyde daha iyi (uyarı: tüm seed'ler bütçe içinde yakınsamadı) |

Gruplar yalnızca aynı durdurma kuralına sahip gruplarla eşleştirilir (sabit bütçe ↔ sabit bütçe, aynı patience ↔ aynı patience).

"Bütçe içinde yakınsayan seed": erken durdurmalı koşularda epoch bütçesine ulaşmadan patience kuralıyla duran seed sayısı. Eski sabit bütçeli koşularda en iyi validation epoch'unun son epoch'tan önce olması yalnızca bir yakınsama göstergesi olarak kullanılır.

Anlamlılık testi: her görüntünün hatası eşleştirilmiş seed'ler üzerinden ortalanır, ardından 14 test sahnesinde eşleştirilmiş Wilcoxon testi uygulanır (Holm düzeltmeli); güven aralığı sahne düzeyinde küme bootstrap ile hesaplanır. Seed düzeyinde doğrudan test yapılmaz, çünkü 5 seed ile ulaşılabilecek en küçük iki yönlü p değeri 0.0625'tir.

Karar kuralı: [`docs/MODEL_SELECTION_PROTOCOL.md`](../MODEL_SELECTION_PROTOCOL.md).
