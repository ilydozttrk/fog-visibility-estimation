# Fog Visibility Estimation using Transfer Learning

Transfer öğrenme tabanlı derin evrişimsel sinir ağları (CNN) kullanılarak sisli hava koşullarında görüntü tabanlı görüş mesafesi tahmini gerçekleştirmeyi amaçlayan TÜBİTAK 2209-A araştırma projesidir.

Bu çalışma kapsamında ImageNet üzerinde önceden eğitilmiş **VGG16** ve **ResNet50** mimarileri sürekli görüş mesafesi regresyonu için karşılaştırılmış, mevcut sentetik deney aşamasında daha başarılı olan VGG16 mimarisi seçilmiş ve modele **CBAM (Convolutional Block Attention Module)** entegre edilmiştir.

---

# TÜBİTAK 2209-A Araştırma Projesi

## Proje Başlığı

> **Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi**

---

# Araştırmanın Amacı

Bu proje;

- görüntü tabanlı sürekli görüş mesafesi tahmini gerçekleştirmeyi,
- transfer öğrenme ile VGG16 ve ResNet50 modellerini karşılaştırmayı,
- en başarılı temel modele Attention Mechanism entegre etmeyi,
- gerçek dünya verileri üzerinde modeli değerlendirmeyi,
- Flask tabanlı bir web prototipi geliştirmeyi

amaçlamaktadır.

Temel performans metriği **Mean Absolute Error (MAE)** olarak belirlenmiştir.

---

# Araştırma Sorusu

Transfer öğrenme yöntemi ile görüş mesafesi tahmini görevine uyarlanan VGG16 ve ResNet50 mimarilerinden hangisi daha düşük MAE değeri üreterek Akıllı Ulaşım Sistemleri için daha uygun bir temel model sunmaktadır?

Attention mekanizmasının seçilen temel model üzerindeki etkisi de deneysel olarak ayrıca değerlendirilecektir.

---

# Veri Seti

Projenin mevcut sentetik deney aşamasında **FRIDA** ve **FRIDA2** veri setleri kullanılmaktadır.

Hazır sürekli görüş mesafesi etiketleri bulunmadığından, veri setlerine ait derinlik haritaları kullanılarak kontrollü sentetik sis görüntüleri oluşturulmuştur.

## Kullanılan Görüş Mesafeleri

- 50 m
- 80 m
- 100 m
- 150 m
- 200 m
- 300 m
- 500 m
- 800 m

## Oluşturulan Veri Kümesi

| Özellik | Değer |
|---|---:|
| FRIDA temel sahne | **18** |
| FRIDA2 temel sahne | **66** |
| Toplam sahne | **84** |
| Görüş mesafesi seviyesi | **8** |
| Toplam görüntü | **672** |

Her görüntü için görüş mesafesi etiketi, sahne kimliği, kaynak veri seti ve sis üretim parametreleri kayıt altına alınmıştır.

---

# Veri Bölme Stratejisi

Veri sızıntısını önlemek amacıyla **scene-based splitting** uygulanmıştır.

Aynı temel sahneye ait farklı sis seviyelerindeki görüntülerin farklı veri kümelerine dağılması engellenmiştir.

| Küme | Görüntü Sayısı |
|---|---:|
| Train | **464** |
| Validation | **96** |
| Test | **112** |

Bölme işlemi tamamen tekrarlanabilir olacak şekilde:

```text
Random Seed = 42
```

kullanılarak gerçekleştirilmiştir.

Aynı split VGG16, ResNet50 ve Attention tabanlı deneylerde korunmaktadır.

---

# Ön İşleme Pipeline'ı

Model eğitiminden önce aşağıdaki işlemler uygulanmaktadır:

- RGB formatına dönüştürme
- 224 × 224 yeniden boyutlandırma
- ImageNet normalizasyonu
- Scene-based train / validation / test bölme
- PyTorch DataLoader oluşturulması

Bu pipeline tüm baseline deneylerinde ortak kullanılmıştır.

---

# Kullanılan Teknolojiler

- Python
- PyTorch
- Torchvision
- Pillow
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- OpenCV
- Flask
- OpenPyXL

---

# Proje Yapısı

