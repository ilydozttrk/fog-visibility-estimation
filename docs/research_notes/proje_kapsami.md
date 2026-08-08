# Proje Kapsamı

## Proje Başlığı

**Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi**

---

## Araştırma Problemi

Kötü hava koşullarına bağlı düşük görüş mesafesi, karayolları trafiğinde önemli bir kaza riski oluşturmaktadır. Mevcut güvenlik sistemlerinde kullanılan sensör tabanlı yöntemler, yüksek maliyetleri ve sınırlı kapsama alanları nedeniyle yaygın entegrasyonda zorluk oluşturabilmektedir.

Bu proje, mevcut yol gözetleme kameralarının kullanılabileceği görüntü tabanlı bir yapay zekâ yaklaşımıyla daha düşük maliyetli görüş mesafesi tahmini yapılabilirliğini araştırmaktadır.

---

## Araştırma Sorusu

Transfer öğrenme yöntemi ile görüntü tabanlı görüş mesafesi tahmini görevine adapte edilen VGG16 ve ResNet50 mimarilerinden hangisi, sentetik ve uygun gerçek dünya veri kümelerinde daha düşük MAE değeri sunarak Akıllı Ulaşım Sistemleri entegrasyonu için daha uygun bir temel oluşturur?

---

## Hipotez

ResNet50 mimarisinin, residual bağlantıları sayesinde transfer öğrenme ile adapte edildiğinde, aynı veri seti ve eğitim parametreleri altında VGG16 mimarisine kıyasla istatistiksel olarak anlamlı düzeyde daha düşük MAE değerleri üretmesi beklenmektedir.

Bu hipotez proje başlangıcında tanımlanmış olup elde edilen deneysel sonuçlar doğrultusunda değerlendirilecektir.

---

## Projenin Temel Amacı

Sisli hava koşullarında yol güvenliğini artırmak amacıyla, transfer öğrenme yöntemi kullanılarak önceden eğitilmiş VGG16 ve ResNet50 CNN modellerini karşılaştırmalı olarak analiz etmek, görüntü tabanlı sürekli görüş mesafesi tahmini gerçekleştirmek ve Flask API ile Akıllı Ulaşım Sistemleri entegrasyonuna uygun fonksiyonel bir prototip geliştirmektir.

---

## Temel Performans Metriği

Projenin temel performans metriği:

**Mean Absolute Error (MAE)**

olarak belirlenmiştir.

MAE değeri, metre cinsinden tahmin edilen görüş mesafesi ile ground-truth görüş mesafesi arasındaki ortalama mutlak farkı ölçmektedir.

Araştırma önerisinde belirlenen temel başarı kriteri:

**MAE < 100 metre**

şeklindedir.

Mevcut baseline sonuçlarına göre:

| Model | Best Validation MAE | Test MAE | Hedef |
| --- | ---: | ---: | --- |
| VGG16 | **69.9705 m** | **66.7227 m** | ✓ MAE < 100 m |
| ResNet50 | **121.8414 m** | **124.6181 m** | ✗ MAE < 100 m |

Bu aşamada VGG16 baseline modeli proje performans hedefini karşılamış, ResNet50 baseline modeli ise aynı hedefi karşılayamamıştır.

---

## Kullanılan ve Planlanan Veri Setleri

Proje kapsamında aşağıdaki veri kaynakları değerlendirilmiştir:

- FRIDA
- FRIDA2
- FVEI
- FHVI

### Sentetik Veri

FRIDA ve FRIDA2 veri setleri temel alınarak farklı görüş mesafelerini temsil eden sentetik görüntülerden oluşan çalışma veri kümesi hazırlanmıştır.

Mevcut sentetik veri kümesi:

- **84 temel sahne**
- **672 görüntü**

içermektedir.

Hazırlanan veri kümesi scene-based split yaklaşımıyla training, validation ve test kümelerine ayrılmıştır.

Aynı temel sahneye ait tüm görüş mesafesi varyasyonlarının aynı veri alt kümesinde tutulması sağlanarak veri sızıntısı riski azaltılmıştır.

Mevcut veri dağılımı:

| Veri Kümesi | Görüntü Sayısı |
| --- | ---: |
| Training | **464** |
| Validation | **96** |
| Test | **112** |
| **Toplam** | **672** |

şeklindedir.

Aynı veri bölünmesi VGG16 ve ResNet50 baseline deneylerinde korunmuştur.

### Gerçek Dünya Verileri

FVEI ve FHVI gibi gerçek dünya veri setlerinin erişilebilirliği ve proje problemine uygunluğu araştırılmaktadır.

