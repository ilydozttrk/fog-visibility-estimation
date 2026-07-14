# Literatür Notları

Bu dosya, TÜBİTAK 2209-A araştırma önerisinde yer alan ve proje sürecinde incelenecek bilimsel çalışmaların yapılandırılmış notlarını içermektedir.

Literatür incelemesinde özellikle görüntü tabanlı görüş mesafesi tahmini, transfer öğrenme, derin evrişimsel sinir ağları, sürekli regresyon yaklaşımı ve model değerlendirme metrikleri üzerinde durulacaktır.

---

## Literatür İnceleme Şablonu

### Makale Bilgileri

- Makale Başlığı:
- Yazarlar:
- Yayın Yılı:
- Kaynak:
- DOI veya Bağlantı:

### Araştırma Problemi

Çalışmanın çözmeyi amaçladığı temel araştırma problemi bu bölümde açıklanacaktır.

### Kullanılan Veri Seti

Çalışmada kullanılan veri seti veya veri setleri belirtilecektir.

Veri setinin sentetik veya gerçek dünya verisi olup olmadığı ayrıca değerlendirilecektir.

### Görüş Mesafesi Etiket Türü

- Sürekli regresyon:
- Ayrık sınıflandırma:
- Ölçüm birimi:

Çalışmanın görüş mesafesini sürekli bir sayısal değer olarak mı yoksa belirli sınıflar üzerinden mi ele aldığı incelenecektir.

### Kullanılan Yöntem

Çalışmada uygulanan temel yöntem ve deneysel süreç özetlenecektir.

### Model Mimarisi

Kullanılan yapay sinir ağı veya derin öğrenme mimarileri belirtilecektir.

### Transfer Öğrenme Yaklaşımı

Önceden eğitilmiş model kullanılıp kullanılmadığı ve transfer öğrenmenin nasıl uygulandığı incelenecektir.

### Değerlendirme Metrikleri

Model performansının değerlendirilmesinde kullanılan metrikler belirtilecektir.

Özellikle MAE, MSE, RMSE ve doğruluk gibi metriklerin kullanımı incelenecektir.

### Temel Sonuçlar

Çalışmanın elde ettiği temel deneysel sonuçlar özetlenecektir.

### Çalışmanın Sınırlılıkları

Yazarlar tarafından belirtilen veya çalışma incelenirken tespit edilen sınırlılıklar kaydedilecektir.

### TÜBİTAK Projemizle İlişkisi

Çalışmanın, transfer öğrenme tabanlı VGG16 ve ResNet50 karşılaştırması ile sürekli görüş mesafesi tahmini gerçekleştiren TÜBİTAK 2209-A projemiz açısından önemi değerlendirilecektir.

### Proje Açısından Ortaya Çıkan Sorular veya Kararlar

Literatür çalışmasının proje yöntemi, veri hazırlama süreci, model eğitimi veya değerlendirme yaklaşımı açısından ortaya çıkardığı teknik sorular ve kararlar kaydedilecektir.

---

## İncelenecek Temel Çalışmalar

Araştırma önerisinde yer alan kaynakça doğrultusunda ilk aşamada aşağıdaki çalışmalar incelenecektir:

1. Li ve arkadaşları — Meteorolojik görüş tahmini için transfer öğrenme yaklaşımı.

2. Li — Transfer öğrenme ve derin evrişimsel sinir ağları tabanlı görünürlük tespiti.

3. FRIDA ve FRIDA2 veri setlerinin temelini oluşturan sisli yol görüntüsü ve sentetik veri üretimi çalışmaları.

4. Görüntü tabanlı görüş mesafesi tahmini ve Akıllı Ulaşım Sistemleri uygulamalarına yönelik ilgili çalışmalar.

---

## Literatür İnceleme Durumu

- [ ] Transfer öğrenme tabanlı meteorolojik görüş tahmini çalışması incelendi.
- [ ] Derin CNN tabanlı görünürlük tespiti çalışması incelendi.
- [ ] FRIDA veri seti dokümantasyonu incelendi.
- [ ] FRIDA2 veri seti dokümantasyonu incelendi.
- [ ] FVEI veri seti araştırıldı.
- [ ] FHVI veri seti araştırıldı.

---

# FRIDA Veri Seti — İlk Dokümantasyon İncelemesi

