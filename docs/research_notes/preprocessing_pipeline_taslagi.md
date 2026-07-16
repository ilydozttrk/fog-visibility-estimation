# Ön İşleme Pipeline Taslağı

## 1. Amaç

Bu doküman, TÜBİTAK 2209-A projesinde kullanılacak FRIDA görüntülerinin VGG16 ve ResNet50 modellerine hazırlanması için uygulanacak ön işleme adımlarını tasarlamak amacıyla oluşturulmuştur.

Bu aşamada herhangi bir görüntü fiziksel olarak dönüştürülmeyecek ve model eğitimi yapılmayacaktır. Amaç; görüntü boyutlandırma, normalizasyon, veri bölme ve veri akışıyla ilgili teknik kararları önceden belirlemektir.

---

## 2. Görüntü Ön İşleme Kavramı

Görüntü ön işleme, ham görüntülerin derin öğrenme modelinin kabul edebileceği standart ve tutarlı bir yapıya dönüştürülmesidir.

FRIDA veri setindeki görüntüler 640 × 480 çözünürlüğünde ve RGB renk modundadır. Ancak transfer öğrenmede kullanılacak VGG16 ve ResNet50 modellerinin girişine verilmeden önce görüntülerin belirli işlemlerden geçirilmesi gerekmektedir.

Ön işleme sürecinin temel amaçları şunlardır:

- Görüntüleri modellerin beklediği giriş boyutuna dönüştürmek
- Piksel değerlerini önceden eğitilmiş model ağırlıklarıyla uyumlu hâle getirmek
- Tüm görüntüler için tutarlı bir veri yapısı oluşturmak
- Eğitim, doğrulama ve test verilerini birbirinden ayırmak
- Veri sızıntısını önlemek
- Model karşılaştırmasının aynı koşullarda yapılmasını sağlamak
- Eğitim verisinin çeşitliliğini kontrollü şekilde artırmak

---

## 3. Proje Kapsamında Değerlendirilecek Ön İşleme Adımları

FRIDA veri seti için aşağıdaki işlemler değerlendirilmiştir:

1. Görüntü dosyalarının okunması
2. Görüntülerin RGB renk modunda olduğunun doğrulanması
3. Temel sahnelerin ve sis varyasyonlarının belirlenmesi
4. Verinin sahne bazlı olarak eğitim, doğrulama ve test kümelerine ayrılması
5. Görüntülerin ortak giriş boyutuna dönüştürülmesi
6. Görüntü oranının korunması veya doğrudan yeniden boyutlandırma seçeneklerinin karşılaştırılması
7. Model mimarisine uygun normalizasyon uygulanması
8. Yalnızca eğitim verisine veri artırma uygulanması
9. Görüntülerin batch yapısına dönüştürülmesi
10. Aynı veri bölünmesinin VGG16 ve ResNet50 için kullanılması

---

## 4. Ön İşlemede Temel İlkeler

### 4.1 Ham Verinin Korunması

`data/raw/frida` klasöründeki orijinal görüntüler üzerinde doğrudan değişiklik yapılmayacaktır.

Ön işlenmiş veriler gerektiğinde ayrı bir klasörde tutulacaktır:

```text
data/processed/

```

Bu yaklaşım, deneylerin tekrarlanabilirliğini ve ham verinin korunmasını sağlar.

### 4.2 Veri Sızıntısının Önlenmesi

FRIDA veri setinde aynı temel sahnenin farklı sis koşullarında oluşturulmuş birden fazla görüntüsü bulunmaktadır.

Aynı sahneye ait görüntülerin bir kısmının eğitim, diğer kısmının test kümesine alınması modelin sahneyi önceden görmesine neden olabilir. Bu durum test performansının gerçekte olduğundan daha yüksek görünmesine yol açar.

Bu nedenle veri bölme işlemi tek tek görüntüler üzerinden değil, temel sahneler üzerinden gerçekleştirilecektir.

### 4.3 Modeller Arasında Adil Karşılaştırma

VGG16 ve ResNet50 modelleri aşağıdaki ortak koşullarda karşılaştırılacaktır:

- Aynı eğitim, doğrulama ve test kümeleri
- Aynı giriş görüntü boyutu
- Aynı regresyon hedefleri
- Aynı veri artırma politikası
- Aynı değerlendirme metriği
- Aynı rastgelelik tohumu

Normalizasyon işlemi ise her modelin önceden eğitilmiş ağırlıklarının gerektirdiği biçimde uygulanacaktır.

### 4.4 Veri Artırmanın Sınırlandırılması

Veri artırma yalnızca eğitim kümesine uygulanacaktır.

Doğrulama ve test görüntülerine veri artırma uygulanmayacaktır. Bu kümelerde yalnızca zorunlu yeniden boyutlandırma ve model uyumlu normalizasyon işlemleri kullanılacaktır.

Ayrıca görüş mesafesi tahminini bozabilecek aşırı renk, kontrast veya sis değişikliklerinden kaçınılacaktır.