Uygun ve erişilebilir gerçek dünya verileri elde edilmesi durumunda bunlar modelin gerçek dünya koşullarındaki davranışını incelemek, gerektiğinde fine-tuning gerçekleştirmek ve sentetik-gerçek veri arasındaki domain farkını değerlendirmek amacıyla kullanılacaktır.

Gerçek dünya verilerinin kullanımı veri erişilebilirliği, etiket yapısı ve araştırma önerisinin kapsamı doğrultusunda gerçekleştirilecektir.

---

# Karşılaştırılan Baseline Modeller

## VGG16 — Tamamlandı

ImageNet üzerinde önceden eğitilmiş VGG16 mimarisi ilk baseline model olarak kullanılmıştır.

Modelin convolutional backbone katmanları baseline deneyinde dondurulmuş ve orijinal sınıflandırma başlığı sürekli görüş mesafesi tahmini gerçekleştiren regresyon başlığı ile değiştirilmiştir.

Temel eğitim ayarları:

- Pretrained weights: **ImageNet**
- Frozen backbone: **True**
- Image size: **224 × 224**
- Batch size: **16**
- Epoch: **20**
- Optimizer: **Adam**
- Learning rate: **1e-4**
- Weight decay: **1e-5**
- Loss function: **L1Loss / MAE**
- Random seed: **42**

Eğitim sonucunda:

- En iyi epoch: **18**
- Best Validation MAE: **69.9705 m**

elde edilmiştir.

En başarılı checkpoint bağımsız test kümesi üzerinde değerlendirilmiş ve:

- Test MAE: **66.7227 m**
- Mean Signed Error: **−17.3877 m**

sonuçları elde edilmiştir.

VGG16 baseline modeli araştırma önerisinde tanımlanan **MAE < 100 metre** hedefini başarıyla karşılamıştır.

Model için eğitim, checkpoint, deney kayıt ve bağımsız evaluation pipeline'ları tamamlanmıştır.

---

## ResNet50 — Tamamlandı

İkinci baseline model olarak ImageNet üzerinde önceden eğitilmiş ResNet50 mimarisi kullanılmıştır.

ResNet50'nin convolutional backbone katmanları baseline deneyinde dondurulmuş ve sınıflandırma başlığı sürekli görüş mesafesi tahmini gerçekleştiren regresyon başlığı ile değiştirilmiştir.

Model VGG16 ile karşılaştırılabilir deneysel koşullar altında eğitilmiştir.

Temel eğitim ayarları:

- Pretrained weights: **ImageNet**
- Frozen backbone: **True**
- Image size: **224 × 224**
- Batch size: **16**
- Epoch: **20**
- Optimizer: **Adam**
- Learning rate: **1e-4**
- Weight decay: **1e-5**
- Loss function: **L1Loss / MAE**
- Random seed: **42**

Eğitim sonucunda:

- En iyi epoch: **20**
- Final Training MAE: **122.1239 m**
- Best Validation MAE: **121.8414 m**

elde edilmiştir.

En başarılı checkpoint bağımsız test veri kümesi üzerinde değerlendirilmiş ve:

- Test MAE: **124.6181 m**
- Mean Signed Error: **−77.3460 m**
- Maximum Absolute Error: **602.6687 m**

sonuçları elde edilmiştir.

Validation MAE ile Test MAE arasındaki fark yalnızca:

**2.7767 m**

olarak hesaplanmıştır.

Training, validation ve test sonuçlarının birbirine yakın olması mevcut baseline deneyinde belirgin bir overfitting davranışı olmadığını göstermektedir.

Bununla birlikte Actual vs Predicted ve Prediction Error Histogram analizlerinde modelin özellikle yüksek görüş mesafelerinde sistematik **underestimation** davranışı gösterdiği tespit edilmiştir.

Ayrıca ground-truth değerleri geniş bir aralığa yayılmasına rağmen model tahminlerinin daha dar bir aralıkta yoğunlaştığı **prediction-range compression** davranışı gözlemlenmiştir.

ResNet50 baseline modeli mevcut konfigürasyon altında araştırma önerisindeki **MAE < 100 metre** hedefini karşılayamamıştır.

---

# Baseline Karşılaştırmasının Mevcut Durumu

Day 14 itibarıyla her iki baseline model:

- geliştirildi,
- eğitildi,
- checkpoint olarak kaydedildi,
- bağımsız test kümesinde değerlendirildi,
- sayısal çıktıları kaydedildi,
- evaluation grafikleri oluşturuldu,
- deneysel gözlemleri dokümante edildi.

Mevcut temel sonuçlar:

| Metrik | VGG16 | ResNet50 |
| --- | ---: | ---: |
| Best Epoch | **18** | **20** |
| Best Validation MAE | **69.9705 m** | **121.8414 m** |
| Test MAE | **66.7227 m** | **124.6181 m** |
| Mean Signed Error | **−17.3877 m** | **−77.3460 m** |
| MAE < 100 m | **Evet** | **Hayır** |

ResNet50'nin Test MAE değeri VGG16'dan:

**57.8954 m**

daha yüksektir.

Başka bir ifadeyle mevcut baseline deneyinde VGG16, bağımsız test MAE açısından ResNet50'den belirgin biçimde daha düşük hata üretmiştir.

Bu sonuç başlangıç hipotezindeki ResNet50'nin daha düşük MAE üretmesi yönündeki beklentiyle uyumlu değildir.

Bununla birlikte hipotezde geçen **istatistiksel anlamlılık** ifadesinin değerlendirilmesi yalnızca tek bir aggregate MAE karşılaştırması üzerinden yapılmayacaktır.

---

# Model Karşılaştırma Yaklaşımı

VGG16 ve ResNet50 modelleri aynı sentetik veri kümesi ve aynı scene-based training/validation/test split'i kullanılarak değerlendirilmiştir.

Karşılaştırılabilirliği artırmak amacıyla aşağıdaki temel koşullar ortak tutulmuştur:

- Görüntü boyutu: **224 × 224**
- Batch size: **16**
- Epoch sayısı: **20**
- Optimizer: **Adam**
- Learning rate: **1e-4**
- Weight decay: **1e-5**
- Loss function: **L1Loss / MAE**
- Random seed: **42**
- Frozen backbone yaklaşımı
- ImageNet pretrained weights
- Preprocessing pipeline
- Evaluation pipeline

Model karşılaştırmasında temel seçim kriteri bağımsız test veri kümesi üzerindeki MAE performansıdır.

Test veri kümesi model geliştirme veya hiperparametre ayarlama amacıyla kullanılmayacak; yalnızca nihai baseline değerlendirmesi için kullanılacaktır.

---

# Nihai Baseline Seçimi ve Attention Mechanism

VGG16 ve ResNet50 baseline karşılaştırmasının tamamlanmasının ardından bağımsız test veri kümesinde daha düşük MAE sağlayan mimari Attention Mechanism aşamasının temel adayı olarak değerlendirilecektir.

Day 14 itibarıyla mevcut sonuçlar:

- VGG16 Test MAE: **66.7227 m**
- ResNet50 Test MAE: **124.6181 m**

olduğundan VGG16 mevcut deneysel sonuçlara göre daha başarılı baseline modeldir.

Resmi baseline seçimi karşılaştırmalı analiz aşamasının tamamlanmasıyla dokümante edilecektir.

Seçilen temel mimariye Attention Mechanism entegre edilecek ve model yeniden eğitilip değerlendirilecektir.

Attention Mechanism'ın amacı modelin görüş mesafesi tahmini açısından önemli uzamsal özelliklere daha fazla ağırlık vermesini sağlamaktır.

Attention modelinin performansı seçilen baseline modelle aynı değerlendirme prosedürü kullanılarak karşılaştırılacaktır.

Temel karşılaştırma:

```text
Selected Baseline Test MAE
            vs
Attention Model Test MAE
```

üzerinden gerçekleştirilecektir.

Attention entegrasyonunun performansı artırıp artırmadığı deneysel sonuçlara göre raporlanacaktır.

---

# Nihai Prototip

Projenin deneysel model geliştirme aşamasından sonra seçilen nihai model Flask API kullanılarak hafif bir web servisine entegre edilecektir.

HTML ve CSS kullanılarak basit ve fonksiyonel bir kullanıcı arayüzü geliştirilecektir.

Kullanıcı:

1. Bir yol görüntüsü yükleyebilecek,
2. Görüntü model preprocessing pipeline'ından geçirilecek,
3. Model görüş mesafesi tahmini üretecek,
4. Tahmin edilen mesafe kullanıcı arayüzünde metre cinsinden gösterilecektir.

Bu prototip, geliştirilen modelin Akıllı Ulaşım Sistemleri benzeri bir yazılım altyapısına nasıl entegre edilebileceğini göstermek amacıyla hazırlanacaktır.

---

# Proje Sınırları