## Veri Setinin Adı

FRIDA — Foggy Road Image DAtabase

## Veri Setinin Temel Amacı

FRIDA, sisli yol görüntülerinde görüş ve kontrast iyileştirme yöntemlerinin değerlendirilmesi amacıyla hazırlanmış sentetik bir yol görüntüsü veri setidir.

Veri seti özellikle sis altında görüntü görünürlüğü, kontrast restorasyonu ve sisli görüntü işleme yöntemlerinin test edilmesine yönelik bir araştırma kaynağı olarak geliştirilmiştir.

## Veri Setinin Yapısı

FRIDA toplam 18 sentetik kentsel yol sahnesinden oluşmaktadır.

Veri setinde toplam 90 sentetik görüntü bulunmaktadır.

Her temel sahne için sisli görüntü varyasyonları ve sahneye ait bir derinlik haritası sağlanmaktadır.

Dokümantasyonda her sahne için dört sisli görüntü ile bir derinlik haritasının bulunduğu belirtilmektedir.

## Sis Türleri

FRIDA veri setinde farklı sis dağılımlarını temsil eden sentetik sis koşulları bulunmaktadır.

Dokümantasyonda aşağıdaki sis türleri belirtilmektedir:

- Homojen sis
- Heterojen sis
- Bulutlu homojen sis
- Bulutlu heterojen sis

Bu farklı sis yapıları, sisin görüntü üzerindeki etkisinin yalnızca tek tip atmosfer koşulu altında değerlendirilmemesine olanak sağlamaktadır.

## Derinlik Bilgisi

FRIDA'nın proje açısından önemli özelliklerinden biri sahnelere ait derinlik haritalarının bulunmasıdır.

Derinlik haritası, görüntüdeki piksellerin veya sahne bölgelerinin kamera ile olan göreli ya da fiziksel mesafe ilişkisini temsil eden uzamsal bilgi sağlamaktadır.

TÜBİTAK 2209-A araştırma önerisinde FRIDA ve FRIDA2 veri setlerindeki derinlik bilgilerinden sürekli görüş mesafesi regresyon etiketlerinin türetilmesi planlanmıştır.

Bu nedenle derinlik haritalarının dosya yapısı, değer aralığı ve fiziksel mesafe karşılığı Day 3 veri seti incelemesinde ayrıca doğrulanmalıdır.

## Görüş Mesafesi Etiketleri Açısından Durum

FRIDA dokümantasyonunun ilk incelemesinde doğrudan her görüntü için hazır ve açık biçimde etiketlenmiş metre cinsinden sürekli görüş mesafesi hedef değerleri bulunduğu doğrulanmamıştır.

Veri seti sisli görüntüler ve derinlik haritaları sağlamaktadır.

Bu durum, TÜBİTAK araştırma önerisinde belirtilen "derinlik haritalarından sürekli regresyon etiketlerinin türetilmesi" adımının teknik olarak ayrıca incelenmesini gerekli kılmaktadır.

Hazır bir görüş mesafesi etiketi bulunduğu varsayılmayacaktır.

Etiket üretim yöntemi, veri setinin gerçek dosyaları ve ilgili teknik yayın incelendikten sonra belirlenecektir.

## TÜBİTAK Projesi Açısından Kullanım Amacı

FRIDA, projenin ilk aşamasında VGG16 ve ResNet50 modellerinin sis etkilerini öğrenmesi ve iki mimarinin kontrollü sentetik veri koşullarında karşılaştırılması için başlangıç veri kaynağı olarak planlanmaktadır.

Araştırma önerisine göre FRIDA ve FRIDA2 sentetik olmalarına rağmen, temel sis etkilerinin öğrenilmesi ve farklı modellerin objektif biçimde karşılaştırılması açısından başlangıç noktası olarak seçilmiştir.

FRIDA'nın projedeki rolü nihai gerçek dünya performansını tek başına temsil etmek değildir.

Gerçek dünya koşullarına uyum ve genelleme yeteneği daha sonraki aşamada FVEI/FHVI verileri kullanılarak değerlendirilecektir.

## Tespit Edilen Sınırlılıklar