```text
.
├── data/
│   ├── generated/
│   ├── processed/
│   ├── raw/
│   └── splits/
│
├── docs/
│   ├── literature/
│   ├── research_notes/
│   └── reports/
│
├── figures/
│
├── notebooks/
│
├── results/
│   ├── checkpoints/
│   ├── evaluation/
│   ├── logs/
│   └── plots/
│
├── src/
│   ├── api/
│   ├── data/
│   ├── evaluation/
│   ├── models/
│   └── training/
│
├── README.md
└── requirements.txt
```

---

# Baseline Modeller

## VGG16

ImageNet üzerinde önceden eğitilmiş VGG16 modeli transfer öğrenme yaklaşımıyla sürekli görüş mesafesi regresyonuna uyarlanmıştır.

VGG16 convolutional backbone dondurulmuş ve classifier bölümü regresyon head'i ile değiştirilmiştir.

Regresyon head:

```text
25088
  ↓
512
  ↓
ReLU
  ↓
Dropout(0.30)
  ↓
128
  ↓
ReLU
  ↓
Dropout(0.30)
  ↓
1
```

### VGG16 Sonuçları

| Metrik | Sonuç |
|---|---:|
| Epoch | **20** |
| Best Epoch | **18** |
| Best Validation MAE | **69.9705 m** |
| Test MAE | **66.7227 m** |
| Mean Signed Error | **-17.3877 m** |
| Maximum Absolute Error | **392.8829 m** |
| Test Görüntü Sayısı | **112** |

VGG16 modeli, proje önerisinde belirlenen:

> **MAE < 100 metre**

hedefini bağımsız test kümesi üzerinde karşılamıştır.

---

## ResNet50

ImageNet üzerinde önceden eğitilmiş ResNet50 modeli aynı veri bölme stratejisi ve temel eğitim koşulları altında değerlendirilmiştir.

ResNet50 backbone dondurulmuş ve model görüş mesafesi regresyonuna uyarlanmıştır.

### ResNet50 Sonuçları

| Metrik | Sonuç |
|---|---:|
| Epoch | **20** |
| Best Epoch | **20** |
| Best Validation MAE | **121.8414 m** |
| Test MAE | **124.6181 m** |
| Mean Signed Error | **-77.3460 m** |
| Maximum Absolute Error | **602.6687 m** |
| Test Görüntü Sayısı | **112** |

ResNet50 eğitim ve validation eğrileri birbirine yakın ilerlemiş ve klasik anlamda belirgin bir overfitting davranışı gözlenmemiştir.

Bununla birlikte özellikle yüksek görüş mesafesi seviyelerinde sistematik düşük tahmin eğilimi ve prediction-range compression davranışı gözlenmiştir.

---

# Baseline Karşılaştırması

VGG16 ve ResNet50 aynı sentetik veri kümesi, aynı scene-based split ve aynı temel deney koşulları altında karşılaştırılmıştır.

| Model | Best Validation MAE | Test MAE |
|---|---:|---:|
| **VGG16** | **69.9705 m** | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

Test MAE farkı:

```text
124.6181 - 66.7227 = 57.8954 m
```

Mevcut sentetik FRIDA/FRIDA2 deney aşamasında VGG16 daha düşük MAE üretmiştir.

Bu nedenle Attention Mechanism entegrasyonu için:

> **Selected Synthetic Baseline: VGG16**

olarak belirlenmiştir.

Bu sonuç yalnızca mevcut sentetik deney koşulları için geçerlidir ve VGG16'nın genel olarak ResNet50'den üstün olduğu anlamına gelmemektedir.

---

# Araştırma Hipotezi

Başlangıç hipotezinde residual learning avantajları nedeniyle ResNet50'nin VGG16'dan daha iyi performans göstermesi beklenmiştir.

Ancak mevcut sentetik baseline deneyleri bu hipotezi desteklememiştir.

Bu durum araştırma açısından başarısızlık olarak değil, deneysel bir bulgu olarak değerlendirilmektedir.

---

# Attention Mechanism

Baseline karşılaştırmasının ardından en başarılı sentetik baseline olan VGG16 için attention tabanlı bir mimari geliştirilmiştir.

SE ve CBAM yaklaşımları incelenmiş ve:

> **CBAM — Convolutional Block Attention Module**

seçilmiştir.

CBAM iki ardışık attention bileşeni kullanmaktadır:

```text
Channel Attention
        ↓
Spatial Attention
```

## Channel Attention

Channel Attention, hangi feature channel'larının görev açısından daha önemli olduğunu öğrenmeyi amaçlamaktadır.

Konfigürasyon:

```text
Input Channels: 512
Reduction Ratio: 16

512 → 32 → 512
```