- Temel araştırma problemi sürekli görüş mesafesi regresyonudur.
- Projenin ana amacı sis sınıflandırması yapmak değildir.
- Ana baseline karşılaştırması VGG16 ve ResNet50 mimarileri arasında gerçekleştirilmektedir.
- Temel performans metriği MAE'dir.
- Attention Mechanism yalnızca baseline karşılaştırması tamamlandıktan sonra seçilen mimariye uygulanacaktır.
- Gerçek dünya verilerinin kullanımı erişilebilirlik ve etiket uygunluğu doğrultusunda gerçekleştirilecektir.
- Web prototipi basit ve fonksiyonel tutulacaktır.
- Flask API model tahmininin web tabanlı kullanımını göstermek amacıyla kullanılacaktır.
- Proje uygulaması onaylanan TÜBİTAK 2209-A araştırma önerisinin bilimsel kapsamı dışına çıkmayacaktır.
- Training, validation ve test ayrımı scene-based gerçekleştirilmektedir.
- Aynı temel sahneye ait tüm görüntüler tek bir veri alt kümesinde tutulmaktadır.
- VGG16 ve ResNet50 mümkün olduğunca aynı eğitim ve değerlendirme koşullarında karşılaştırılmaktadır.
- Eğitim sırasında en iyi checkpoint validation MAE kullanılarak belirlenmektedir.
- Nihai baseline performansı bağımsız test kümesi üzerinde değerlendirilmektedir.
- Test veri kümesi model geliştirme veya hiperparametre ayarlama amacıyla kullanılmayacaktır.
- Baseline deneylerinin sonuçları sonradan değiştirilmeyecek; farklı hiperparametre veya eğitim stratejileri ayrı deneyler olarak kaydedilecektir.
- Grafiklerden elde edilen davranışsal gözlemler ile bunların olası nedenleri birbirinden ayrılacaktır.
- Bir davranışın nedeni deneysel olarak doğrulanmadıkça kesin nedensel sonuç olarak raporlanmayacaktır.

---

# Proje Uygulama İlkesi

Projenin bütün teknik ve bilimsel kararlarında onaylanan TÜBİTAK 2209-A Araştırma Önerisi Formu temel kaynak olarak kabul edilecektir.

Roadmap, araştırma önerisinde tanımlanan çalışmanın günlük uygulama sırasını belirlemek amacıyla kullanılacaktır.

Araştırma önerisinin kapsamını değiştiren yeni bir araştırma problemi, temel model mimarisi veya proje amacı eklenmeyecektir.

Teknik uygulama sırasında alınması gereken kararlar araştırma sorusu, hipotez, yöntem ve proje hedefleri ile uyumlu olacak şekilde değerlendirilecektir.

Geliştirilen:

- kaynak kod,
- veri hazırlama adımları,
- preprocessing kararları,
- deney parametreleri,
- checkpoint'ler,
- evaluation sonuçları,
- grafikler,
- deneysel gözlemler

düzenli olarak dokümante edilecektir.

Deneylerde kullanılan temel konfigürasyon merkezi yapılandırma dosyasında tutulacak ve tekrarlanabilirliği destekleyen random seed ve veri bölme politikaları korunacaktır.

Baseline sonuçlarında yapılacak herhangi bir değişiklik ayrı bir deney olarak kaydedilecek ve mevcut referans sonuçların üzerine yazılmayacaktır.

Bu yaklaşım proje sürecinin bilimsel olarak izlenebilir, tekrarlanabilir ve denetlenebilir olmasını sağlayacaktır.

---

# Güncel Proje Durumu — Day 14

Day 14 itibarıyla:

- ✓ Sentetik veri hazırlama tamamlandı.
- ✓ Scene-based split oluşturuldu.
- ✓ Preprocessing pipeline tamamlandı.
- ✓ PyTorch Dataset ve DataLoader altyapısı tamamlandı.
- ✓ VGG16 baseline geliştirildi.
- ✓ VGG16 eğitildi.
- ✓ VGG16 bağımsız test değerlendirmesi tamamlandı.
- ✓ VGG16 proje MAE hedefini karşıladı.
- ✓ ResNet50 baseline geliştirildi.
- ✓ ResNet50 eğitildi.
- ✓ ResNet50 bağımsız test değerlendirmesi tamamlandı.
- ✓ ResNet50 evaluation grafikleri analiz edildi.
- ✓ ResNet50 için overfitting analizi gerçekleştirildi.
- ✓ ResNet50 yüksek visibility underestimation davranışı dokümante edildi.
- ✓ Her iki baseline için deney kayıt ve evaluation çıktıları oluşturuldu.
- ⏳ VGG16–ResNet50 karşılaştırmalı analizinin tamamlanması.
- ⏳ Nihai baseline mimarisinin resmi olarak seçilmesi.
- ⏳ Attention Mechanism entegrasyonu.
- ⏳ Attention modelinin eğitilmesi ve değerlendirilmesi.
- ⏳ Gerçek dünya veri değerlendirmesi / uygunluk durumunun kesinleştirilmesi.
- ⏳ Flask tabanlı prototipin geliştirilmesi.