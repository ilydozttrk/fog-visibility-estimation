# Ön İşleme Pipeline Dokümantasyonu

## 1. Amaç

Bu doküman, TÜBİTAK 2209-A projesinde kullanılan FRIDA ve FRIDA2 tabanlı sentetik görüntü veri kümesinin VGG16 ve ResNet50 transfer öğrenme modellerine hazırlanması için tasarlanan ve uygulanan ön işleme sürecini açıklamaktadır.

Dokümanın ilk sürümü model eğitiminden önce görüntü boyutlandırma, normalizasyon, veri bölme ve veri akışıyla ilgili teknik kararları belirlemek amacıyla hazırlanmıştır.

Projenin mevcut aşamasında preprocessing ve DataLoader altyapısı uygulanmış; hem VGG16 hem de ResNet50 baseline deneylerinde başarıyla kullanılmıştır.

---

## 2. Görüntü Ön İşleme Kavramı

Görüntü ön işleme, ham görüntülerin derin öğrenme modelinin kabul edebileceği standart ve tutarlı bir yapıya dönüştürülmesidir.

FRIDA tabanlı görüntüler modele verilmeden önce ortak giriş formatına dönüştürülmektedir.

Ön işleme sürecinin temel amaçları şunlardır:

- Görüntüleri modellerin beklediği giriş boyutuna dönüştürmek
- Piksel değerlerini ImageNet üzerinde önceden eğitilmiş model ağırlıklarıyla uyumlu hâle getirmek
- Tüm görüntüler için tutarlı bir veri yapısı oluşturmak
- Eğitim, doğrulama ve test verilerini birbirinden bağımsız tutmak
- Veri sızıntısını önlemek
- Model karşılaştırmasının aynı veri koşullarında yapılmasını sağlamak
- Deneylerin tekrarlanabilirliğini korumak

---

## 3. Proje Kapsamında Uygulanan Ön İşleme Adımları

Proje kapsamında kullanılan veri hazırlama süreci aşağıdaki temel adımlardan oluşmaktadır:

1. Görüntü dosyalarının okunması
2. Görüntülerin RGB renk formatına dönüştürülmesi
3. Temel sahnelerin ve görüntü varyasyonlarının belirlenmesi
4. Verinin sahne bazlı olarak eğitim, doğrulama ve test kümelerine ayrılması
5. Görüntülerin ortak model giriş boyutuna dönüştürülmesi
6. ImageNet uyumlu normalizasyon uygulanması
7. Görüntü ve regresyon hedeflerinin `FogVisibilityDataset` üzerinden yüklenmesi
8. Verilerin mini-batch yapısına dönüştürülmesi
9. Aynı veri bölünmesinin VGG16 ve ResNet50 modellerinde kullanılması
10. Sabit random seed kullanılarak deneylerin tekrarlanabilirliğinin korunması

---

## 4. Ön İşlemede Temel İlkeler

### 4.1 Ham Verinin Korunması

Orijinal veri üzerinde doğrudan ve geri döndürülemez değişiklik yapılmamaktadır.

Model eğitiminde kullanılacak veri ve üretilen metadata yapıları proje içerisindeki ilgili veri klasörlerinde ayrı olarak tutulmaktadır.

Bu yaklaşım:

- ham verinin korunmasını,
- deneylerin yeniden gerçekleştirilebilmesini,
- farklı preprocessing stratejilerinin ileride karşılaştırılabilmesini

sağlamaktadır.

---

### 4.2 Veri Sızıntısının Önlenmesi

FRIDA ve FRIDA2 tabanlı veri yapısında aynı temel sahnenin farklı sis koşullarını veya varyasyonlarını temsil eden birden fazla görüntü bulunabilmektedir.

Aynı temel sahneye ait görüntülerin bir kısmının eğitim, diğer kısmının validation veya test kümesine alınması modelin sahne özelliklerini daha önce görmesine neden olabilir.

Bu durum bağımsız test performansının gerçekte olduğundan daha yüksek görünmesine yol açabilecek bir veri sızıntısı oluşturabilir.

