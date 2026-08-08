# Yöntem Özeti

## Aşama 1 — Veri Seti Analizi ve Hazırlığı

Proje kapsamında öncelikle FRIDA ve FRIDA2 sentetik veri setleri ayrıntılı olarak analiz edilmiştir.

Her iki veri setindeki açık hava görüntüleri, derinlik haritaları ve klasör yapıları incelenmiş; model eğitiminde kullanılacak temel sahneler doğrulanmıştır.

FRIDA veri setinden **18**, FRIDA2 veri setinden **66** temel sahne olmak üzere toplam **84 sahne** belirlenmiştir.

FRIDA ve FRIDA2 veri setlerinde proje kapsamında doğrudan kullanılabilecek metre cinsinden sürekli görüş mesafesi etiketleri bulunmadığından, araştırma önerisinde planlanan yöntem doğrultusunda yeni regresyon verileri oluşturulmuştur.

Atmosferik saçılım modeli uygulanarak her temel sahne için aşağıdaki görüş mesafelerini temsil eden sentetik görüntüler üretilmiştir:

- 50 m
- 80 m
- 100 m
- 150 m
- 200 m
- 300 m
- 500 m
- 800 m

Bu süreç sonunda:

```text
84 sahne × 8 görüş mesafesi = 672 görüntü
```

olmak üzere toplam **672 sentetik görüntüden** oluşan veri kümesi hazırlanmıştır.

Üretilen görüntülere ait metadata ve regresyon hedefleri `labels.csv` dosyasında saklanmıştır.

Sentetik veri üretiminden sonra veri bütünlüğü doğrulanmış; eksik görüntü, hatalı dosya yolu ve tutarsız etiket kontrolleri gerçekleştirilmiştir.

---

## Aşama 2 — Veri Ön İşleme ve Veri Yükleme

Üretilen veri kümesi transfer öğrenme tabanlı CNN modellerinde kullanılabilecek biçime dönüştürülmüştür.

Bu kapsamda görüntüler:

- RGB formatına dönüştürülmüş,
- **224 × 224** piksel giriş boyutuna hazırlanmış,
- ImageNet pretrained modelleriyle uyumlu normalizasyon işleminden geçirilmiştir.

Model eğitiminde kullanılmak üzere PyTorch tabanlı özel bir `FogVisibilityDataset` sınıfı geliştirilmiştir.

Verilerin mini-batch yapısında modele aktarılması amacıyla `DataLoader` altyapısı oluşturulmuştur.

Baseline deneylerinde kullanılan temel veri yükleme ayarları:

- Image Size: **224 × 224**
- Batch Size: **16**
- Number of Workers: **0**
- Random Seed: **42**

olarak belirlenmiştir.

Aynı preprocessing ve veri yükleme pipeline'ı hem VGG16 hem de ResNet50 baseline deneylerinde kullanılmış ve başarıyla doğrulanmıştır.

Bu ortak altyapı Attention Mechanism aşamasında da kullanılacaktır.

---

## Aşama 3 — Eğitim, Doğrulama ve Test Veri Ayrımı

Hazırlanan veri kümesi eğitim, doğrulama ve test olmak üzere üç bağımsız alt kümeye ayrılmıştır.

Veri sızıntısını önlemek amacıyla rastgele görüntü bazlı split yerine **scene-based split** yaklaşımı kullanılmıştır.

Aynı temel sahneye ait tüm görüş mesafesi varyasyonları aynı veri alt kümesinde tutulmuştur.

Bu sayede modelin test aşamasında training sırasında gördüğü aynı temel sahnenin farklı bir varyasyonuyla karşılaşması engellenmiştir.

Elde edilen veri dağılımı:

| Veri Kümesi | Görüntü Sayısı |
| --- | ---: |
| Training | **464** |
| Validation | **96** |
| Test | **112** |
| **Toplam** | **672** |

şeklindedir.

Hedeflenen oranlar yaklaşık olarak:

- Training: %70
- Validation: %15
- Test: %15

olarak belirlenmiştir.

Aynı scene-based split hem VGG16 hem de ResNet50 deneylerinde korunmuştur.

Deneylerin tekrarlanabilirliğini desteklemek amacıyla tüm veri bölme işlemlerinde:

```text
random_seed = 42
```

kullanılmıştır.

---

## Aşama 4 — Transfer Öğrenme ile Baseline Model Adaptasyonu

Proje kapsamında VGG16 ve ResNet50 mimarileri ImageNet üzerinde önceden eğitilmiş ağırlıklarla görüş mesafesi regresyon problemine adapte edilmiştir.

Her iki baseline deneyinde ortak yaklaşım olarak:

- ImageNet pretrained weights kullanılmış,
- backbone katmanları dondurulmuş,
- orijinal classification head kaldırılmış,
- tek bir sürekli görüş mesafesi değeri üreten regression head eklenmiş,
- aynı scene-based split kullanılmış,
- aynı temel eğitim parametreleri korunmuştur.

Deney parametreleri merkezi `config.py` dosyasında yönetilmiştir.

Ortak baseline eğitim ayarları:

- Image Size: **224 × 224**
- Batch Size: **16**
- Epoch: **20**
- Optimizer: **Adam**
- Learning Rate: **1e-4**
- Weight Decay: **1e-5**
- Loss Function: **L1Loss / MAE**
- Random Seed: **42**
- Frozen Backbone: **True**

olarak belirlenmiştir.

Her epoch sonunda Training MAE ve Validation MAE hesaplanmış, en düşük Validation MAE değerine sahip model otomatik olarak checkpoint olarak kaydedilmiştir.

Deney sonuçları ayrıca:

- `experiment_log.xlsx`
- model eğitim logları
- learning curve grafikleri

üzerinden kaydedilmiştir.

---

### VGG16 Baseline Modeli

İlk baseline model olarak ImageNet pretrained VGG16 mimarisi kullanılmıştır.

VGG16'nın backbone katmanları dondurulmuş ve orijinal classification head sürekli görüş mesafesi tahmini gerçekleştiren regresyon yapısına dönüştürülmüştür.

Model toplam **20 epoch** boyunca eğitilmiştir.

Eğitim sonucunda:

- En iyi epoch: **18**
- Best Validation MAE: **69.9705 m**

elde edilmiştir.

Bu sonuç araştırma önerisinde belirlenen:

**MAE < 100 metre**

performans hedefini başarıyla karşılamıştır.

---

### VGG16 Model Evaluation

VGG16 için kaydedilen en iyi checkpoint bağımsız test veri kümesi üzerinde değerlendirilmiştir.

Evaluation pipeline kapsamında:

- checkpoint yükleme,
- test tahminlerinin oluşturulması,
- Test MAE hesaplanması,
- prediction CSV oluşturulması,
- evaluation JSON oluşturulması,
- Actual vs Predicted grafiği,
- Prediction Error Histogram,
- otomatik Markdown evaluation raporu

üretilmiştir.

VGG16 bağımsız test sonuçları:

| Metrik | Sonuç |
| --- | ---: |
| Test Samples | **112** |
| Test MAE | **66.7227 m** |
| Validation MAE | **69.9705 m** |
| Mean Signed Error | **−17.3877 m** |

şeklindedir.

Validation ve Test MAE değerlerinin birbirine yakın olması modelin bağımsız test sahnelerinde benzer performans gösterdiğini ortaya koymuştur.

---

### ResNet50 Baseline Modeli

İkinci baseline model olarak ImageNet pretrained ResNet50 mimarisi geliştirilmiştir.

ResNet50'nin backbone katmanları dondurulmuş ve orijinal `fc` classification katmanı kaldırılarak sürekli görüş mesafesi tahmini yapan yeni bir regression head eklenmiştir.

Kullanılan regresyon başlığı temel olarak:

```text
2048
 ↓
512
 ↓
ReLU
 ↓
Dropout
 ↓
128
 ↓
ReLU
 ↓
Dropout
 ↓
1
```

yapısındadır.

ResNet50 modeli VGG16 ile aynı temel deney koşulları altında toplam **20 epoch** boyunca eğitilmiştir.

Eğitim sonucunda:

- En iyi epoch: **20**
- Final Training MAE: **122.1239 m**
- Best Validation MAE: **121.8414 m**

elde edilmiştir.

ResNet50 modeli mevcut baseline konfigürasyonunda araştırma önerisindeki **MAE < 100 metre** hedefini karşılayamamıştır.

---

### ResNet50 Model Evaluation

ResNet50'nin en başarılı checkpoint'i bağımsız test veri kümesi üzerinde değerlendirilmiştir.

Evaluation pipeline VGG16 ile aynı prosedürü kullanacak şekilde geliştirilmiştir.

Elde edilen sonuçlar:

| Metrik | Sonuç |
| --- | ---: |
| Test Samples | **112** |
| Test MAE | **124.6181 m** |
| Validation MAE | **121.8414 m** |
| Mean Signed Error | **−77.3460 m** |
| Maximum Absolute Error | **602.6687 m** |

şeklindedir.

Validation MAE ile Test MAE arasındaki fark:

**2.7767 m**

olarak hesaplanmıştır.

Bu yakınlık, mevcut deneyde belirgin bir validation-test performans çöküşü olmadığını göstermektedir.

---

## Aşama 5 — Baseline Modellerin Davranışsal Analizi