---

## 5. İlk Değerlendirme

FRIDA veri setinin küçük olması ve aynı temel sahnelere ait farklı sis varyasyonları içermesi nedeniyle ön işleme sürecinde en kritik konu veri sızıntısının engellenmesidir.

Bu nedenle projenin ön işleme yaklaşımı aşağıdaki esaslara dayanacaktır:

- ham veriyi değiştirmeme,
- sahne bazlı veri bölme,
- modeller için ortak giriş boyutu,
- model uyumlu normalizasyon,
- yalnızca eğitim verisine kontrollü veri artırma,
- tekrarlanabilir veri bölme ve deney yapısı.

Bir sonraki aşamada VGG16 ve ResNet50 için kullanılacak ortak görüntü boyutu belirlenecektir.

---

# 6. Görüntü Boyutlandırma (Resize) Kararı

## Mevcut Durum

FRIDA veri setindeki görüntüler 640 × 480 piksel çözünürlüğündedir.

Transfer öğrenmede kullanılacak VGG16 ve ResNet50 modelleri ise standart olarak 224 × 224 piksel giriş boyutu beklemektedir.

Bu nedenle tüm görüntülerin ortak bir giriş boyutuna dönüştürülmesi gerekmektedir.

## Değerlendirilen Yaklaşımlar

### Yaklaşım 1

Doğrudan 224 × 224 yeniden boyutlandırma

Avantajları

- Basit uygulama
- Hızlıdır

Dezavantajları

- Görüntü oranı değişebilir.
- Yol geometrisi ve nesne oranları bozulabilir.

---

### Yaklaşım 2

Aspect ratio korunarak yeniden boyutlandırma ve padding uygulanması

Avantajları

- Görüntü geometrisi korunur.
- Yol yapısı bozulmaz.
- Görüş mesafesi ile ilişkili görsel ipuçları daha doğru korunur.

Dezavantajları

- Görüntü kenarlarında padding oluşabilir.

---

## Seçilen Yaklaşım

Bu proje kapsamında görüntülerin aspect ratio korunarak yeniden boyutlandırılması ve gerekli durumlarda padding uygulanarak 224 × 224 giriş boyutuna dönüştürülmesi planlanmaktadır.

Bu yaklaşım hem transfer öğrenme modelleriyle uyumludur hem de görüş mesafesi tahmini açısından önemli olan yol geometrisinin korunmasını sağlamaktadır.

---

# 7. Normalizasyon Kararı

## Amaç

Transfer öğrenme modellerinin önceden öğrendikleri ağırlıkları doğru şekilde kullanabilmeleri için giriş görüntülerinin uygun biçimde normalize edilmesi gerekmektedir.

Ham görüntülerde piksel değerleri 0–255 aralığında bulunmaktadır. Bu değerler doğrudan modele verilmek yerine modelin beklediği giriş formatına dönüştürülecektir.

## Değerlendirilen Yaklaşımlar

### Yaklaşım 1

Manuel normalizasyon

Örnek:

- Piksel değerlerini 255'e bölmek
- Ortalama ve standart sapma kullanmak

Avantajları

- Basit uygulanabilir.
- Genel amaçlıdır.

Dezavantajları

- Önceden eğitilmiş model ağırlıklarıyla tam uyum sağlamayabilir.

---

### Yaklaşım 2

Modelin resmi preprocessing fonksiyonunun kullanılması

Avantajları

- Önceden eğitilmiş ImageNet ağırlıklarıyla tam uyumludur.
- Ek manuel ayar gerektirmez.
- Literatürde yaygın olarak kullanılan yaklaşımdır.

Dezavantajları

- Kullanılan derin öğrenme kütüphanesine bağlıdır.

---

## Seçilen Yaklaşım

Bu proje kapsamında VGG16 ve ResNet50 modelleri için ilgili derin öğrenme kütüphanesinin sağladığı resmi preprocessing fonksiyonlarının kullanılması planlanmaktadır.

Bu yaklaşım, transfer öğrenme sürecinde model ağırlıkları ile giriş görüntüleri arasındaki uyumu koruyacak ve modeller arasında adil karşılaştırma yapılmasını sağlayacaktır.

---

# 8. Ön İşleme İş Akışı (Workflow)

## Genel İş Akışı

Proje kapsamında uygulanması planlanan veri hazırlama süreci aşağıdaki sırayla gerçekleştirilecektir.

```text
FRIDA Ham Görüntüleri
        │
        ▼
Dosya Kontrolü
        │
        ▼
Sahne Kimliklerinin Belirlenmesi
        │
        ▼
Sahne Bazlı Train / Validation / Test Ayrımı
        │
        ▼
Aspect Ratio Korunarak Resize
        │
        ▼
Padding ile 224 × 224 Boyutuna Getirme
        │
        ▼
Model Uyumlu Normalizasyon
        │
        ▼
(Yalnızca Train Setinde)
Data Augmentation
        │
        ▼
Batch Oluşturma
        │
        ▼
VGG16 / ResNet50
```