Bu nedenle veri bölme işlemi tek tek görüntüler üzerinden değil, **scene-based split** yaklaşımı kullanılarak gerçekleştirilmiştir.

Aynı temel sahneye ait örneklerin farklı veri kümelerine dağılması engellenmiştir.

---

### 4.3 Modeller Arasında Adil Karşılaştırma

VGG16 ve ResNet50 baseline modelleri mümkün olduğunca aynı deneysel koşullar altında karşılaştırılmıştır.

Ortak tutulan temel koşullar şunlardır:

- Aynı training, validation ve test split'i
- Aynı giriş görüntü boyutu
- Aynı regresyon hedefleri
- Aynı preprocessing pipeline
- Aynı değerlendirme metriği
- Aynı random seed
- Aynı batch size
- Aynı baseline eğitim süresi
- Aynı evaluation prosedürü

Bu yaklaşım, modeller arasında gözlenen performans farklılıklarının veri hazırlama veya değerlendirme farklılıklarından kaynaklanma olasılığını azaltmaktadır.

---

### 4.4 Veri Artırma Politikası

Projenin başlangıç tasarımında veri artırmanın yalnızca training kümesine uygulanması ve validation/test kümelerinin değiştirilmeden değerlendirilmesi planlanmıştır.

Görüş mesafesi tahmini probleminde görüntünün sis yoğunluğu, kontrastı ve atmosferik görünümü doğrudan hedef değişkenle ilişkili olabileceğinden agresif renk, kontrast veya yapay sis dönüşümlerinin regresyon hedefinin anlamını değiştirebileceği değerlendirilmiştir.

Bu nedenle augmentation kullanımı kontrollü tutulmalı ve uygulanan her dönüşüm deney kayıtlarında açık biçimde belirtilmelidir.

Validation ve test verilerine performansı yapay biçimde değiştirecek augmentation uygulanmaması temel deneysel ilke olarak korunmaktadır.

---

## 5. Görüntü Boyutlandırma Kararı

### Mevcut Durum

Transfer öğrenmede kullanılan VGG16 ve ResNet50 modelleri için ortak giriş boyutu:

**224 × 224 piksel**

olarak belirlenmiştir.

Bu karar iki mimarinin aynı görüntü boyutu altında karşılaştırılmasını sağlamaktadır.

### İlk Tasarımda Değerlendirilen Yaklaşımlar

#### Yaklaşım 1 — Doğrudan 224 × 224 Resize

Avantajları:

- Basit uygulanabilir.
- Hesaplama açısından pratiktir.
- Standart CNN giriş yapısıyla doğrudan uyumludur.

Dezavantajları:

- Orijinal görüntü en-boy oranı farklıysa geometrik deformasyon oluşturabilir.

#### Yaklaşım 2 — Aspect Ratio Koruma ve Padding

Avantajları:

- Görüntü geometrisinin korunmasını sağlar.
- Yol ve sahne yapısındaki geometrik ilişkilerin bozulmasını azaltabilir.

Dezavantajları:

- Görüntü kenarlarında yapay padding bölgeleri oluşturabilir.
- Pipeline'ı bir miktar karmaşıklaştırır.

### Uygulanan Deneysel Ayar

Baseline deneylerinde VGG16 ve ResNet50 için aynı **224 × 224** giriş boyutu kullanılmıştır.

Dolayısıyla iki modelin performans karşılaştırmasında görüntü boyutu sabit tutulmuştur.

Gelecekte resize stratejisinin etkisi ayrıca araştırılacaksa bu değişiklik mevcut baseline deneyinden bağımsız bir ablation veya ek deney olarak değerlendirilmelidir.

---

## 6. Normalizasyon Kararı

### Amaç

VGG16 ve ResNet50 modellerinde ImageNet üzerinde önceden eğitilmiş ağırlıklar kullanılmaktadır.

Bu nedenle giriş görüntülerinin pretrained ağırlıkların beklediği dağılımla uyumlu biçimde normalize edilmesi gerekmektedir.