ResNet50 baseline modelinin performansı yalnızca toplam MAE metriği üzerinden değil, learning curve ve evaluation grafikleri üzerinden de incelenmiştir.

### Learning Curve Analizi

Training ve Validation MAE değerleri 20 epoch boyunca düzenli biçimde azalmıştır.

Training MAE:

**271.6411 m → 122.1239 m**

Validation MAE:

**269.8412 m → 121.8414 m**

seviyesine düşmüştür.

Training ve validation eğrileri özellikle eğitimin ilerleyen aşamalarında birbirine oldukça yakın ilerlemiştir.

20. epoch sonunda Training ve Validation MAE arasındaki fark yaklaşık **0.28 m** seviyesindedir.

Bu nedenle mevcut baseline konfigürasyonunda belirgin bir klasik overfitting davranışı gözlenmemiştir.

En iyi Validation MAE değerinin son epoch'ta elde edilmesi, modelin 20 epoch sonunda tamamen yakınsamamış olabileceğini düşündürmektedir.

Ancak VGG16 ve ResNet50 baseline deneylerinin aynı eğitim bütçesi altında karşılaştırılması amacıyla ResNet50 bu aşamada daha uzun süre yeniden eğitilmemiştir.

---

### Actual vs Predicted Analizi

ResNet50'nin Actual vs Predicted grafiğinde düşük ve orta görüş mesafelerinde tahminlerin ground-truth değerlere görece daha yakın olduğu görülmüştür.

Bununla birlikte özellikle **500 m** ve **800 m** ground-truth değerlerinde tahminlerin sistematik biçimde gerçek değerlerin altında kaldığı gözlemlenmiştir.

800 m ground-truth değerine sahip örneklerde model tahminlerinin yaklaşık **200–360 m** bandında yoğunlaştığı görülmüştür.

Bu davranış yüksek görüş mesafelerinde sistematik **underestimation** olarak değerlendirilmiştir.

Ayrıca ground-truth hedefleri yaklaşık **50–800 m** aralığında değişmesine rağmen model tahminlerinin daha dar bir aralıkta kalması **prediction-range compression** davranışı olarak kaydedilmiştir.

---

### Prediction Error Histogram Analizi

Tahmin hatası:

```text
Prediction Error = Prediction - Ground Truth
```

şeklinde tanımlanmıştır.

Histogram incelendiğinde test örneklerinin önemli bir bölümünün sıfıra yakın hata bölgelerinde toplandığı, ancak negatif yönde uzun bir hata kuyruğu bulunduğu görülmüştür.

Bazı negatif hatalar yaklaşık **−600 m** seviyesine ulaşmıştır.

Bu asimetrik hata dağılımı:

- Mean Signed Error: **−77.3460 m**
- Maximum Absolute Error: **602.6687 m**

sonuçlarıyla uyumludur.

Bu nedenle ResNet50'nin temel sınırlılığı mevcut deneysel gözlemlere göre klasik overfitting değil, özellikle yüksek görüş mesafelerinde oluşan sistematik underestimation ve prediction-range compression davranışıdır.

Bu davranışın kesin nedeni mevcut deneylerden belirlenmemiştir.

Hedef dağılımı, model mimarisi, frozen backbone veya eğitim süresi gibi faktörler yalnızca olası hipotezler olarak değerlendirilmektedir.

---

## Aşama 6 — VGG16 ve ResNet50 Karşılaştırması

Her iki baseline model aynı temel deneysel koşullar altında geliştirilmiş ve aynı bağımsız test veri kümesi üzerinde değerlendirilmiştir.

Mevcut temel sonuçlar:

| Metrik | VGG16 | ResNet50 |
| --- | ---: | ---: |
| Best Epoch | **18** | **20** |
| Best Validation MAE | **69.9705 m** | **121.8414 m** |
| Test MAE | **66.7227 m** | **124.6181 m** |
| Mean Signed Error | **−17.3877 m** | **−77.3460 m** |
| MAE < 100 m | **Evet** | **Hayır** |

Mevcut bağımsız test sonuçlarına göre VGG16, ResNet50'den daha düşük MAE üretmiştir.

Test MAE farkı:

**124.6181 − 66.7227 = 57.8954 m**

olarak hesaplanmaktadır.

Bu nedenle Day 14 itibarıyla VGG16 mevcut deneysel sonuçlarda daha güçlü baseline adayıdır.

Nihai baseline seçimi karşılaştırmalı analiz aşamasının tamamlanmasıyla resmi olarak dokümante edilecektir.

---

## Aşama 7 — Attention Mechanism Entegrasyonu

Baseline karşılaştırmasının tamamlanmasının ardından bağımsız test MAE açısından en başarılı model Attention Mechanism aşamasının temel mimarisi olarak seçilecektir.

