# Veri Seti Envanteri

## 1. Amaç

Bu doküman, TÜBİTAK 2209-A projesi kapsamında kullanılan ve değerlendirilen veri setlerinin teknik özelliklerini, projedeki rollerini, seçim gerekçelerini ve veri hazırlama sürecini özetlemek amacıyla hazırlanmıştır.

Projenin temel amacı; sisli hava koşullarında görüntü tabanlı sürekli görüş mesafesi tahmini gerçekleştirmek için transfer öğrenme tabanlı VGG16 ve ResNet50 mimarilerini karşılaştırmak, bağımsız test performansına göre en uygun baseline mimariyi belirlemek ve seçilen modele Attention Mechanism entegre etmektir.

Bu doğrultuda veri setlerinin bilimsel ve teknik açıdan değerlendirilmesi, veri hazırlama sürecinin belgelenmesi, veri sızıntısının önlenmesi ve modellerin karşılaştırılabileceği tekrarlanabilir bir veri yapısının oluşturulması hedeflenmiştir.

---

# 2. Veri Seti Stratejisi

Projede iki aşamalı veri stratejisi benimsenmiştir.

## Aşama 1 — Sentetik Veri ile Baseline Model Geliştirme

Kullanılan veri setleri:

- FRIDA
- FRIDA2

Amaç:

- Kontrollü deney ortamı oluşturmak
- VGG16 ve ResNet50 modellerini aynı veri koşullarında karşılaştırmak
- Sürekli görüş mesafesi regresyonu için etiketlenmiş sentetik veri kümesi oluşturmak
- Attention Mechanism entegrasyonu öncesinde baseline performanslarını belirlemek

Bu aşamada FRIDA ve FRIDA2 veri setlerindeki açık hava görüntüleri ve derinlik haritaları kullanılarak farklı görüş mesafelerini temsil eden yeni sentetik görüntüler oluşturulmuştur.

Oluşturulan sentetik veri kümesi hem VGG16 hem de ResNet50 baseline modellerinin geliştirilmesi, eğitilmesi ve bağımsız test değerlendirmesi için başarıyla kullanılmıştır.

---

## Aşama 2 — Gerçek Dünya Verileri ile Fine-Tuning ve Değerlendirme

Kullanılması değerlendirilen veri setleri:

- FVEI
- FHVI

Amaç:

- Gerçek yol görüntülerinde model performansını değerlendirmek
- Sentetik veriden gerçek dünya görüntülerine geçiş başarısını analiz etmek
- Uygun etiket yapısı bulunması durumunda fine-tuning gerçekleştirmek
- Modelin gerçek dünya genelleme yeteneğini incelemek

Bu aşama veri setlerinin erişilebilirliği, etiket yapısı ve proje kapsamına uygunluğu doğrultusunda gerçekleştirilecektir.

---

# 3. Veri Seti Özeti

## 3.1 FRIDA

### Veri Türü

Sentetik

### Kullanım Amacı

Sisli ortamların kontrollü olarak modellenmesi ve sentetik regresyon veri kümesinin oluşturulması.

### İçerik

- 18 temel yol sahnesi
- RGB görüntüler
- Derinlik haritaları (`.fdd`)
- Açık hava referans görüntüleri

### Avantajları

- Kontrollü ortam sunması
- Derinlik haritaları içermesi
- Fiziksel sis modelinin uygulanabilmesine olanak sağlaması
- Scene-based veri organizasyonuna uygun olması

### Dezavantajları

- Küçük ölçekli olması
- Gerçek dünya görüntülerini doğrudan temsil etmemesi
- Hazır sürekli görüş mesafesi etiketi içermemesi
- Sentetik-gerçek veri arasında domain farkı bulunabilmesi

### Projedeki Rolü

FRIDA, sentetik veri üretiminin başlangıç veri kaynaklarından biri olarak kullanılmıştır.

---

## 3.2 FRIDA2

### Veri Türü

Sentetik

### Kullanım Amacı

Sentetik veri kümesinin ana sahne çeşitliliğini sağlamak.