### Değerlendirilen Yaklaşımlar

#### Yaklaşım 1 — Genel Amaçlı Manuel Normalizasyon

Örneğin:

- Piksel değerlerini `[0, 1]` aralığına dönüştürmek
- Veri kümesine özgü ortalama ve standart sapma kullanmak

Bu yaklaşım uygulanabilir olmakla birlikte ImageNet pretrained ağırlıklarıyla kullanılan standart preprocessing prosedüründen farklılaşabilir.

#### Yaklaşım 2 — ImageNet Uyumlu Normalizasyon

ImageNet üzerinde önceden eğitilmiş CNN modelleriyle uyumlu standart normalizasyon değerlerinin kullanılmasıdır.

Bu yaklaşım:

- pretrained ağırlıklarla uyumluluğu korur,
- transfer öğrenme deneylerinin standartlaştırılmasını sağlar,
- VGG16 ve ResNet50 için ortak preprocessing koşulu oluşturur.

### Seçilen ve Uygulanan Yaklaşım

Proje kapsamında **ImageNet uyumlu normalizasyon** kullanılmaktadır.

Aynı normalizasyon prosedürü VGG16 ve ResNet50 baseline deneylerinde başarıyla uygulanmıştır.

---

## 7. Ön İşleme İş Akışı

### Güncel İş Akışı

```text
FRIDA + FRIDA2 Tabanlı Sentetik Veri
                │
                ▼
            labels.csv
                │
                ▼
       Scene-Based Split
                │
                ▼
     FogVisibilityDataset
                │
                ▼
         RGB Dönüşümü
                │
                ▼
        Resize (224×224)
                │
                ▼
   ImageNet Normalizasyonu
                │
                ▼
       PyTorch DataLoader
                │
                ▼
       Mini-Batch Oluşturma
                │
                ▼
        VGG16 / ResNet50
                │
                ▼
       Regression Output
```

---

## 8. İş Akışının Açıklaması

### 8.1 Dosya ve Metadata Kontrolü

Model eğitiminden önce görüntü yolları ve regresyon hedefleri `labels.csv` üzerinden okunmaktadır.

Görüntü ve etiket eşleşmelerinin korunması, supervised regression pipeline'ının temel gereksinimlerinden biridir.

---

### 8.2 Sahne Kimliklerinin Kullanılması

Aynı temel sahneye ait görüntüler scene identifier bilgileri kullanılarak birlikte değerlendirilmektedir.

Bu yapı scene-based split uygulanmasını mümkün kılmaktadır.

---

### 8.3 Veri Bölme

Veri kümesi training, validation ve test olmak üzere üç bağımsız bölüme ayrılmaktadır.

Bölme işlemi sahne bazlı gerçekleştirildiğinden aynı sahneye ait görüntüler farklı split'lere dağıtılmamaktadır.

---

### 8.4 RGB Dönüşümü

Model girişlerinin tutarlı kanal yapısına sahip olması amacıyla görüntüler RGB formatına dönüştürülmektedir.

Bu işlem VGG16 ve ResNet50'nin üç kanallı görüntü giriş yapısıyla uyumludur.

---

### 8.5 Resize

Görüntüler model girişinde ortak **224 × 224** boyutuna dönüştürülmektedir.

Bu boyut hem VGG16 hem de ResNet50 baseline deneylerinde sabit tutulmuştur.

---

### 8.6 Normalizasyon

Görüntülere ImageNet pretrained modelleriyle uyumlu normalizasyon uygulanmaktadır.

Bu işlem transfer öğrenme sırasında pretrained feature extractor'ların beklediği giriş dağılımının korunmasını amaçlamaktadır.

---

### 8.7 DataLoader

`FogVisibilityDataset` üzerinden hazırlanan görüntü ve hedef çiftleri PyTorch `DataLoader` yapısına aktarılmaktadır.

Baseline deneylerinde kullanılan temel DataLoader ayarları:

- Batch Size: **16**
- Number of Workers: **0**
- Random Seed: **42**