Average Pooling ve Max Pooling birlikte kullanılmaktadır.

---

## Spatial Attention

Spatial Attention, feature map üzerindeki hangi bölgelerin görev açısından daha önemli olduğunu öğrenmeyi amaçlamaktadır.

Konfigürasyon:

```text
Average Projection
        +
Maximum Projection
        ↓
Concatenation
        ↓
7 × 7 Convolution
        ↓
Sigmoid
```

---

# VGG16 + CBAM Architecture

CBAM, VGG16'nın son convolutional bloğundan sonra ve final MaxPool katmanından önce entegre edilmiştir.

Genel mimari:

```text
Input Image
    ↓
Frozen VGG16 Feature Extractor
    ↓
[B, 512, 14, 14]
    ↓
CBAM
    ├── Channel Attention
    └── Spatial Attention
    ↓
Final MaxPool
    ↓
[B, 512, 7, 7]
    ↓
Regression Head
    ↓
Visibility Prediction
```

Baseline karşılaştırmasının kontrollü kalması amacıyla VGG16 regression head değiştirilmeden korunmuştur.

---

# Attention Model Validation

CBAM modülü üzerinde gerçekleştirilen shape testi:

```text
Input  : [2, 512, 14, 14]
Output : [2, 512, 14, 14]
```

VGG16 + CBAM model forward-pass testi:

```text
Input  : [2, 3, 224, 224]
Output : [2, 1]
```

Gerçek DataLoader batch'i ile uyumluluk testi:

```text
Images  : [16, 3, 224, 224]
Targets : [16]
Outputs : [16, 1]
```

başarıyla tamamlanmıştır.

---

# Trainable / Frozen Parameters

VGG16 + CBAM mimarisi için doğrulanan parametre yapısı:

| Parametre Grubu | Sayı |
|---|---:|
| Total Parameters | **27,658,915** |
| Frozen Parameters | **14,714,688** |
| Trainable Parameters | **12,944,227** |
| CBAM Trainable Parameters | **32,866** |
| Regression Head Trainable Parameters | **12,911,361** |

Transfer learning stratejisi:

```text
VGG16 Feature Extractor : Frozen
CBAM                    : Trainable
Regression Head         : Trainable
```

şeklindedir.

---

# Training Configuration

Baseline ve Attention deneyleri için temel deney ayarları:

| Parametre | Değer |
|---|---|
| Image Size | **224 × 224** |
| Batch Size | **16** |
| Epoch | **20** |
| Optimizer | **Adam** |
| Learning Rate | **1e-4** |
| Weight Decay | **1e-5** |
| Loss Function | **L1Loss / MAE** |
| Random Seed | **42** |
| Pretrained Weights | **ImageNet** |

Attention modeli için ayrı training pipeline ve checkpoint sistemi hazırlanmıştır.

---

# Evaluation Pipeline

Baseline modeller için evaluation pipeline aşağıdaki çıktıları otomatik olarak oluşturmaktadır:

- Test prediction CSV
- Evaluation summary JSON
- Markdown evaluation report
- Actual vs Predicted scatter plot
- Prediction error histogram
- Training / Validation learning curve
- Experiment log

Attention modeli de eğitim tamamlandıktan sonra aynı değerlendirme prensipleriyle bağımsız test kümesinde değerlendirilecektir.

---

# Tamamlanan Çalışmalar

- ✅ Literatür araştırması
- ✅ FRIDA ve FRIDA2 veri seti analizi
- ✅ Sentetik sis üretim pipeline'ı
- ✅ 672 görüntülük sentetik veri kümesi
- ✅ Veri doğrulama
- ✅ Scene-based splitting
- ✅ PyTorch DataLoader altyapısı
- ✅ Ortak preprocessing pipeline
- ✅ VGG16 transfer learning modeli
- ✅ VGG16 training pipeline
- ✅ VGG16 baseline training
- ✅ VGG16 evaluation pipeline
- ✅ VGG16 bağımsız test değerlendirmesi
- ✅ ResNet50 transfer learning modeli
- ✅ ResNet50 training pipeline
- ✅ ResNet50 baseline training
- ✅ ResNet50 evaluation pipeline
- ✅ ResNet50 bağımsız test değerlendirmesi
- ✅ VGG16 vs ResNet50 baseline karşılaştırması
- ✅ Sentetik baseline model seçimi
- ✅ Attention mekanizmalarının incelenmesi
- ✅ SE ve CBAM karşılaştırması
- ✅ CBAM seçimi
- ✅ Channel Attention implementasyonu
- ✅ Spatial Attention implementasyonu
- ✅ CBAM implementasyonu
- ✅ VGG16 + CBAM mimarisi
- ✅ Attention model forward-pass doğrulaması
- ✅ Frozen / trainable parameter doğrulaması
- ✅ VGG16 + CBAM training pipeline
- ✅ Attention mimari dokümantasyonu