### İçerik

- 66 temel yol sahnesi
- RGB görüntüler
- Derinlik haritaları
- Açık hava referans görüntüleri

### Avantajları

- FRIDA'dan daha fazla sahne içermesi
- Daha yüksek sahne çeşitliliği sağlaması
- Derinlik haritaları içermesi
- Kontrollü sentetik veri üretimine uygun olması

### Dezavantajları

- Gerçek dünya verisi olmaması
- Hazır sürekli görüş mesafesi etiketi içermemesi
- Modern büyük ölçekli derin öğrenme veri setlerine kıyasla sınırlı sahne sayısına sahip olması

### Projedeki Rolü

FRIDA2, oluşturulan sentetik veri kümesinin büyük bölümünü oluşturmaktadır.

---

## 3.3 FVEI

### Veri Türü

Gerçek Dünya

### Kullanım Amacı

Gerçek dünya performans değerlendirmesi ve uygunluk durumunda fine-tuning.

### Avantajları

- Gerçek yol görüntüleri içermesi
- Görüş mesafesi bilgisi sağlaması
- Gerçek trafik ve atmosfer koşullarını temsil etmesi
- Sentetik veri üzerinde eğitilmiş modelin domain adaptasyonu açısından değerli olması

### Dezavantajları

- Erişim kısıtlı olabilir
- Kullanım koşullarının ayrıca doğrulanması gerekebilir
- Projedeki mevcut sentetik veri etiket yapısıyla doğrudan uyumluluk kontrolü gerektirir

### Projedeki Rolü

Sentetik baseline aşamasından sonra gerçek dünya davranışının değerlendirilmesi için öncelikli aday veri setidir.

---

## 3.4 FHVI

### Veri Türü

Gerçek Dünya

### Kullanım Amacı

Alternatif gerçek dünya doğrulama veri seti.

### Avantajları

- Gerçek meteorolojik koşullar içermesi
- Gerçek trafik görüntüleri sağlaması
- Modelin sentetik veri dışındaki davranışının incelenmesine olanak vermesi

### Dezavantajları

- Sürekli regresyon etiketi açısından sınırlı olması
- Ayrık visibility level yapısının projenin sürekli regresyon problemiyle doğrudan uyumlu olmaması
- Erişim durumunun değişken olabilmesi

### Projedeki Rolü

Temel sürekli regresyon eğitimi için değil, uygunluk durumunda ek gerçek dünya doğrulaması amacıyla değerlendirilmektedir.

---

# 4. Oluşturulan Sentetik Veri Kümesi

FRIDA ve FRIDA2 veri setlerinde doğrudan proje kapsamında kullanılabilecek metre cinsinden sürekli görüş mesafesi etiketleri bulunmadığından yeni bir sentetik veri kümesi oluşturulmuştur.

Veri üretim sürecinde:

- açık hava görüntüleri,
- derinlik haritaları,
- atmosferik saçılım modeli

birlikte kullanılmıştır.

Her temel sahne için aşağıdaki görüş mesafesi seviyeleri oluşturulmuştur:

- 50 m
- 80 m
- 100 m
- 150 m
- 200 m
- 300 m
- 500 m
- 800 m

## Toplam Sahne Sayısı

| Veri Seti | Sahne |
| --- | ---: |
| FRIDA | 18 |
| FRIDA2 | 66 |
| **Toplam** | **84** |

## Üretilen Görüntü Sayısı

```text
84 sahne × 8 görüş mesafesi = 672 görüntü
```

Toplam **672 sentetik görüntü** oluşturulmuştur.

---

# 5. Etiket Yapısı

Üretilen veri kümesine ait bilgiler `labels.csv` dosyasında tutulmaktadır.

Dosya aşağıdaki alanlardan oluşmaktadır:

| Alan | Açıklama |
| --- | --- |
| `filename` | Görüntü yolu |
| `visibility_m` | Görüş mesafesi (metre) |
| `scene_id` | Temel sahne kimliği |
| `source_dataset` | FRIDA / FRIDA2 |
| `beta` | Atmosferik saçılım katsayısı |
| `clear_image` | Kullanılan açık hava görüntüsü |
| `depth_map` | Kullanılan derinlik haritası |

