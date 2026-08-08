# VGG16 ve ResNet50 Baseline Karşılaştırması

## Amaç

Bu dokümanın amacı, FRIDA ve FRIDA2 veri setlerinden oluşturulan sentetik sürekli görüş mesafesi regresyon veri kümesi üzerinde geliştirilen VGG16 ve ResNet50 baseline modellerinin performanslarını karşılaştırmaktır.

Her iki model aynı scene-based eğitim, doğrulama ve test ayrımı ile ortak temel deney koşulları altında değerlendirilmiştir.

Bu karşılaştırmanın amacı, projenin nihai modelini doğrudan belirlemek değil; mevcut sentetik veri aşamasında en başarılı baseline mimarisini belirleyerek Attention Mechanism aşamasında kullanılacak temel modeli seçmektir.

Gerçek dünya performansı ve nihai genelleme başarısı, proje planındaki FVEI/FHVI veya uygun alternatif gerçek dünya verileriyle gerçekleştirilecek sonraki değerlendirme ve fine-tuning aşamalarında ayrıca incelenecektir.

---

## Deneysel Karşılaştırma Koşulları

VGG16 ve ResNet50 baseline modelleri, mimariler arasındaki karşılaştırmanın mümkün olduğunca kontrollü ve tekrarlanabilir olması amacıyla ortak temel deney koşulları altında değerlendirilmiştir.

Her iki model için:

- FRIDA ve FRIDA2 kaynaklı aynı sentetik veri kümesi kullanılmıştır.
- Toplam 672 görüntü kullanılmıştır.
- Aynı scene-based train/validation/test ayrımı korunmuştur.
- Training kümesinde 464 görüntü kullanılmıştır.
- Validation kümesinde 96 görüntü kullanılmıştır.
- Test kümesinde 112 görüntü kullanılmıştır.
- Giriş görüntüleri 224 × 224 piksel olarak hazırlanmıştır.
- ImageNet pretrained weights kullanılmıştır.
- Backbone katmanları dondurulmuştur.
- Batch size 16 olarak belirlenmiştir.
- Her model 20 epoch boyunca eğitilmiştir.
- Adam optimizer kullanılmıştır.
- Learning rate 1e-4 olarak belirlenmiştir.
- Weight decay 1e-5 olarak kullanılmıştır.
- L1Loss / MAE temel hata fonksiyonu olarak kullanılmıştır.
- Random seed 42 olarak sabitlenmiştir.
- Model checkpoint seçimi en düşük Validation MAE değerine göre yapılmıştır.
- Nihai baseline karşılaştırması bağımsız test kümesindeki MAE sonuçları üzerinden gerçekleştirilmiştir.

Bu ortak deneysel çerçeve, iki mimarinin mevcut sentetik veri aşamasındaki performanslarının karşılaştırılabilmesini sağlamaktadır.

---

## Genel Sonuç Tablosu

Evaluation çıktılarından doğrulanan sonuçlar aşağıdaki gibidir:

| Metrik | VGG16 | ResNet50 | Daha İyi Sonuç |
| --- | ---: | ---: | :---: |
| Best Checkpoint Epoch | 18 | 20 | — |
| Validation MAE | **69.9705 m** | 121.8414 m | **VGG16** |
| Test MAE | **66.7227 m** | 124.6181 m | **VGG16** |
| Mean Signed Error | **−17.3877 m** | −77.3460 m | **VGG16** |
| Minimum Absolute Error | 0.8415 m | **0.7323 m** | ResNet50 |
| Maximum Absolute Error | **392.8829 m** | 602.6687 m | **VGG16** |
| Test Samples | 112 | 112 | — |
| MAE < 100 m | **Evet** | Hayır | **VGG16** |

Minimum absolute error ResNet50 modelinde daha düşük olmasına rağmen bu değer yalnızca en başarılı tekil tahmini temsil etmektedir. Genel model performansının değerlendirilmesinde temel seçim kriteri bağımsız test kümesi üzerindeki MAE değeridir.

---

## Validation MAE Karşılaştırması

VGG16 baseline modeli en başarılı checkpoint'inde:

**69.9705 m Validation MAE**

elde etmiştir.

ResNet50 baseline modeli ise:

**121.8414 m Validation MAE**

elde etmiştir.

İki model arasındaki Validation MAE farkı:

```text
121.8414 − 69.9705 = 51.8709 m
```
olarak hesaplanmıştır.

Dolayısıyla mevcut sentetik validation kümesi üzerinde VGG16, ResNet50'ye göre belirgin biçimde daha düşük ortalama mutlak hata üretmiştir.

VGG16 ayrıca araştırma önerisinde belirlenen **MAE < 100 m** hedefini validation kümesinde karşılarken ResNet50 mevcut baseline konfigürasyonunda bu eşiğin üzerinde kalmıştır.

---

## Test MAE Karşılaştırması