- Veri seti sentetiktir.
- Yalnızca 18 temel kentsel yol sahnesi içermektedir.
- Toplam görüntü sayısı modern derin öğrenme veri setlerine kıyasla sınırlıdır.
- Sentetik görüntüler ile gerçek dünya sis koşulları arasında alan farkı bulunabilir.
- Doğrudan metre cinsinden sürekli görüş mesafesi etiketi bulunduğu henüz doğrulanmamıştır.
- Derinlik haritalarından proje için kullanılacak regresyon hedefinin nasıl türetileceği teknik olarak doğrulanmalıdır.

## Day 3 İçin Doğrulanacak Noktalar

FRIDA veri seti indirildikten sonra aşağıdaki noktalar doğrudan dosyalar üzerinden kontrol edilecektir:

- Gerçek klasör ve dosya hiyerarşisi
- Toplam görüntü sayısı
- Görüntü dosyası formatları
- Görüntü çözünürlükleri
- Derinlik haritası dosya formatı
- Derinlik haritası değer aralığı
- Derinlik değerlerinin fiziksel mesafe birimi
- Sis türlerinin dosya adlarında nasıl temsil edildiği
- Her görüntü ile derinlik haritası arasındaki eşleşme yapısı
- Hazır görüş mesafesi etiketi veya metadata bulunup bulunmadığı
- Sürekli regresyon hedefi üretmek için kullanılabilecek teknik bilgi

## İlk Değerlendirme

FRIDA, TÜBİTAK 2209-A araştırma önerisinde tanımlanan sentetik başlangıç veri stratejisiyle uyumludur.

Ancak veri setinin doğrudan görüş mesafesi regresyon veri seti olduğu varsayılmamalıdır.

Özellikle metre cinsinden sürekli hedef değer üretimi konusu, projenin bilimsel geçerliliği açısından kritik bir teknik adımdır.

Bu nedenle etiket türetme yaklaşımı veri seti dosyaları ve ilgili teknik yayın incelenmeden kesinleştirilmeyecektir.

---

# FRIDA2 Veri Seti — İlk Dokümantasyon İncelemesi

## Veri Setinin Adı

FRIDA2 — Foggy Road Image Database 2

## Veri Setinin Temel Amacı

FRIDA2, görüntü tabanlı görünürlük iyileştirme (visibility restoration), sis giderme (dehazing) ve Akıllı Ulaşım Sistemleri (ITS) alanında geliştirilen görüntü işleme algoritmalarını değerlendirmek amacıyla oluşturulmuş sentetik bir yol görüntüsü veri setidir.

FRIDA veri setinin genişletilmiş sürümüdür.

## Veri Setinin Yapısı

FRIDA2 toplam **66 farklı yol sahnesi** içermektedir.

Her sahne için aşağıdaki dosyalar bulunmaktadır:

- Sis olmayan referans görüntü
- Derinlik haritası (Depth Map)
- Homojen sisli görüntü
- Heterojen sisli görüntü
- Bulutlu homojen sisli görüntü
- Bulutlu heterojen sisli görüntü

Toplamda yaklaşık **330 sentetik görüntü** bulunmaktadır.

## FRIDA ile Karşılaştırma

FRIDA:

- 18 temel sahne
- 90 sentetik görüntü

FRIDA2:

- 66 temel sahne
- 330 sentetik görüntü

Dolayısıyla FRIDA2 hem daha fazla sahne çeşitliliği hem de daha fazla eğitim örneği sağlamaktadır.

## Sis Türleri

FRIDA2 aşağıdaki sis tiplerini içermektedir:

- Homojen sis
- Heterojen sis
- Bulutlu homojen sis
- Bulutlu heterojen sis

Bu yapı farklı atmosferik koşullar altında model davranışını incelemeye olanak sağlar.

## Derinlik Bilgisi

Her sahneye ait bir derinlik haritası bulunmaktadır.

Bu derinlik haritaları sahnedeki nesnelerin kamera ile olan uzaklık bilgisini temsil etmektedir.

Araştırma önerimiz doğrultusunda sürekli görüş mesafesi regresyon etiketlerinin oluşturulmasında bu derinlik bilgilerinin kullanılabilirliği araştırılacaktır.

## Görüş Mesafesi Etiketleri

İlk dokümantasyon incelemesine göre FRIDA2 doğrudan her görüntü için metre cinsinden hazır görüş mesafesi etiketi sağlamamaktadır.