---

# Devam Eden Çalışmalar

- 🚧 VGG16 + CBAM 20-epoch training
- 🚧 Attention model evaluation
- 🚧 VGG16 baseline vs VGG16 + CBAM performans karşılaştırması
- 🚧 Fine-tuning deneyleri
- 🚧 Gerçek dünya veri setlerinde değerlendirme
- 🚧 Flask tabanlı inference API
- 🚧 Web prototipi
- 🚧 Final TÜBİTAK raporu
- 🚧 Yayınlanabilir araştırma çıktısının hazırlanması

---

# Yol Haritası

- [x] Veri seti analizi
- [x] Sentetik veri kümesi oluşturulması
- [x] Veri ön işleme
- [x] Scene-based veri bölme
- [x] PyTorch DataLoader
- [x] VGG16 baseline
- [x] VGG16 evaluation
- [x] ResNet50 baseline
- [x] ResNet50 evaluation
- [x] Baseline model comparison
- [x] Synthetic baseline selection
- [x] Attention mechanism selection
- [x] CBAM implementation
- [x] VGG16 + CBAM architecture
- [x] Attention training pipeline
- [ ] VGG16 + CBAM training
- [ ] Attention evaluation
- [ ] Baseline vs Attention comparison
- [ ] Fine-tuning
- [ ] Real-world evaluation
- [ ] Flask API
- [ ] Web interface
- [ ] Final project report

---

# Mevcut Proje Durumu

Mevcut aşamada VGG16 ve ResNet50 baseline deneyleri tamamlanmıştır.

Sentetik FRIDA/FRIDA2 test kümesi üzerinde:

```text
VGG16 Test MAE    : 66.7227 m
ResNet50 Test MAE : 124.6181 m
```

elde edilmiştir.

VGG16 mevcut sentetik baseline olarak seçilmiş ve CBAM Attention Mechanism başarıyla mimariye entegre edilmiştir.

VGG16 + CBAM modeli için training pipeline hazırlanmış ve teknik validation testleri tamamlanmıştır.

Bir sonraki ana deney:

> **VGG16 + CBAM 20-epoch training**

aşamasıdır.

---

# Beklenen Çıktılar

Proje sonunda aşağıdaki çıktıların elde edilmesi hedeflenmektedir:

- VGG16 ve ResNet50 performans karşılaştırması
- Attention Mechanism performans analizi
- Sürekli görüş mesafesi regresyon modeli
- Sentetik ve gerçek dünya veri performans analizi
- Flask tabanlı web prototipi
- TÜBİTAK 2209-A final proje raporu
- Deney kayıtları ve değerlendirme raporları
- Yayınlanabilir araştırma çıktısı
- Açık kaynak GitHub repository

---

# Reproducibility

Deneylerin tekrarlanabilirliği için:

```text
Random Seed = 42
```

kullanılmaktadır.

Baseline modeller ve Attention modeli aynı veri split'lerini ve mümkün olduğunca aynı temel eğitim koşullarını kullanmaktadır.

Bu yaklaşım mimari değişikliklerin etkisinin daha kontrollü biçimde değerlendirilmesini amaçlamaktadır.

---

# Disclaimer

Bu repository aktif olarak geliştirilen akademik bir araştırma projesini içermektedir.

Mevcut performans sonuçları ağırlıklı olarak FRIDA ve FRIDA2 tabanlı sentetik sis görüntüleri üzerinde elde edilmiştir.

Bu nedenle mevcut sonuçlar gerçek dünya görüş mesafesi tahmin performansını doğrudan temsil etmemektedir.

Gerçek dünya veri setleri üzerindeki değerlendirmeler projenin sonraki aşamalarında gerçekleştirilecektir.

---

# Lisans

Bu proje **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında akademik araştırma amacıyla geliştirilmektedir.

Repository için açık kaynak lisanslama politikası proje ilerledikçe ayrıca belirlenecektir.