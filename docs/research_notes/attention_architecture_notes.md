# Attention-Enhanced VGG16 — Mimari Tasarım Notları

## Amaç

Bu doküman, TÜBİTAK 2209-A projesinde baseline model karşılaştırmasının ardından seçilen VGG16 mimarisine Attention Mechanism entegrasyonu için alınan teknik kararları belgelemektedir.

Day 15 kapsamında gerçekleştirilen VGG16 ve ResNet50 baseline karşılaştırmasında VGG16, mevcut FRIDA/FRIDA2 kaynaklı sentetik test veri kümesi üzerinde **66.7227 m Test MAE** ile en başarılı baseline model olarak belirlenmiştir.

Bu nedenle Attention Mechanism deneylerinde temel mimari olarak VGG16 kullanılacaktır.

Attention entegrasyonunun amacı, CNN tarafından çıkarılan feature map'ler içerisindeki daha önemli özellikleri ve uzamsal bölgeleri adaptif olarak ağırlıklandırarak görüş mesafesi regresyon performansına etkisini deneysel olarak incelemektir.

---

## Attention Mekanizması Seçimi

Proje kapsamında CNN mimarilerine uygulanabilecek attention yaklaşımları incelenmiş ve özellikle Squeeze-and-Excitation (SE) ile Convolutional Block Attention Module (CBAM) değerlendirilmiştir.

SE yaklaşımı temel olarak channel attention uygularken CBAM iki ardışık attention mekanizması kullanmaktadır:

1. Channel Attention
2. Spatial Attention

Görüş mesafesi tahmini probleminde yalnızca hangi feature channel'larının önemli olduğu değil, görüntünün hangi uzamsal bölgelerinin bilgi taşıdığı da önemli olabileceğinden **CBAM kullanılmasına karar verilmiştir**.

Bu seçim CBAM'ın performansı kesin olarak artıracağı varsayımına dayanmamaktadır. Attention mekanizmasının katkısı kontrollü deney sonucunda değerlendirilecektir.

---

## CBAM Genel Yapısı

CBAM, VGG16 tarafından oluşturulan feature map üzerinde sırasıyla Channel Attention ve Spatial Attention uygular.

Genel işlem akışı:

```text
VGG16 Feature Map
        │
        ▼
Channel Attention
        │
        ▼
Spatial Attention
        │
        ▼
Attended Feature Map
```

CBAM giriş tensorunun channel ve spatial boyutlarını değiştirmez.

Projedeki kullanım için:

```text
Input  : [B, 512, 14, 14]
Output : [B, 512, 14, 14]
```

şeklinde çalışması doğrulanmıştır.

---

## Channel Attention

Channel Attention'ın amacı, feature map içerisindeki hangi feature channel'larının mevcut görüntü için daha önemli olduğunu öğrenmektir.

Girdi feature map'i:

```text
[B, 512, 14, 14]
```

üzerinde hem Adaptive Average Pooling hem de Adaptive Max Pooling uygulanmaktadır.

Her iki işlem sonucunda:

```text
[B, 512, 1, 1]
```

boyutunda temsil elde edilmektedir.

Bu temsiller ortak bir öğrenilebilir dönüşümden geçirilir.

Projede kullanılan reduction ratio:

```text
16
```

olarak belirlenmiştir.

Buna göre channel dönüşümü:

```text
512 → 32 → 512
```

şeklindedir.

Average ve maximum pooling yollarından elde edilen çıktılar birleştirildikten sonra sigmoid aktivasyonu uygulanarak channel attention ağırlıkları oluşturulur.

Bu ağırlıklar giriş feature map'i ile çarpılarak önemli feature channel'larının güçlendirilmesi ve daha az önemli channel'ların baskılanması amaçlanır.

---

## Spatial Attention

Spatial Attention'ın amacı, channel attention sonrasında görüntünün hangi uzamsal bölgelerinin daha önemli olduğunu öğrenmektir.

Channel attention çıktısı üzerinde channel ekseninde:

- Average projection
- Maximum projection

hesaplanmaktadır.

Her iki temsil:

```text
[B, 1, 14, 14]
```

boyutundadır.

Bu temsiller concatenate edilerek:

```text
[B, 2, 14, 14]
```

tensoru oluşturulur.

Ardından:

```text
Kernel size = 7 × 7
Padding     = 3
```

olan bir convolution işlemi uygulanır.

Sigmoid aktivasyonu sonucunda:

```text
[B, 1, 14, 14]
```

boyutunda spatial attention maskesi elde edilir.

Bu maske feature map ile çarpılarak uzamsal bölgelerin adaptif biçimde ağırlıklandırılması sağlanır.

---

## VGG16 Entegrasyon Noktası

CBAM'ın VGG16 feature extractor'ın son convolutional bloğundan sonra ve final MaxPool katmanından önce uygulanmasına karar verilmiştir.

224 × 224 giriş görüntüsü için ilgili feature map:

```text
[B, 512, 14, 14]
```

boyutundadır.

Genel mimari:

```text
Input Image
224 × 224
     │
     ▼
Pretrained VGG16
Convolutional Feature Extractor
     │
     ▼
512 × 14 × 14
     │
     ▼
CBAM
 ├─ Channel Attention
 └─ Spatial Attention
     │
     ▼
512 × 14 × 14
     │
     ▼
Final VGG16 MaxPool
     │
     ▼
512 × 7 × 7
     │
     ▼
Adaptive Average Pool
     │
     ▼
Flatten
     │
     ▼
Regression Head
     │
     ▼
Visibility Prediction
(metres)
```

CBAM'ın final MaxPool öncesinde konumlandırılmasıyla Spatial Attention'ın 7 × 7 yerine **14 × 14 çözünürlüklü feature map** üzerinde çalışması sağlanmaktadır.

---

## Regression Head

Attention deneyinde baseline karşılaştırmasının mümkün olduğunca kontrollü tutulması amacıyla VGG16 baseline modelindeki regression head korunmuştur.

Yapı:

```text
25088
  │
  ▼
512
  │
ReLU
  │
Dropout (0.30)
  │
  ▼
128
  │
ReLU
  │
Dropout (0.30)
  │
  ▼
1
```

Son katman tek bir sürekli değer üretmektedir.

Bu değer tahmin edilen görüş mesafesini metre cinsinden temsil etmektedir.

Regression head'in değiştirilmemesi sayesinde attention deneyindeki temel mimari değişken CBAM entegrasyonu olarak sınırlandırılmıştır.

---

## Transfer Learning Stratejisi

Baseline VGG16 deneyinde kullanılan transfer learning yaklaşımı Attention modelinde de korunmaktadır.

Pretrained VGG16 feature extractor:

```text
FROZEN
```

durumundadır.

Yeni eklenen CBAM:

```text
TRAINABLE
```

durumundadır.

Regression head:

```text
TRAINABLE
```

durumundadır.

Gerçekleştirilen parametre kontrolünde aşağıdaki değerler doğrulanmıştır:

| Parametre Grubu | Sayı |
| --- | ---: |
| Total Parameters | 27,658,915 |
| Frozen Parameters | 14,714,688 |
| Trainable Parameters | 12,944,227 |
| CBAM Trainable Parameters | 32,866 |
| Regression Head Trainable Parameters | 12,911,361 |

Ayrıca:

```text
32,866 + 12,911,361 = 12,944,227
```

olduğu doğrulanmıştır.

Bu sonuç, trainable parametrelerin yalnızca CBAM ve regression head içerisinde bulunduğunu göstermektedir.

---

## Teknik Doğrulamalar

CBAM ve Attention-enhanced VGG16 mimarisi üzerinde ilk yapısal testler gerçekleştirilmiştir.

### CBAM Shape Test

```text
Input  : [2, 512, 14, 14]
Output : [2, 512, 14, 14]
```

CBAM'ın feature map boyutlarını koruduğu doğrulanmıştır.

### Model Forward Pass Test

```text
Input  : [2, 3, 224, 224]
Output : [2, 1]
```

Attention-enhanced VGG16 modelinin beklenen regresyon çıktısını başarıyla ürettiği doğrulanmıştır.

### Parameter Freeze Test

```text
Feature extractor trainable : False
CBAM trainable              : True
Regression head trainable   : True
```

Sonuçları elde edilmiştir.

Böylece transfer learning ve attention eğitim stratejisinin kod seviyesinde doğru yapılandırıldığı doğrulanmıştır.

---

## Oluşturulan Model Dosyaları

Attention mimarisi modüler biçimde geliştirilmiştir.

```text
src/models/attention.py
src/models/vgg16_attention.py
```

`attention.py` içerisinde:

- `ChannelAttention`
- `SpatialAttention`
- `CBAM`

modülleri bulunmaktadır.

`vgg16_attention.py` içerisinde ise CBAM ile genişletilmiş VGG16 regresyon mimarisi tanımlanmıştır.

Bu ayrım attention mekanizmasının model eğitim kodundan bağımsız ve yeniden kullanılabilir biçimde tutulmasını sağlamaktadır.

---

## Deneysel Hipotez

Attention aşamasındaki deneysel beklenti, CBAM'ın VGG16 feature map'leri üzerinde channel ve spatial yeniden ağırlıklandırma uygulamasının görüş mesafesi regresyon performansını iyileştirebilmesidir.

Attention modelinin performansı öncelikle mevcut VGG16 baseline ile karşılaştırılacaktır.

Referans değer:

```text
VGG16 Baseline Test MAE = 66.7227 m
```

olarak belirlenmiştir.

Attention modelinin performans katkısı ancak eğitim ve bağımsız test değerlendirmesi tamamlandıktan sonra belirlenecektir.

Bu nedenle mevcut aşamada CBAM'ın model performansını artırdığına ilişkin bir sonuç çıkarılmamaktadır.

---

## Sonraki Adım

Mimari tasarım ve ilk yapısal doğrulamalar tamamlandıktan sonra Attention-enhanced VGG16 modeli mevcut training pipeline'a entegre edilecektir.

Model mümkün olduğunca baseline VGG16 ile aynı:

- veri kümesi,
- scene-based veri ayrımı,
- preprocessing,
- batch size,
- optimizer,
- learning rate,
- epoch sayısı,
- random seed,
- loss fonksiyonu

kullanılarak eğitilecektir.

Bu yaklaşım Attention Mechanism'ın model performansına etkisinin kontrollü biçimde değerlendirilmesini sağlayacaktır.