Attention Mechanism'ın amacı modelin görüş mesafesi tahmini açısından önemli uzamsal bölgelere ve özelliklere daha fazla ağırlık vermesini sağlamaktır.

Attention entegrasyonu sonrasında model aynı temel deneysel prosedür kullanılarak yeniden:

- eğitilecek,
- validation performansı takip edilecek,
- bağımsız test kümesinde değerlendirilecek,
- prediction ve error grafikleri oluşturulacaktır.

Attention modelinin başarısı seçilen baseline modelin Test MAE değeriyle karşılaştırılacaktır.

Temel karşılaştırma:

```text
Selected Baseline Test MAE
            vs
Attention Model Test MAE
```

şeklinde gerçekleştirilecektir.

Attention Mechanism'ın model performansına etkisi elde edilen deneysel sonuçlar üzerinden raporlanacaktır.

---

## Aşama 8 — Gerçek Dünya Değerlendirmesi

Gerçek dünya veri setlerine erişim sağlanması ve etiket yapılarının proje problemine uygun olması durumunda FVEI ve/veya FHVI veri setleri değerlendirilecektir.

Bu aşamanın amaçları:

- sentetik veri üzerinde geliştirilen modelin gerçek görüntülerde davranışını incelemek,
- sentetik-gerçek domain farkını değerlendirmek,
- uygun veri bulunması hâlinde fine-tuning gerçekleştirmek,
- gerçek dünya genelleme performansını analiz etmek

olarak belirlenmiştir.

FVEI, sürekli görüş mesafesi regresyonuna daha uygun bir gerçek dünya veri kaynağı olarak değerlendirilirken FHVI daha çok ek doğrulama veri seti adayı olarak ele alınmaktadır.

Gerçek dünya veri aşaması erişilebilirlik ve veri uygunluğu koşullarına bağlı olarak uygulanacaktır.

---

## Aşama 9 — Web Tabanlı Prototip

Projenin deneysel model geliştirme aşaması tamamlandıktan sonra seçilen nihai model Flask tabanlı web uygulamasına entegre edilecektir.

HTML ve CSS kullanılarak basit ve fonksiyonel bir kullanıcı arayüzü geliştirilecektir.

Planlanan çalışma akışı:

```text
Kullanıcı Görüntü Yükler
          │
          ▼
Preprocessing Pipeline
          │
          ▼
Nihai Model
          │
          ▼
Görüş Mesafesi Tahmini
          │
          ▼
Flask API
          │
          ▼
Web Arayüzünde Sonuç
```

Kullanıcı sisteme yol görüntüsü yükleyebilecek ve model ilgili görüntü için metre cinsinden görüş mesafesi tahmini gerçekleştirecektir.

Bu prototip, geliştirilen modelin Akıllı Ulaşım Sistemleri benzeri bir yazılım altyapısına entegrasyonunun temel bir gösterimini sağlayacaktır.

---

# Güncel Yöntem Durumu — Day 14

Day 14 itibarıyla:

- ✓ FRIDA ve FRIDA2 veri analizi tamamlandı.
- ✓ Sentetik veri üretimi tamamlandı.
- ✓ 672 görüntülük regresyon veri kümesi oluşturuldu.
- ✓ Veri bütünlüğü doğrulandı.
- ✓ Scene-based split tamamlandı.
- ✓ Preprocessing pipeline tamamlandı.
- ✓ PyTorch Dataset ve DataLoader geliştirildi.
- ✓ VGG16 baseline modeli geliştirildi.
- ✓ VGG16 eğitimi tamamlandı.
- ✓ VGG16 bağımsız test değerlendirmesi tamamlandı.
- ✓ ResNet50 baseline modeli geliştirildi.
- ✓ ResNet50 eğitimi tamamlandı.
- ✓ ResNet50 bağımsız test değerlendirmesi tamamlandı.
- ✓ ResNet50 learning curve analizi gerçekleştirildi.
- ✓ Overfitting analizi tamamlandı.
- ✓ Actual vs Predicted analizi tamamlandı.
- ✓ Prediction Error Histogram analizi tamamlandı.
- ✓ ResNet50 underestimation ve prediction-range compression davranışları dokümante edildi.
- ⏳ VGG16–ResNet50 karşılaştırmalı analizinin resmi olarak tamamlanması.
- ⏳ Nihai baseline modelin seçilmesi.
- ⏳ Attention Mechanism entegrasyonu.
- ⏳ Attention modelinin eğitilmesi ve değerlendirilmesi.
- ⏳ Gerçek dünya veri aşamasının kesinleştirilmesi.
- ⏳ Flask tabanlı prototipin geliştirilmesi.