Baseline model seçiminin temel performans kriteri bağımsız test kümesi üzerindeki MAE değeridir.

VGG16:

**66.7227 m Test MAE**

elde ederken ResNet50:

**124.6181 m Test MAE**

elde etmiştir.

İki model arasındaki mutlak Test MAE farkı:

```text
124.6181 − 66.7227 = 57.8954 m
```

olarak hesaplanmıştır.

ResNet50'nin Test MAE değeri VGG16'nın Test MAE değerinden yaklaşık **%86.77 daha yüksektir**.

Diğer yönden ifade edildiğinde VGG16 kullanımı, ResNet50 baseline sonucuna kıyasla Test MAE'de yaklaşık **%46.46 azalma** sağlamıştır.

Bu sonuç mevcut FRIDA/FRIDA2 kaynaklı sentetik veri kümesi üzerinde VGG16'nın bağımsız test performansının ResNet50'den daha başarılı olduğunu göstermektedir.

---

## Hata Davranışlarının Karşılaştırılması

Model performansı yalnızca MAE değerleri üzerinden değil, tahmin hatalarının yönü ve büyüklüğü açısından da değerlendirilmiştir.

VGG16 modelinin Mean Signed Error değeri:

**−17.3877 m**

iken ResNet50 modelinde:

**−77.3460 m**

olarak ölçülmüştür.

Her iki negatif değer de modellerin ortalama olarak gerçek görüş mesafesini olduğundan düşük tahmin etme eğilimi bulunduğunu göstermektedir.

Bununla birlikte bu eğilim ResNet50 modelinde belirgin biçimde daha güçlüdür.

Maximum Absolute Error değerleri:

- VGG16: **392.8829 m**
- ResNet50: **602.6687 m**

olarak ölçülmüştür.

ResNet50 değerlendirme grafiklerinde özellikle yüksek ground-truth görüş mesafelerinde sistematik underestimation ve prediction-range compression davranışı gözlenmiştir.

Bu nedenle ResNet50'nin daha yüksek Test MAE sonucu yalnızca birkaç tekil örnekten kaynaklanan bir fark olarak değerlendirilmemekte; genel hata dağılımı ve tahmin davranışlarıyla birlikte ele alınmaktadır.

---

## Hipotezin Değerlendirilmesi

Projenin başlangıç hipotezinde ResNet50 mimarisinin residual learning yapısı ve daha derin özellik çıkarım kapasitesi nedeniyle VGG16'ya kıyasla daha düşük MAE değerleri üretmesi beklenmiştir.

Bu hipotez doğrultusunda iki mimari mümkün olduğunca ortak deney koşulları altında eğitilmiş ve bağımsız test kümesi üzerinde değerlendirilmiştir.

Ancak mevcut FRIDA/FRIDA2 kaynaklı sentetik veri kümesi üzerinde elde edilen deneysel sonuçlar başlangıç hipotezini desteklememiştir.

Elde edilen temel sonuçlar:

| Model | Validation MAE | Test MAE |
| --- | ---: | ---: |
| VGG16 | **69.9705 m** | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

şeklindedir.

ResNet50'nin daha modern ve residual bağlantılara sahip daha derin bir mimari olması, mevcut deney koşullarında otomatik olarak daha düşük regresyon hatasına dönüşmemiştir.

Bu sonuç, mimari karmaşıklığın tek başına görüş mesafesi regresyon performansını belirlemediğini göstermektedir.

Bununla birlikte mevcut deneylerden ResNet50'nin daha düşük performans göstermesinin kesin nedeni belirlenemez.

Olası açıklamalar arasında:

- kullanılan sentetik veri kümesinin büyüklüğü ve yapısı,
- backbone katmanlarının tamamen dondurulmuş olması,
- yalnızca yeni regresyon başlığının eğitilmesi,
- 20 epoch ile sınırlandırılmış ortak eğitim bütçesi,
- VGG16 ve ResNet50'nin pretrained feature temsillerinin bu regresyon görevine farklı düzeylerde uygun olması

bulunabilir.

Bu faktörler mevcut sonuçların olası açıklamalarıdır ve ayrıca kontrollü deneylerle doğrulanmadıkları sürece kesin neden olarak kabul edilmeyecektir.

Dolayısıyla araştırma hipotezi, mevcut sentetik baseline deneyleri kapsamında desteklenmemiştir.

Bu sonuç, iki mimarinin aynı problem üzerindeki performansının deneysel olarak ölçülmesi sonucunda başlangıç beklentisinden farklı bir bulgu elde edildiğini göstermektedir.

---

## Sentetik Baseline Model Seçimi

Proje yönteminde baseline model seçiminin temel kriteri bağımsız test kümesi üzerinde elde edilen MAE değeridir.

Mevcut sonuçlarda:

```text
VGG16 Test MAE    = 66.7227 m
ResNet50 Test MAE = 124.6181 m
```