Bu yapı sayesinde veri kümesi PyTorch tabanlı `FogVisibilityDataset` tarafından doğrudan okunabilmektedir.

`scene_id` alanı aynı sahneye ait görüntülerin farklı training, validation ve test kümelerine dağılmasını önlemek amacıyla scene-based split işleminde kullanılmaktadır.

---

# 6. Scene-Based Veri Bölme

Model değerlendirmesinde veri sızıntısını önlemek amacıyla görüntü bazlı rastgele split yerine **scene-based split** uygulanmıştır.

Aynı temel sahneye ait sekiz görüş mesafesi varyasyonu aynı veri alt kümesinde tutulmaktadır.

Bu sayede modelin test aşamasında training sırasında gördüğü bir sahnenin farklı sis varyasyonlarıyla karşılaşması engellenmiştir.

Hedeflenen oranlar:

- Training: %70
- Validation: %15
- Test: %15

şeklinde belirlenmiştir.

Sahne bazlı ayrım sonucunda elde edilen gerçek görüntü dağılımı:

| Veri Kümesi | Görüntü Sayısı |
| --- | ---: |
| Training | **464** |
| Validation | **96** |
| Test | **112** |
| **Toplam** | **672** |

şeklindedir.

Aynı veri bölünmesi hem VGG16 hem de ResNet50 baseline deneylerinde kullanılmıştır.

Deneylerin tekrarlanabilirliği için:

```text
RANDOM_SEED = 42
```

değeri sabit tutulmuştur.

---

# 7. Veri Setlerinin Karşılaştırılması

| Özellik | FRIDA | FRIDA2 | FVEI | FHVI |
| --- | --- | --- | --- | --- |
| Veri Türü | Sentetik | Sentetik | Gerçek | Gerçek |
| RGB Görüntü | ✓ | ✓ | ✓ | ✓ |
| Depth Map | ✓ | ✓ | ✗ | ✗ |
| Hazır Visibility Etiketi | ✗ | ✗ | ✓ | Kısmen / seviye tabanlı |
| Sürekli Regresyon | Projede üretildi | Projede üretildi | Uygun aday | Sınırlı |
| Baseline Eğitimi | ✓ | ✓ | ✗ | ✗ |
| Gerçek Dünya Değerlendirmesi | ✗ | ✗ | Planlanıyor | Uygunluk durumuna bağlı |
| Fine-Tuning | ✗ | ✗ | Uygunluk durumunda | Sınırlı / uygunluk durumunda |

---

# 8. Projede Kullanım Sırası

```text
FRIDA + FRIDA2
        │
        ▼
Açık Hava Görüntüleri + Derinlik Haritaları
        │
        ▼
Atmosferik Saçılım Modeli
        │
        ▼
672 Sentetik Görüntü
        │
        ▼
labels.csv
        │
        ▼
Scene-Based Split
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
     Train          Validation       Test
     464              96             112
        │
        ▼
FogVisibilityDataset
        │
        ▼
PyTorch DataLoader
        │
        ▼
VGG16 Baseline
        │
        ▼
ResNet50 Baseline
        │
        ▼
Baseline Karşılaştırması
        │
        ▼
En Başarılı Mimari
        │
        ▼
Attention Mechanism
        │
        ▼
Attention Model Evaluation
        │
        ▼
FVEI / FHVI
(Uygunluk ve erişim durumuna bağlı)
        │
        ▼
Gerçek Dünya Değerlendirmesi / Fine-Tuning
        │
        ▼
Flask Prototipi
```

---

# 9. Baseline Deneylerinde Veri Kullanımı

Hazırlanan 672 görüntülük sentetik veri kümesi proje kapsamında geliştirilen iki temel modelde başarıyla kullanılmıştır.

## VGG16

VGG16 modeli:

- 464 training görüntüsü,
- 96 validation görüntüsü,
- 112 bağımsız test görüntüsü