şeklindedir.

GPU kullanılması durumunda veri aktarım performansını desteklemek amacıyla `pin_memory` cihaz türüne göre yapılandırılabilmektedir.

---

### 8.8 Model Eğitimi

Hazırlanan DataLoader yapısı hem VGG16 hem de ResNet50 eğitim pipeline'larında kullanılmıştır.

Böylece her iki model aynı veri hazırlama altyapısı üzerinden eğitilmiştir.

---

## 9. Veri Bölme Planı ve Uygulaması

### Amaç

Model performansının gerçekçi biçimde değerlendirilebilmesi için training, validation ve test kümelerinin birbirinden bağımsız tutulması amaçlanmıştır.

Bu süreçte veri sızıntısının önlenmesi temel öncelik olarak belirlenmiştir.

### Değerlendirilen Yaklaşımlar

#### Yaklaşım 1 — Rastgele Görüntü Bazlı Split

Avantajları:

- Kolay uygulanabilir.
- Örnek sayılarının dengelenmesi daha kolay olabilir.

Dezavantajları:

- Aynı temel sahne farklı veri kümelerinde bulunabilir.
- Veri sızıntısına yol açabilir.
- Test performansının yapay biçimde yükselmesine neden olabilir.

#### Yaklaşım 2 — Scene-Based Split

Avantajları:

- Aynı sahnenin farklı split'lerde bulunmasını engeller.
- Veri sızıntısı riskini azaltır.
- Bağımsız test değerlendirmesinin güvenilirliğini artırır.

Dezavantajları:

- Örnek oranlarının tam olarak hedeflenen yüzdelere eşit olması her zaman mümkün olmayabilir.

### Seçilen ve Uygulanan Yaklaşım

Projede **scene-based split** uygulanmıştır.

Aynı temel sahneye ait örnekler aynı veri kümesinde tutulmaktadır.

Hedeflenen oranlar:

- Training: **%70**
- Validation: **%15**
- Test: **%15**

olarak belirlenmiştir.

Scene-based split nedeniyle gerçek görüntü sayılarının bu oranlarla birebir eşleşmesi zorunlu değildir.

Mevcut baseline deneylerinde oluşan veri dağılımı:

| Veri Kümesi | Görüntü Sayısı |
| --- | ---: |
| Training | **464** |
| Validation | **96** |
| Test | **112** |
| Toplam | **672** |

şeklindedir.

Bu aynı split hem VGG16 hem de ResNet50 baseline deneylerinde kullanılmıştır.

---

## 10. Rastgelelik ve Tekrarlanabilirlik Kontrolü

Deneylerin tekrarlanabilirliğini artırmak amacıyla sabit random seed kullanılmaktadır.

Mevcut deneylerde:

```text
RANDOM_SEED = 42
```

olarak belirlenmiştir.

Aynı random seed;

- veri bölme,
- model deneyleri,
- karşılaştırmalı baseline çalışmaları

boyunca korunmaktadır.

Ayrıca deterministik davranışı desteklemek amacıyla ilgili PyTorch reproducibility ayarları merkezi konfigürasyon üzerinden yönetilmektedir.

---

## 11. Baseline Deneylerinde Doğrulama

Hazırlanan preprocessing ve DataLoader altyapısı artık yalnızca teorik bir tasarım değildir.

Pipeline iki bağımsız transfer öğrenme baseline deneyinde kullanılmış ve doğrulanmıştır.

### VGG16

VGG16 modeli aynı preprocessing pipeline kullanılarak eğitilmiş ve bağımsız test veri kümesi üzerinde değerlendirilmiştir.

Elde edilen temel sonuçlar:

- Best Validation MAE: **69.9705 m**
- Test MAE: **66.7227 m**

olarak kaydedilmiştir.

### ResNet50

ResNet50 modeli de aynı veri hazırlama ve split yapısı kullanılarak eğitilmiş ve değerlendirilmiştir.

Elde edilen temel sonuçlar:

- Best Validation MAE: **121.8414 m**
- Test MAE: **124.6181 m**

