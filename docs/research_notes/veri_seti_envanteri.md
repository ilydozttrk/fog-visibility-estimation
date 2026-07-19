# Veri Seti Envanteri

## 1. Amaç

Bu doküman, TÜBİTAK 2209-A projesi kapsamında kullanılan veri setlerinin teknik özelliklerini, projedeki rollerini, seçim gerekçelerini ve veri hazırlama sürecini özetlemek amacıyla hazırlanmıştır.

Projenin temel amacı; sisli hava koşullarında görüntü tabanlı sürekli görüş mesafesi tahmini gerçekleştirmek için transfer öğrenme tabanlı VGG16 ve ResNet50 mimarilerini karşılaştırmak ve en başarılı modele Attention (Dikkat) mekanizması entegre etmektir.

Bu doğrultuda kullanılacak veri setlerinin hem bilimsel hem de teknik açıdan değerlendirilmesi, veri hazırlama sürecinin belgelenmesi ve model eğitimine uygun veri yapısının oluşturulması hedeflenmiştir.

---

# 2. Veri Seti Stratejisi

Projede iki aşamalı veri stratejisi benimsenmiştir.

## Aşama 1 — Sentetik Veri ile Temel Model Eğitimi

Kullanılan veri setleri

- FRIDA
- FRIDA2

Amaç

- Kontrollü eğitim ortamı oluşturmak
- VGG16 ve ResNet50 modellerini aynı koşullarda karşılaştırmak
- Sürekli görüş mesafesi regresyonu için etiketlenmiş sentetik veri kümesi oluşturmak

Bu aşamada FRIDA ve FRIDA2 veri setlerinde bulunan açık hava görüntüleri ve derinlik haritaları kullanılarak farklı görüş mesafelerini temsil eden yeni sentetik görüntüler oluşturulmuştur.

---

## Aşama 2 — Gerçek Dünya Verileri ile Fine-Tuning

Kullanılması planlanan veri setleri

- FVEI
- FHVI (erişilebilirlik durumuna bağlı)

Amaç

- Gerçek yol görüntülerinde model performansını değerlendirmek
- Sentetik veriden gerçek dünyaya geçiş başarısını analiz etmek
- Modelin genelleme yeteneğini artırmak

---

# 3. Veri Seti Özeti

## 3.1 FRIDA

### Veri Türü

Sentetik

### Kullanım Amacı

Sisli ortamların kontrollü olarak modellenmesi ve temel eğitim verisinin oluşturulması.

### İçerik

- 18 temel yol sahnesi
- RGB görüntüler
- Derinlik haritaları (.fdd)
- Açık hava referans görüntüleri

### Avantajları

- Kontrollü ortam
- Derinlik haritası içermesi
- Fiziksel sis modeli uygulanabilmesi

### Dezavantajları

- Küçük veri seti
- Gerçek dünya verisi değildir
- Hazır sürekli görüş mesafesi etiketi içermez

### Projedeki Rolü

Sentetik veri üretiminin başlangıç veri seti.

---

## 3.2 FRIDA2

### Veri Türü

Sentetik

### Kullanım Amacı

Ana sentetik eğitim veri seti.

### İçerik

- 66 temel yol sahnesi
- RGB görüntüler
- Derinlik haritaları
- Açık hava referans görüntüleri

### Avantajları

- Daha fazla sahne
- Daha çeşitli yol görüntüleri
- Derinlik haritası desteği

### Dezavantajları

- Gerçek dünya verisi değildir
- Hazır sürekli görüş mesafesi etiketi içermez

### Projedeki Rolü

Sentetik veri kümesinin büyük bölümünü oluşturmaktadır.

---

## 3.3 FVEI

### Veri Türü

Gerçek Dünya

### Kullanım Amacı

Fine-Tuning ve gerçek dünya performans değerlendirmesi.

### Avantajları

- Gerçek yol görüntüleri
- Sürekli görüş mesafesi bilgisi
- Gerçek trafik koşulları

### Dezavantajları

- Erişim kısıtlı olabilir

---

## 3.4 FHVI

### Veri Türü

Gerçek Dünya

### Kullanım Amacı

Alternatif gerçek dünya doğrulama veri seti.

### Avantajları

- Gerçek meteorolojik koşullar
- Gerçek trafik görüntüleri

### Dezavantajları

- Sürekli regresyon etiketi sınırlıdır
- Erişim durumu değişken olabilir

---

# 4. Oluşturulan Sentetik Veri Kümesi

FRIDA ve FRIDA2 veri setlerinde doğrudan sürekli görüş mesafesi etiketleri bulunmadığından proje kapsamında yeni bir sentetik veri kümesi oluşturulmuştur.