kullanılarak geliştirilmiştir.

Elde edilen sonuçlar:

| Metrik | Sonuç |
| --- | ---: |
| Best Validation MAE | **69.9705 m** |
| Test MAE | **66.7227 m** |
| Mean Signed Error | **−17.3877 m** |

VGG16, araştırma önerisindeki **MAE < 100 m** hedefini karşılamıştır.

---

## ResNet50

ResNet50 modeli aynı scene-based split ve aynı veri hazırlama pipeline'ı kullanılarak geliştirilmiştir.

Elde edilen sonuçlar:

| Metrik | Sonuç |
| --- | ---: |
| Best Validation MAE | **121.8414 m** |
| Test MAE | **124.6181 m** |
| Mean Signed Error | **−77.3460 m** |
| Maximum Absolute Error | **602.6687 m** |

Validation MAE ile Test MAE arasındaki fark yalnızca **2.7767 m** olarak ölçülmüştür.

Day 14 değerlendirmesinde modelin belirgin bir overfitting davranışı göstermediği; ancak özellikle yüksek görüş mesafelerinde sistematik düşük tahmin yaptığı gözlemlenmiştir.

Model tahminlerinin ground-truth hedef aralığından daha dar bir bölgede yoğunlaşması **prediction-range compression** olarak kaydedilmiştir.

Bu gözlemin nedeninin doğrudan veri setinden kaynaklandığı sonucuna varılmamıştır. Veri dağılımı yalnızca ileride incelenebilecek olası faktörlerden biridir.

---

# 10. Veri Stratejisinin Bilimsel Önemi

Projede kullanılan veri stratejisinin temel amacı yalnızca yeterli sayıda görüntü oluşturmak değildir.

Strateji aynı zamanda model karşılaştırmasının bilimsel olarak güvenilir olmasını sağlamayı hedeflemektedir.

Bu nedenle:

- Aynı veri kümesi her iki baseline modelde kullanılmıştır.
- Scene-based split uygulanmıştır.
- Test kümesi model geliştirme sırasında kullanılmamıştır.
- Random seed sabit tutulmuştur.
- Aynı preprocessing pipeline kullanılmıştır.
- Aynı test kümesi üzerinde bağımsız evaluation gerçekleştirilmiştir.

Bu yapı sayesinde VGG16 ve ResNet50 arasındaki performans farkının farklı veri split'lerinden kaynaklanma olasılığı azaltılmıştır.

---

# 11. Olası Riskler

## Risk 1 — Gerçek Dünya Veri Setlerine Erişimin Kısıtlı Olması

Gerçek dünya veri setlerinin doğrudan indirilememesi veya kullanım koşullarının sınırlı olması mümkündür.

### Çözüm

Araştırma önerisinde belirtildiği şekilde veri seti sahipleriyle iletişime geçilecek veya proje problemine uygun erişilebilir alternatif gerçek dünya veri kaynakları değerlendirilecektir.

Sentetik baseline deneyleri gerçek dünya veri erişiminden bağımsız olarak sürdürülebilmektedir.

---

## Risk 2 — Sentetik Veriden Gerçek Dünyaya Geçişte Performans Kaybı

Sentetik görüntüler ile gerçek atmosfer ve kamera koşulları arasında domain farkı bulunabilir.

### Çözüm

Uygun gerçek dünya veri kümesi elde edilmesi durumunda:

- gerçek dünya evaluation,
- fine-tuning,
- sentetik-gerçek performans karşılaştırması

gerçekleştirilecektir.

---

## Risk 3 — Hazır Sürekli Görüş Mesafesi Etiketlerinin Bulunmaması

FRIDA ve FRIDA2 doğrudan proje için kullanılabilir sürekli görüş mesafesi etiketleri sağlamamaktadır.

### Çözüm

Derinlik haritaları ve atmosferik saçılım modeli kullanılarak metre cinsinden hedef değerlere sahip sentetik veri kümesi oluşturulmuştur.

Bu risk proje kapsamında teknik olarak giderilmiştir.

---

## Risk 4 — Scene Leakage

