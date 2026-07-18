# Sisli Hava Koşullarında Görüş Mesafesi Tahmini

Bu proje, sisli hava koşullarında görüntü tabanlı görüş mesafesi tahmini için transfer öğrenme temelli VGG16 ve ResNet50 CNN mimarilerinin karşılaştırmalı analizini gerçekleştirmeyi amaçlamaktadır.

Proje, TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı kapsamında yürütülmektedir.

---

## Araştırmanın Amacı

VGG16 ve ResNet50 modellerinin sürekli görüş mesafesi regresyonu görevindeki performansları Ortalama Mutlak Hata (MAE) metriği kullanılarak karşılaştırılacaktır.

Test veri seti üzerinde en düşük MAE değerini sağlayan model seçilecek ve seçilen modele Dikkat Mekanizması (Attention Mechanism) entegre edilerek performans artışı değerlendirilecektir.

---

## Araştırma Sorusu

Transfer öğrenme yöntemi ile görüntü tabanlı görüş mesafesi tahmini görevine adapte edilen VGG16 ve ResNet50 mimarilerinden hangisi daha düşük Ortalama Mutlak Hata (MAE) değeri sağlayarak Akıllı Ulaşım Sistemleri entegrasyonu için daha uygun bir temel model oluşturur?

---

## Planlanan Proje Süreci

1. FRIDA ve FRIDA2 veri setlerinin hazırlanması
2. Sürekli görüş mesafesi regresyon etiketlerinin hazırlanması
3. Veri ön işleme pipeline'ının geliştirilmesi
4. Eğitim, doğrulama ve test veri kümelerinin oluşturulması
5. VGG16 tabanlı transfer öğrenme modeli
6. ResNet50 tabanlı transfer öğrenme modeli
7. Modellerin MAE metriği ile karşılaştırılması
8. En başarılı modele Dikkat Mekanizması entegrasyonu
9. Gerçek dünya veri setleri üzerinde ince ayar (Fine-tuning)
10. Flask API ve HTML/CSS tabanlı web prototipi geliştirilmesi

---

## Veri Ön İşleme

FRIDA veri seti için yeniden kullanılabilir bir veri ön işleme modülü geliştirilmiştir.

Uygulanan işlemler:

- RGB formatında güvenli görüntü yükleme
- En-boy oranı korunarak 224×224 piksele yeniden boyutlandırma
- Siyah padding uygulanması
- İşlenmiş görüntülerin `data/processed/frida` klasörüne kaydedilmesi
- Dosya doğrulama ve hata yönetimi

Model mimarilerine özgü normalizasyon işlemleri (VGG16 / ResNet50 `preprocess_input`) eğitim aşamasında uygulanacaktır.

---

## Veri Seti Bölme Stratejisi

FRIDA veri seti, veri sızıntısını önlemek amacıyla **sahne bazlı (scene-based)** olarak bölünmektedir.

Aynı sahneye ait farklı sis varyasyonlarının farklı veri kümelerinde bulunmasına izin verilmemektedir.

Kullanılan bölme:

- Eğitim: **12 sahne (60 görüntü)**
- Doğrulama: **3 sahne (15 görüntü)**
- Test: **3 sahne (15 görüntü)**

Bölme işlemi tekrarlanabilir sonuçlar elde etmek amacıyla **Random Seed = 42** kullanılarak gerçekleştirilmiştir.

---

## Proje Yapısı

```
src/
├── api/
├── attention/
├── data/
│   ├── preprocessing.py
│   └── dataset_split.py
├── evaluation/
├── models/
└── training/
```

---

## Kullanılan Teknolojiler

- Python
- PyTorch
- Torchvision
- Pillow (PIL)
- NumPy
- Pandas
- Scikit-learn
- OpenCV
- Matplotlib
- Flask

---

## Proje Durumu

### Tamamlanan

- Veri seti araştırması
- FRIDA veri seti analizi
- Veri seti doğrulama
- Görüntü ön işleme pipeline'ı
- Sahne bazlı veri bölme sistemi

### Devam Eden

- Regresyon etiketlerinin hazırlanması
- VGG16 baseline modeli
- ResNet50 baseline modeli