Veri üretim sürecinde

- açık hava görüntüleri
- derinlik haritaları
- atmosferik saçılım modeli

birlikte kullanılmıştır.

Her temel sahne için aşağıdaki görüş mesafeleri oluşturulmuştur.

- 50 m
- 80 m
- 100 m
- 150 m
- 200 m
- 300 m
- 500 m
- 800 m

### Toplam Sahne Sayısı

| Veri Seti | Sahne |
|-----------|------:|
| FRIDA | 18 |
| FRIDA2 | 66 |
| **Toplam** | **84** |

### Üretilen Görüntü Sayısı

84 sahne × 8 görüş mesafesi

= **672 sentetik görüntü**

---

# 5. Etiket Yapısı

Üretilen veri kümesine ait bilgiler `labels.csv` dosyasında tutulmaktadır.

Dosya aşağıdaki alanlardan oluşmaktadır.

| Alan | Açıklama |
|------|----------|
| filename | Görüntü yolu |
| visibility_m | Görüş mesafesi (metre) |
| scene_id | Sahne numarası |
| source_dataset | FRIDA / FRIDA2 |
| beta | Atmosferik saçılım katsayısı |
| clear_image | Kullanılan açık hava görüntüsü |
| depth_map | Kullanılan derinlik haritası |

Bu yapı sayesinde veri kümesi doğrudan PyTorch DataLoader tarafından okunabilmektedir.

---

# 6. Veri Setlerinin Karşılaştırılması

| Özellik | FRIDA | FRIDA2 | FVEI | FHVI |
|----------|--------|---------|---------|---------|
| Veri Türü | Sentetik | Sentetik | Gerçek | Gerçek |
| RGB Görüntü | ✓ | ✓ | ✓ | ✓ |
| Depth Map | ✓ | ✓ | ✗ | ✗ |
| Hazır Visibility Etiketi | ✗ | ✗ | ✓ | Kısmen |
| Sürekli Regresyon | Projede üretildi | Projede üretildi | ✓ | Sınırlı |
| Fine-Tuning | ✗ | ✗ | ✓ | Kısmen |
| Başlangıç Eğitimi | ✓ | ✓ | ✗ | ✗ |

---

# 7. Projede Kullanım Sırası

```
FRIDA
      │
      ▼
FRIDA2
      │
      ▼
Sahne Eşleştirme
      │
      ▼
Derinlik Haritaları
      │
      ▼
Sentetik Veri Üretimi
      │
      ▼
labels.csv
      │
      ▼
PyTorch Dataset
      │
      ▼
DataLoader
      │
      ▼
VGG16 Eğitimi
      │
      ▼
ResNet50 Eğitimi
      │
      ▼
Model Karşılaştırması
      │
      ▼
Attention
      │
      ▼
FVEI / FHVI
      │
      ▼
Fine-Tuning
      │
      ▼
Flask Prototipi
```

---

# 8. Olası Riskler

## Risk 1

Gerçek dünya veri setlerine erişimin kısıtlı olması.

**Çözüm**

Araştırma önerisinde belirtildiği şekilde veri seti sahipleriyle iletişime geçilecek veya erişilebilir alternatif veri setleri değerlendirilecektir.

---

## Risk 2

Sentetik veriden gerçek dünyaya geçişte performans kaybı yaşanması.

**Çözüm**

Fine-Tuning uygulanarak model gerçek dünya görüntülerine adapte edilecektir.

---

## Risk 3

FRIDA ve FRIDA2 veri setlerinde hazır sürekli görüş mesafesi etiketi bulunmaması.

**Çözüm**

Derinlik haritaları kullanılarak atmosferik saçılım modeli uygulanmış ve sürekli görüş mesafesi etiketlerine sahip sentetik veri kümesi oluşturulmuştur.

---

# 9. Sonuç

Proje kapsamında oluşturulan veri stratejisi araştırma önerisiyle uyumludur.

FRIDA ve FRIDA2 veri setlerinden yararlanılarak toplam **84 sahneden oluşan**, **672 görüntü içeren** sürekli görüş mesafesi etiketli sentetik veri kümesi hazırlanmıştır. Bu veri kümesi PyTorch tabanlı veri yükleme altyapısına entegre edilmiş olup VGG16 ve ResNet50 modellerinin eğitiminde kullanılmaya hazır durumdadır.

İlerleyen aşamada gerçek dünya veri setleri kullanılarak fine-tuning ve performans değerlendirme çalışmaları gerçekleştirilecektir.