Veri setinin temel amacı görüntü iyileştirme algoritmalarının değerlendirilmesidir.

Bu nedenle proje kapsamında kullanılacak regresyon hedeflerinin oluşturulması veri hazırlama aşamasında ayrıca gerçekleştirilecektir.

## TÜBİTAK Projesindeki Rolü

FRIDA2, FRIDA ile birlikte projenin ilk eğitim aşamasında kullanılacak temel sentetik veri setidir.

Bu veri seti sayesinde:

- VGG16 ve ResNet50 aynı kontrollü veri üzerinde karşılaştırılacaktır.
- Modeller sis etkisini öğrenmeye başlayacaktır.
- En düşük MAE sağlayan temel mimari belirlenecektir.

Gerçek dünya performansı ise sonraki aşamada FVEI/FHVI veri setleri ile değerlendirilecektir.

## Avantajları

- FRIDA'dan daha büyük veri setidir.
- Daha fazla sahne çeşitliliği sunmaktadır.
- Her sahne için depth map bulunmaktadır.
- Kontrollü sentetik sis üretimi sayesinde adil model karşılaştırması yapılabilir.

## Sınırlılıkları

- Sentetik veri setidir.
- Gerçek yol görüntülerini tamamen temsil etmez.
- Doğrudan hazır sürekli görüş mesafesi etiketi sağlamaz.
- Modern derin öğrenme veri setlerine kıyasla görüntü sayısı hâlâ sınırlıdır.

## İlk Değerlendirme

FRIDA2, TÜBİTAK 2209-A araştırma önerisinde tanımlanan başlangıç eğitim stratejisi için uygun görünmektedir.

Özellikle VGG16 ve ResNet50 modellerinin aynı kontrollü veri koşullarında objektif olarak karşılaştırılması açısından önemli bir veri kaynağıdır.

Gerçek dünya genelleme performansı ise proje planına uygun olarak daha sonraki aşamada gerçek dünya veri setleri üzerinde değerlendirilecektir.

---

# FVEI Veri Seti — İlk Dokümantasyon İncelemesi

## Veri Setinin Adı

FVEI — Fog Visibility Estimation Image Dataset

## Veri Setinin Temel Amacı

FVEI, görüntü tabanlı görüş mesafesi tahmini çalışmalarında kullanılmak üzere hazırlanmış gerçek dünya otoyol görüntülerinden oluşan bir veri setidir.

Veri seti özellikle derin öğrenme tabanlı görüş mesafesi regresyonu ve sis seviyesi tahmini çalışmalarını desteklemek amacıyla geliştirilmiştir.

## Veri Kaynağı

Görüntüler gerçek otoyol kameralarından elde edilmiştir.

Veri toplama süreci yaklaşık bir yıl sürmüştür.

Görüntüler farklı hava koşullarında ve farklı zaman dilimlerinde kaydedilmiştir.

## Veri Setinin Yapısı

Veri seti yaklaşık **15.000 gerçek görüntü** içermektedir.

Her görüntü iki farklı etiket taşımaktadır:

- Sis seviyesi (Fog Level)
- Görüş mesafesi (Visibility)

Etiketleme işlemi ulaştırma ve meteoroloji alanında uzman kişiler tarafından gerçekleştirilmiştir.

## Görüş Mesafesi Etiketleri

FVEI veri setinin en önemli avantajı görüntüler için görüş mesafesi bilgisinin bulunmasıdır.

Bu özellik veri setini görüntü tabanlı görüş mesafesi regresyonu için oldukça değerli hale getirmektedir.

Araştırma önerimiz açısından FVEI, sentetik veri üzerinde eğitilen modelin gerçek dünya koşullarında değerlendirilmesi amacıyla kullanılacaktır.

## TÜBİTAK Projesindeki Rolü

FVEI veri seti proje kapsamında başlangıç eğitiminde kullanılmayacaktır.

Öncelikle FRIDA ve FRIDA2 veri setleri üzerinde temel model eğitimi gerçekleştirilecektir.

VGG16 ve ResNet50 karşılaştırması tamamlandıktan sonra seçilen en iyi model FVEI veri seti ile gerçek dünya koşullarına uyarlanacaktır.

