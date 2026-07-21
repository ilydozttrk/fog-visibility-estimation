# Fog Visibility Estimation using Transfer Learning

Transfer öğrenme tabanlı derin evrişimsel sinir ağları (CNN) kullanılarak sisli hava koşullarında görüntü tabanlı görüş mesafesi tahmini gerçekleştirmeyi amaçlayan TÜBİTAK 2209-A araştırma projesidir.

Bu çalışma kapsamında ImageNet üzerinde önceden eğitilmiş **VGG16** ve **ResNet50** mimarileri karşılaştırılacak, en başarılı temel modele **Attention Mechanism** entegre edilerek performans artışı değerlendirilecektir.

---

# TÜBİTAK 2209-A Araştırma Projesi

**Proje Başlığı**

> Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

---

# Araştırmanın Amacı

Bu proje;

- görüntü tabanlı sürekli görüş mesafesi tahmini gerçekleştirmeyi,
- transfer öğrenme ile VGG16 ve ResNet50 modellerini karşılaştırmayı,
- en başarılı temel modele Attention Mechanism eklemeyi,
- gerçek dünya verileri üzerinde modeli değerlendirmeyi,
- Flask tabanlı bir web prototipi geliştirmeyi

amaçlamaktadır.

Temel performans metriği **Mean Absolute Error (MAE)** olarak belirlenmiştir.

---

# Araştırma Sorusu

Transfer öğrenme yöntemi ile görüş mesafesi tahmini görevine uyarlanan VGG16 ve ResNet50 mimarilerinden hangisi daha düşük MAE değeri üreterek Akıllı Ulaşım Sistemleri için daha uygun bir temel model sunmaktadır?

---

# Veri Seti

Projede başlangıç modeli için **FRIDA** ve **FRIDA2** veri setleri kullanılmaktadır.

Hazır sürekli görüş mesafesi etiketleri bulunmadığından derinlik haritaları kullanılarak sentetik görüş mesafesi görüntüleri oluşturulmuştur.

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
|---------|------:|
| Toplam sahne | **84** |
| Toplam görüntü | **672** |
| Görüş mesafesi seviyesi | **8** |

---

# Veri Bölme Stratejisi

Veri sızıntısını önlemek amacıyla **scene-based splitting** uygulanmıştır.

Aynı temel sahneye ait tüm görüntüler yalnızca tek veri kümesinde bulunmaktadır.

| Küme | Görüntü |
|------|---------:|
| Train | **464** |
| Validation | **96** |
| Test | **112** |

Bölme işlemi tamamen tekrarlanabilir olacak şekilde **Random Seed = 42** kullanılarak gerçekleştirilmiştir.

---

# Ön İşleme

Model eğitiminden önce aşağıdaki işlemler uygulanmaktadır.

- RGB formatına dönüştürme
- 224×224 yeniden boyutlandırma
- ImageNet normalizasyonu
- Scene-based veri bölme
- PyTorch DataLoader oluşturulması

Bu ön işleme süreci hem VGG16 hem de ResNet50 tarafından ortak kullanılmaktadır.

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
│   └── research_notes/
│
├── notebooks/
│
├── results/
│   ├── checkpoints/
│   ├── logs/
│   └── plots/
│
├── src/
│   ├── api/
│   ├── attention/
│   ├── data/
│   ├── evaluation/
│   ├── models/
│   └── training/
│
├── README.md
└── requirements.txt
```

---

# İlk Eğitim Sonuçları

# VGG16 Baseline Results

İlk VGG16 transfer öğrenme tabanlı baseline modeli başarıyla eğitilmiş ve bağımsız test kümesi üzerinde değerlendirilmiştir.

| Metrik | Sonuç |
|--------|------:|
| Epoch | **20** |
| Best Epoch | **18** |
| Best Validation MAE | **69.9705 m** |
| Test MAE | **66.7227 m** |
| Test Görüntü Sayısı | **112** |

Model, proje önerisinde belirlenen

> **MAE < 100 metre**

hedefini hem doğrulama hem de bağımsız test kümesi üzerinde başarıyla karşılamıştır.

Evaluation pipeline kapsamında aşağıdaki çıktılar otomatik olarak oluşturulmaktadır:

- Test prediction CSV
- Evaluation summary JSON
- Markdown evaluation report
- Actual vs Predicted scatter plot
- Prediction error histogram

---

# Tamamlanan Çalışmalar

- ✅ Literatür araştırması
- ✅ Veri seti analizi
- ✅ FRIDA ve FRIDA2 incelemesi
- ✅ Sentetik veri kümesinin oluşturulması
- ✅ Veri doğrulama süreci
- ✅ Ön işleme pipeline'ı
- ✅ Scene-based veri bölme
- ✅ PyTorch veri yükleme altyapısı
- ✅ VGG16 transfer öğrenme modeli
- ✅ Eğitim pipeline'ı
- ✅ Checkpoint sistemi
- ✅ Deney kayıt sistemi
- ✅ VGG16 baseline eğitimi
- ✅ VGG16 evaluation pipeline
- ✅ Test kümesi değerlendirmesi
- ✅ Otomatik değerlendirme raporu ve grafik üretimi

---

# Devam Eden Çalışmalar

# Devam Eden Çalışmalar

- 🚧 ResNet50 baseline modeli
- 🚧 ResNet50 evaluation pipeline
- 🚧 VGG16 ve ResNet50 performans karşılaştırması
- 🚧 Attention Mechanism entegrasyonu
- 🚧 Fine-tuning çalışmaları
- 🚧 Gerçek dünya veri kümelerinde değerlendirme
- 🚧 Flask tabanlı web prototipi

---

# Yol Haritası

# Yol Haritası

- [x] Veri seti analizi
- [x] Sentetik veri kümesi oluşturulması
- [x] Veri ön işleme
- [x] Scene-based veri bölme
- [x] PyTorch DataLoader
- [x] VGG16 baseline
- [x] VGG16 evaluation
- [ ] ResNet50 baseline
- [ ] ResNet50 evaluation
- [ ] Model comparison
- [ ] Attention Mechanism
- [ ] Fine-tuning
- [ ] Flask API
- [ ] Web interface

---

# Beklenen Çıktılar

# Beklenen Çıktılar

- VGG16 ve ResNet50 performans karşılaştırması
- Attention Mechanism performans analizi
- Görüş mesafesi regresyon modeli
- Flask tabanlı web prototipi
- TÜBİTAK 2209-A proje raporu
- Deney kayıtları ve değerlendirme raporları
- Açık kaynak GitHub deposu

---

# Lisans

Bu proje, **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında akademik araştırma amacıyla geliştirilmektedir.