Aynı temel sahneye ait farklı görüş mesafesi görüntülerinin training ve test kümelerine dağılması değerlendirme sonuçlarını yapay biçimde yükseltebilir.

### Çözüm

Scene-based split uygulanarak aynı temel sahneye ait tüm görüntüler tek bir veri alt kümesinde tutulmuştur.

---

## Risk 5 — Target Range Davranışı

ResNet50 değerlendirmesinde özellikle yüksek görüş mesafelerinde sistematik underestimation ve prediction-range compression gözlemlenmiştir.

Bu davranışın hedef dağılımı, model mimarisi, frozen backbone veya eğitim süresi gibi çeşitli faktörlerle ilişkili olması mümkündür.

### Çözüm

Mevcut sonuç üzerinden nedensel bir sonuca varılmayacaktır.

Gerekli görülmesi durumunda hedef değerlerine göre hata dağılımı ve farklı deney konfigürasyonları ayrıca incelenecektir.

---

# 12. Güncel Durum — Day 14

Day 14 itibarıyla veri hazırlama aşaması tamamen uygulanmış ve iki baseline deneyinde doğrulanmıştır.

Tamamlanan çalışmalar:

- ✓ FRIDA veri seti incelendi.
- ✓ FRIDA2 veri seti incelendi.
- ✓ FVEI araştırıldı.
- ✓ FHVI araştırıldı.
- ✓ Sentetik veri üretim pipeline'ı geliştirildi.
- ✓ 84 sahneden 672 görüntü oluşturuldu.
- ✓ `labels.csv` oluşturuldu.
- ✓ Sentetik veri bütünlüğü doğrulandı.
- ✓ Scene-based split uygulandı.
- ✓ Training / validation / test ayrımı tamamlandı.
- ✓ PyTorch `FogVisibilityDataset` geliştirildi.
- ✓ DataLoader altyapısı tamamlandı.
- ✓ VGG16 aynı veri üzerinde eğitildi ve değerlendirildi.
- ✓ ResNet50 aynı veri üzerinde eğitildi ve değerlendirildi.
- ✓ Bağımsız test kümesi her iki baseline için kullanıldı.
- ✓ ResNet50 hata davranışı görsel olarak analiz edildi.
- ⏳ Baseline karşılaştırmasının resmi olarak tamamlanması.
- ⏳ Attention modelinin geliştirilmesi.
- ⏳ Gerçek dünya veri aşamasının uygulanabilirliğinin kesinleştirilmesi.

---

# 13. Sonuç

Proje kapsamında FRIDA ve FRIDA2 veri setlerinden yararlanılarak toplam **84 temel sahneden** ve **672 sentetik görüntüden** oluşan sürekli görüş mesafesi etiketli veri kümesi başarıyla hazırlanmıştır.

Oluşturulan veri:

- **464 training görüntüsü**
- **96 validation görüntüsü**
- **112 test görüntüsü**

olacak şekilde scene-based split yaklaşımıyla ayrılmıştır.

Aynı veri hazırlama ve bölme pipeline'ı hem VGG16 hem de ResNet50 modellerinde başarıyla kullanılmıştır.

VGG16:

- **69.9705 m Validation MAE**
- **66.7227 m Test MAE**

elde ederken ResNet50:

- **121.8414 m Validation MAE**
- **124.6181 m Test MAE**

elde etmiştir.

Bu sonuçlarla sentetik veri stratejisinin iki bağımsız baseline modelin kontrollü ve tekrarlanabilir koşullarda karşılaştırılmasına olanak sağladığı doğrulanmıştır.

Projenin sonraki aşamasında VGG16 ve ResNet50 sonuçları ayrıntılı biçimde karşılaştırılacak, en başarılı baseline mimari belirlenecek ve Attention Mechanism entegrasyonu gerçekleştirilecektir.

Gerçek dünya veri setleri ise erişilebilirlik, etiket uygunluğu ve proje metodolojisi doğrultusunda gerçek dünya değerlendirmesi ve gerektiğinde fine-tuning amacıyla kullanılacaktır.