olarak ölçülmüştür.

VGG16, ResNet50'ye kıyasla **57.8954 m daha düşük Test MAE** elde etmiştir.

Ayrıca VGG16:

- daha düşük Validation MAE,
- daha düşük Test MAE,
- sıfıra daha yakın Mean Signed Error,
- daha düşük Maximum Absolute Error

elde etmiştir.

Bu nedenle **FRIDA ve FRIDA2 kaynaklı mevcut sentetik veri aşamasında en başarılı baseline mimarisi VGG16 olarak seçilmiştir.**

Bu seçim VGG16'nın genel olarak ResNet50'den daha üstün bir CNN mimarisi olduğu anlamına gelmemektedir.

Karar yalnızca bu projede kullanılan:

- sentetik veri kümesi,
- scene-based veri ayrımı,
- transfer learning konfigürasyonu,
- frozen backbone yaklaşımı,
- eğitim parametreleri,
- bağımsız test sonuçları

altında elde edilen deneysel bulgulara dayanmaktadır.

---

## Attention Mechanism Aşamasına Geçiş

Mevcut sentetik baseline karşılaştırması sonucunda VGG16, Attention Mechanism entegrasyonu için temel mimari olarak seçilmiştir.

Bir sonraki aşamada seçilen VGG16 baseline mimarisine Attention Mechanism entegre edilecek ve yeni model aynı temel deneysel prosedür altında eğitilip değerlendirilecektir.

Attention modelinin performansı öncelikle mevcut VGG16 baseline sonucu olan:

**66.7227 m Test MAE**

ile karşılaştırılacaktır.

Bu karşılaştırma Attention Mechanism'ın mevcut sentetik görüş mesafesi regresyon problemine sağladığı katkının ölçülmesini sağlayacaktır.

---

## Gerçek Dünya Verileri Açısından Kararın Kapsamı

Day 15 kapsamında yapılan model seçimi projenin nihai gerçek dünya model seçimi olarak değerlendirilmemektedir.

Şu ana kadar gerçekleştirilen VGG16 ve ResNet50 baseline deneyleri FRIDA ve FRIDA2 kaynaklı sentetik görüntülerden oluşturulan veri kümesi üzerinde gerçekleştirilmiştir.

Proje planının sonraki aşamalarında FVEI, FHVI veya problem tanımına uygun erişilebilir alternatif gerçek dünya verilerinin değerlendirilmesi planlanmaktadır.

Uygun gerçek dünya verisine erişilmesi durumunda seçilen model üzerinde fine-tuning ve gerçek dünya performans analizi gerçekleştirilecektir.

Sentetik veri üzerinde elde edilen model sıralamasının gerçek dünya verilerinde aynı şekilde korunacağı önceden varsayılmayacaktır.

Dolayısıyla VGG16 için Day 15'te alınan kararın doğru ifadesi:

> **VGG16, mevcut FRIDA/FRIDA2 kaynaklı sentetik deneylerde Attention Mechanism aşamasına aktarılacak en başarılı baseline mimarisi olarak seçilmiştir.**

şeklindedir.

Nihai model performansı, Attention Mechanism ve mümkün olması hâlinde gerçek dünya değerlendirme/fine-tuning aşamalarının tamamlanmasının ardından ayrıca raporlanacaktır.

---

## Day 15 Sonucu

Day 15 kapsamında VGG16 ve ResNet50 baseline modellerinin karşılaştırmalı analizi tamamlanmıştır.

Gerçekleştirilen çalışmalar:

- VGG16 ve ResNet50 evaluation sonuçları doğrudan deney çıktı dosyalarından doğrulandı.
- Validation MAE değerleri karşılaştırıldı.
- Test MAE değerleri karşılaştırıldı.
- Mean Signed Error değerleri incelendi.
- Minimum ve Maximum Absolute Error değerleri karşılaştırıldı.
- Model hata davranışları değerlendirildi.
- Başlangıç araştırma hipotezi deneysel sonuçlar ışığında değerlendirildi.
- Sentetik veri aşamasındaki en başarılı baseline model belirlendi.
- Attention Mechanism aşamasında kullanılacak temel mimari seçildi.

### Nihai Day 15 Kararı

**Selected Synthetic Baseline: VGG16**

**Baseline Test MAE: 66.7227 m**

**ResNet50 Test MAE: 124.6181 m**

**Test MAE Difference: 57.8954 m**

**VGG16 Test MAE Reduction Relative to ResNet50: 46.46%**

Başlangıçta ResNet50'nin daha düşük MAE üretmesi beklenmiş olmasına rağmen mevcut deneysel sonuçlar bu hipotezi desteklememiştir.

VGG16, mevcut sentetik veri aşamasında daha düşük bağımsız test hatası elde ettiği için Attention Mechanism aşamasına aktarılacak baseline mimarisi olarak seçilmiştir.