## Avantajları

- Gerçek dünya görüntülerinden oluşmaktadır.
- Büyük ölçekli veri setidir.
- Görüş mesafesi etiketi bulunmaktadır.
- Uzmanlar tarafından etiketlenmiştir.
- Transfer öğrenme sonrası ince ayar (fine-tuning) için uygundur.

## Sınırlılıkları

- Veri seti kamuya açık olarak doğrudan indirilemeyebilir.
- Erişim için yayın yazarları ile iletişim gerekebilir.
- Kullanım koşulları ayrıca doğrulanmalıdır.

## İlk Değerlendirme

FVEI, TÜBİTAK 2209-A araştırma önerisinde tanımlanan gerçek dünya doğrulama aşaması için en uygun veri setlerinden biridir.

Sentetik veri üzerinde eğitilen modelin gerçek yol görüntülerindeki performansını değerlendirmek amacıyla kullanılacaktır.

Veri setinin erişilebilirliği Day 2 kapsamında ayrıca doğrulanacaktır.

---

# FHVI Veri Seti — İlk Dokümantasyon İncelemesi

## Veri Setinin Adı

FHVI — Foggy Highway Visibility Images

## Veri Setinin Temel Amacı

FHVI, gerçek otoyol kameralarından elde edilen sisli görüntüler kullanılarak görüş seviyesi tahmini çalışmalarını desteklemek amacıyla geliştirilmiş bir veri setidir.

Veri seti özellikle gerçek dünya koşullarında görünürlük tahmini yapan yapay zekâ modellerinin geliştirilmesi ve değerlendirilmesi amacıyla oluşturulmuştur.

## Veri Kaynağı

Görüntüler Çin'in Anhui bölgesindeki yaklaşık 84 otoyol kamerasından elde edilmiştir.

Her kamera, yaklaşık 1 km mesafedeki meteoroloji istasyonlarında bulunan görünürlük ölçüm cihazları ile ilişkilendirilmiştir.

Görüntüler gerçek yol gözetleme sistemlerinden toplanmıştır.

## Görüş Mesafesi Etiketleri

Meteoroloji istasyonlarından elde edilen ölçümler referans olarak kullanılmıştır.

Ancak görüntüler doğrudan metre cinsinden sürekli görüş mesafesi değeri ile değil, uzmanlar tarafından doğrulanmış görünürlük seviyeleri (visibility level) ile etiketlenmiştir.

Bu nedenle FHVI temel olarak ayrık (discrete) görünürlük etiketleri içeren bir veri setidir.

## Veri Setinin Yapısı

Gerçek otoyol görüntülerinden oluşmaktadır.

Her görüntü için görünürlük seviyesi etiketi bulunmaktadır.

Veri seti gerçek trafik koşullarını temsil etmektedir.

## TÜBİTAK Projesindeki Rolü

FHVI veri seti proje kapsamında doğrudan temel regresyon eğitimi amacıyla kullanılmayacaktır.

Bunun yerine gerçek dünya görüntüleri üzerinde model davranışının değerlendirilmesi ve gerektiğinde ek doğrulama amacıyla kullanılabilecek alternatif bir gerçek dünya veri kaynağı olarak değerlendirilecektir.

## Avantajları

- Gerçek otoyol görüntüleri içermektedir.
- Meteoroloji uzmanları tarafından doğrulanmış etiketlere sahiptir.
- Gerçek trafik koşullarını temsil etmektedir.
- Transfer öğrenme sonrası gerçek dünya değerlendirmesi için uygundur.

## Sınırlılıkları

- Sürekli (metre cinsinden) görüş mesafesi etiketi sağlamamaktadır.
- Ayrık görünürlük seviyeleri kullanmaktadır.
- Kamuya açık erişim durumu sınırlıdır.
- Kullanım için yayın yazarları ile iletişim gerekebilir.

## İlk Değerlendirme

FHVI, gerçek dünya görüntüleri açısından oldukça değerli bir veri setidir.

Ancak proje kapsamında temel performans metriğimiz MAE ve problem tanımımız sürekli görüş mesafesi regresyonu olduğundan, FHVI başlangıç eğitim veri seti olarak değil; gerçek dünya doğrulaması ve ek değerlendirme amacıyla kullanılmaya daha uygundur.