---

## İş Akışının Açıklaması

### 1. Dosya Kontrolü

İlk aşamada veri setindeki tüm görüntülerin okunabilir olduğu doğrulanacaktır.

Bozuk veya eksik dosyalar tespit edilerek veri bütünlüğü kontrol edilecektir.

---

### 2. Sahne Kimliklerinin Belirlenmesi

FRIDA veri setinde aynı temel sahneye ait farklı sis seviyelerinde oluşturulmuş görüntüler bulunmaktadır.

Bu nedenle görüntüler yalnızca dosya adı üzerinden değil, ait oldukları temel sahneye göre gruplandırılacaktır.

---

### 3. Veri Bölme

Eğitim, doğrulama ve test kümeleri sahne bazlı olarak oluşturulacaktır.

Bu yöntem veri sızıntısını önleyecek ve modellerin daha gerçekçi değerlendirilmesini sağlayacaktır.

---

### 4. Resize

Tüm görüntüler aspect ratio korunarak yeniden boyutlandırılacaktır.

Gerekli durumlarda padding uygulanarak ortak giriş boyutu olan 224 × 224 elde edilecektir.

---

### 5. Normalizasyon

Her model için ilgili derin öğrenme kütüphanesinin sağladığı resmi preprocessing yöntemi uygulanacaktır.

---

### 6. Data Augmentation

Veri artırma yalnızca eğitim kümesine uygulanacaktır.

Doğrulama ve test kümeleri değiştirilmeden kullanılacaktır.

---

### 7. Batch Oluşturma

Ön işleme tamamlandıktan sonra görüntüler mini-batch yapısına dönüştürülecek ve model eğitimine hazır hale getirilecektir.

---

### 8. Model Eğitimi

Hazırlanan veri aynı koşullar altında hem VGG16 hem de ResNet50 modellerine verilecektir.

Bu sayede karşılaştırma adil ve tekrarlanabilir olacaktır.

---

# 9. Veri Bölme (Split) Planı

## Amaç

Model performansının gerçekçi biçimde değerlendirilebilmesi için eğitim, doğrulama ve test kümeleri birbirinden bağımsız oluşturulacaktır.

Bu süreçte veri sızıntısını önlemek temel öncelik olacaktır.

---

## Değerlendirilen Yaklaşımlar

### Yaklaşım 1

Rastgele görüntü bazlı veri bölme

Avantajları

- Kolay uygulanabilir.
- Veri dağılımı dengeli olabilir.

Dezavantajları

- Aynı temel sahne farklı veri kümelerinde yer alabilir.
- Veri sızıntısına neden olabilir.
- Model performansı olduğundan yüksek görünebilir.

---

### Yaklaşım 2

Sahne bazlı veri bölme

Avantajları

- Veri sızıntısını önler.
- Gerçek dünya performansını daha doğru yansıtır.
- Literatürde önerilen yaklaşımla uyumludur.

Dezavantajları

- Veri dağılımı daha dikkatli planlanmalıdır.

---

## Seçilen Yaklaşım

Bu proje kapsamında veri bölme işlemi görüntü bazlı değil, temel sahneler bazında gerçekleştirilecektir.

Aynı temel sahneye ait tüm sis varyasyonları aynı veri kümesinde tutulacaktır.

Bu yaklaşım model karşılaştırmasının güvenilirliğini artıracaktır.

---

## Planlanan Dağılım

Veri kümeleri aşağıdaki oranlar dikkate alınarak oluşturulacaktır.

- Eğitim (Train): %70
- Doğrulama (Validation): %15
- Test: %15

Sahne sayısının sınırlı olması nedeniyle kesin dağılım uygulama aşamasında temel sahneler dikkate alınarak belirlenecektir.

---

## Rastgelelik Kontrolü

Deneylerin tekrarlanabilir olması amacıyla veri bölme işlemi sabit bir rastgelelik tohumu (random seed) kullanılarak gerçekleştirilecektir.

Aynı seed değeri tüm deneylerde korunacaktır.

---

# 10. Ön İşleme Pipeline Özeti

Bu dokümanda FRIDA veri setinin ön işleme süreci için temel teknik kararlar belirlenmiştir.

Belirlenen yaklaşım aşağıdaki esaslara dayanmaktadır:

- Ham veri korunacaktır.
- Veri bölme işlemi sahne bazlı gerçekleştirilecektir.
- Görüntüler ortak giriş boyutuna dönüştürülecektir.
- Model uyumlu normalizasyon uygulanacaktır.
- Veri artırma yalnızca eğitim kümesine uygulanacaktır.
- Aynı veri hazırlama süreci hem VGG16 hem de ResNet50 için kullanılacaktır.

Bu taslak, ilerleyen günlerde gerçekleştirilecek veri hazırlama ve model geliştirme çalışmalarının temel referans dokümanı olacaktır.