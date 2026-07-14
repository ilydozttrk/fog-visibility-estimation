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