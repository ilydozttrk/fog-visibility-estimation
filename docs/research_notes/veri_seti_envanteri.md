# Veri Seti Envanteri

## 1. Amaç

Bu doküman, TÜBİTAK 2209-A projesi kapsamında kullanılacak veri setlerinin teknik özelliklerini, projedeki rollerini ve seçim gerekçelerini özetlemek amacıyla hazırlanmıştır.

Projenin temel amacı; sisli hava koşullarında görüntü tabanlı sürekli görüş mesafesi tahmini gerçekleştirmek için transfer öğrenme tabanlı VGG16 ve ResNet50 mimarilerini karşılaştırmak ve en başarılı modele dikkat (Attention) mekanizması entegre etmektir.

Bu doğrultuda kullanılacak veri setlerinin hem bilimsel hem de teknik açıdan değerlendirilmesi gerekmektedir.

---

# 2. Veri Seti Stratejisi

Projede iki aşamalı veri stratejisi benimsenmiştir.

## Aşama 1

Sentetik veri kullanılarak temel model eğitimi.

Kullanılacak veri setleri:

- FRIDA
- FRIDA2

Amaç:

- modellerin sis etkisini öğrenmesi
- kontrollü karşılaştırma yapılması
- VGG16 ve ResNet50'nin aynı koşullarda eğitilmesi

---

## Aşama 2

Gerçek dünya verileri ile ince ayar (Fine-Tuning) ve değerlendirme.

Kullanılacak veri setleri:

- FVEI
- FHVI (erişim ve uygunluk durumuna bağlı)

Amaç:

- gerçek yol görüntülerinde model performansını değerlendirmek
- sentetik veriden gerçek dünyaya geçiş başarısını ölçmek

---

# 3. Veri Seti Özeti

## 3.1 FRIDA

### Veri Türü

Sentetik

### Kullanım Amacı

Sis giderme, görünürlük iyileştirme ve görüntü işleme algoritmalarının değerlendirilmesi.

### İçerik

- 18 temel yol sahnesi
- yaklaşık 90 görüntü
- depth map
- farklı sis türleri

### Avantajları

- kontrollü ortam
- depth map
- farklı sis senaryoları

### Dezavantajları

- küçük veri seti
- gerçek dünya değildir
- hazır görüş mesafesi etiketi içermez

### Projedeki Rolü

Başlangıç eğitimi.

---

## 3.2 FRIDA2

### Veri Türü

Sentetik

### Kullanım Amacı

FRIDA'nın geliştirilmiş sürümü.

### İçerik

- 66 temel sahne
- yaklaşık 330 görüntü
- depth map
- dört farklı sis türü

### Avantajları

- daha büyük
- daha çeşitli
- daha fazla eğitim örneği

### Dezavantajları

- sentetik veri
- hazır sürekli görüş mesafesi etiketi içermez

### Projedeki Rolü

Ana sentetik eğitim veri seti.

---

## 3.3 FVEI

### Veri Türü

Gerçek Dünya

### Kullanım Amacı

Görüntü tabanlı görüş mesafesi tahmini.

### İçerik

Yaklaşık 15.000 gerçek otoyol görüntüsü.

Her görüntü için

- sis seviyesi
- görüş mesafesi

etiketi bulunmaktadır.

### Avantajları

- gerçek veri
- büyük veri seti
- uzman etiketleme

### Dezavantajları

- erişim kısıtlı olabilir

### Projedeki Rolü

Fine-Tuning ve gerçek dünya değerlendirmesi.

---

## 3.4 FHVI

### Veri Türü

Gerçek Dünya

### Kullanım Amacı

Gerçek otoyol görüntülerinde görünürlük seviyesi tahmini.

### İçerik

Meteoroloji istasyonları ile ilişkilendirilmiş gerçek yol görüntüleri.

### Avantajları

- gerçek veri
- meteorolojik doğrulama
- uzman etiketleme

### Dezavantajları

- sürekli görüş mesafesi yerine görünürlük seviyesi kullanmaktadır.

### Projedeki Rolü

Alternatif gerçek dünya doğrulama veri seti.

---

# 4. Veri Setlerinin Karşılaştırılması

| Özellik | FRIDA | FRIDA2 | FVEI | FHVI |
|----------|--------|---------|---------|---------|
| Veri Türü | Sentetik | Sentetik | Gerçek | Gerçek |
| Yol Görüntüsü | ✓ | ✓ | ✓ | ✓ |
| Depth Map | ✓ | ✓ | ✗ | ✗ |
| Hazır Visibility Etiketi | ✗ | ✗ | ✓ | Kısmen |
| Sürekli Regresyon | Etiket üretilecek | Etiket üretilecek | ✓ | Sınırlı |
| Fine-Tuning | ✗ | ✗ | ✓ | Kısmen |
| Başlangıç Eğitimi | ✓ | ✓ | ✗ | ✗ |

---

# 5. Veri Seti Seçim Kriterleri

Veri setleri aşağıdaki kriterlere göre değerlendirilmiştir.

- Araştırma problemine uygunluk
- Sürekli görüş mesafesi tahmini yapılabilmesi
- Transfer öğrenme için uygunluk
- Veri çeşitliliği
- Görüntü kalitesi
- Etiket güvenilirliği
- Gerçek dünya temsil gücü
- Akademik çalışmalarda yaygın kullanımı
- Erişilebilirlik

---

# 6. Projede Kullanım Sırası

```
FRIDA
      │
      ▼
FRIDA2
      │
      ▼
Veri Hazırlama
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
FVEI
      │
      ▼
Gerçek Dünya Fine-Tuning
      │
      ▼
Flask Prototipi
```

---

# 7. Olası Riskler

## Risk 1

Gerçek dünya veri setlerine erişimin kısıtlı olması.

Çözüm:

Araştırma önerisinde belirtildiği gibi yayın yazarları ile iletişime geçilebilir.

---

## Risk 2

Sentetik veriden gerçek dünyaya geçişte performans kaybı.

Çözüm:

Fine-Tuning uygulanacaktır.

---

## Risk 3

FRIDA ve FRIDA2 veri setlerinde doğrudan sürekli görüş mesafesi etiketi bulunmaması.

Çözüm:

Araştırma önerisinde planlandığı şekilde derinlik haritaları kullanılarak uygun regresyon hedefleri oluşturulacaktır.

---

# 8. Sonuç

Mevcut incelemeler doğrultusunda proje veri stratejisi bilimsel olarak uygun görünmektedir.

FRIDA ve FRIDA2 veri setleri kontrollü başlangıç eğitimi için yeterli altyapıyı sağlamaktadır.

Gerçek dünya genellemesi ise FVEI ve gerektiğinde FHVI veri setleri ile desteklenecektir.

Bu yaklaşım, araştırma önerisinde tanımlanan proje metodolojisi ile uyumludur.