olarak kaydedilmiştir.

Her iki modelin aynı preprocessing ve veri bölme altyapısını kullanması, ilerleyen karşılaştırmalı analiz için ortak deneysel temel sağlamaktadır.

---

## 12. ResNet50 Değerlendirmesinden Elde Edilen İlgili Gözlemler

ResNet50 evaluation sonuçlarının Day 14 kapsamında gerçekleştirilen görsel analizinde training ve validation eğrilerinin birbirine yakın ilerlediği ve belirgin bir overfitting davranışı göstermediği gözlemlenmiştir.

Bununla birlikte Actual vs Predicted ve Prediction Error Histogram analizleri, modelin özellikle yüksek görüş mesafelerinde sistematik underestimation davranışı gösterdiğini ortaya koymuştur.

Ground-truth değerleri geniş bir aralığa yayılmasına rağmen model tahminlerinin daha dar bir aralıkta yoğunlaşması **prediction-range compression** davranışı olarak değerlendirilmiştir.

ResNet50 için hesaplanan:

- Mean Signed Error: **−77.3460 m**
- Maximum Absolute Error: **602.6687 m**

değerleri de yüksek görüş mesafelerindeki büyük negatif tahmin hatalarıyla uyumludur.

Bu davranışın kesin nedeninin preprocessing pipeline olduğu sonucuna varılmamıştır.

Hedef değer dağılımı, frozen backbone kullanımı, eğitim süresi ve model mimarisi gibi faktörler olası açıklamalar arasında bulunmakla birlikte bunların etkisini belirlemek için ayrı deneyler gerekmektedir.

---

## 13. Güncel Teknik Kararlar

Projenin Day 14 aşamasında preprocessing ve veri hazırlama açısından aşağıdaki kararlar kesinleşmiştir:

- Ham veri korunacaktır.
- Veri bölme scene-based olarak gerçekleştirilecektir.
- VGG16 ve ResNet50 aynı split üzerinde değerlendirilecektir.
- Ortak giriş boyutu **224 × 224** olacaktır.
- ImageNet uyumlu normalizasyon kullanılacaktır.
- Validation ve test verilerine performansı değiştirecek augmentation uygulanmayacaktır.
- Random seed **42** olarak sabit tutulacaktır.
- Baseline modeller aynı temel veri hazırlama ve evaluation koşulları altında karşılaştırılacaktır.
- Mevcut preprocessing pipeline Attention Mechanism aşamasında da ortak altyapı olarak kullanılacaktır.
- Preprocessing veya eğitim ayarlarında yapılacak önemli değişiklikler mevcut baseline sonuçlarının üzerine sessizce uygulanmayacak; ayrı deney olarak kaydedilecektir.

---

## 14. Güncel Durum — Day 14

Ön işleme ve veri yükleme pipeline'ı proje kapsamında başarıyla uygulanmış ve iki baseline model üzerinde doğrulanmıştır.

FRIDA ve FRIDA2 tabanlı sentetik veri kümesi `labels.csv` üzerinden okunmakta, scene-based split ile training, validation ve test kümelerine ayrılmakta ve PyTorch tabanlı `FogVisibilityDataset` / `DataLoader` altyapısı üzerinden modellere aktarılmaktadır.

Mevcut veri dağılımı:

- **464 training görüntüsü**
- **96 validation görüntüsü**
- **112 test görüntüsü**

olmak üzere toplam **672 görüntüden** oluşmaktadır.

VGG16 ve ResNet50 aynı preprocessing ve veri bölme altyapısı kullanılarak eğitilmiş ve bağımsız test kümesi üzerinde değerlendirilmiştir.

Bu nedenle preprocessing pipeline artık projenin doğrulanmış ortak deneysel altyapısı olarak kabul edilmektedir.

Bir sonraki aşamada VGG16 ve ResNet50 baseline sonuçları ayrıntılı olarak karşılaştırılacak ve Attention Mechanism entegrasyonunda kullanılacak temel mimari deneysel sonuçlara göre belirlenecektir.