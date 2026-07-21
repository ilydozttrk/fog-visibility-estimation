# 1. Hafta İlerleme Raporu

**Proje Adı:** Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Destek Programı:** TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı

**Rapor Dönemi:** 1. Hafta

**Hazırlayan:** İlayda Öztürk

---

# 1. Giriş

Bu rapor, proje kapsamında gerçekleştirilen ilk haftalık çalışmaları ayrıntılı olarak belgelemek amacıyla hazırlanmıştır.

İlk hafta boyunca temel hedef, model geliştirme sürecine başlamadan önce kullanılacak veri kümesini ayrıntılı olarak incelemek, güvenilir ve tekrarlanabilir bir veri hazırlama altyapısı oluşturmak ve sonraki haftalarda gerçekleştirilecek derin öğrenme deneyleri için gerekli yazılım altyapısını hazırlamaktır.

Bu doğrultuda veri setinin analizi, doğrulanması, ön işleme sürecinin planlanması ve eğitim sırasında kullanılacak veri yükleme mekanizmasının geliştirilmesi tamamlanmıştır.

---

# 2. Haftalık Hedefler

İlk hafta için belirlenen çalışma hedefleri aşağıdaki gibidir.

- FRIDA ve FRIDA2 veri setlerinin incelenmesi
- Veri setinin proje açısından uygunluğunun değerlendirilmesi
- Görüntülerin doğrulanması
- Veri kümesinin analiz edilmesi
- Sentetik görüş mesafesi veri kümesinin oluşturulması
- Ön işleme (Preprocessing) sürecinin tasarlanması
- Veri bölme stratejisinin belirlenmesi
- Eğitimde kullanılacak DataLoader altyapısının geliştirilmesi
- Proje dokümantasyonunun oluşturulması

Planlanan hedeflerin tamamı başarıyla gerçekleştirilmiştir.

---

# 3. Gerçekleştirilen Çalışmalar

## 3.1 FRIDA ve FRIDA2 Veri Setlerinin İncelenmesi

İlk olarak proje kapsamında kullanılacak FRIDA ve FRIDA2 veri setleri ayrıntılı biçimde incelenmiştir.

Bu inceleme sırasında;

- veri setinin amacı,
- görüntü üretim yöntemi,
- sis simülasyonu yaklaşımı,
- görüş mesafesi seviyeleri,
- klasör yapısı,
- görüntü formatları

detaylı olarak araştırılmıştır.

Literatür incelemesi sonucunda FRIDA veri setinin bilgisayar destekli oluşturulan sentetik yol sahnelerinden meydana geldiği ve farklı sis yoğunluklarını temsil eden görüntüler içerdiği belirlenmiştir.

Veri setinin görüş mesafesi tahmini problemi için uygun olduğu değerlendirilmiştir.

---

## 3.2 Veri Seti Analizi

Veri kümesinin teknik özellikleri ayrıntılı olarak incelenmiştir.

Bu kapsamda;

- toplam sahne sayısı,
- görüntü sayısı,
- çözünürlük,
- görüntü formatı,
- renk uzayı,
- dosya organizasyonu

kontrol edilmiştir.

Gerçekleştirilen analiz sonucunda;

- tüm görüntülerin PNG formatında olduğu,
- tüm görüntülerin RGB renk uzayında bulunduğu,
- çözünürlüklerin tutarlı olduğu,
- bozuk dosya bulunmadığı

tespit edilmiştir.

Bu analiz sonucunda veri kümesinin eğitim sürecinde doğrudan kullanılabilecek kaliteye sahip olduğu doğrulanmıştır.

---

## 3.3 Sentetik Görüş Mesafesi Veri Kümesinin Oluşturulması

Projede kullanılacak görünürlük seviyeleri belirlenmiş ve sentetik veri kümesi oluşturulmuştur.

Kullanılan görüş mesafeleri;

- 50 metre
- 80 metre
- 100 metre
- 150 metre
- 200 metre
- 300 metre
- 500 metre
- 800 metre

olarak belirlenmiştir.

Oluşturulan veri kümesi aşağıdaki özelliklere sahiptir.

| Özellik | Değer |
|---------|------:|
| Toplam Sahne | **84** |
| Toplam Görüntü | **672** |
| Görüş Mesafesi Seviyesi | **8** |

Bu yapı, sürekli görüş mesafesi tahmini (regression) problemi için temel veri kümesini oluşturmaktadır.

---

## 3.4 Veri Bölme Stratejisinin Tasarlanması

Derin öğrenme çalışmalarında aynı sahneye ait görüntülerin hem eğitim hem de test kümelerinde bulunması model performansının olduğundan yüksek görünmesine neden olabilmektedir.

Bu problemi önlemek amacıyla Scene-Based Split yaklaşımı tercih edilmiştir.

Bu yöntem sayesinde aynı sahneye ait tüm görüntüler yalnızca tek veri kümesinde yer almaktadır.

Veri kümesi aşağıdaki şekilde bölünmüştür.

| Veri Kümesi | Görüntü Sayısı |
|-------------|---------------:|
| Eğitim | **464** |
| Doğrulama | **96** |
| Test | **112** |

Bölme işlemi Random Seed = 42 kullanılarak gerçekleştirilmiş ve deneylerin tekrarlanabilir olması sağlanmıştır.

---

## 3.5 Ön İşleme (Preprocessing) Pipeline'ının Tasarlanması

Model eğitiminden önce uygulanacak ortak ön işleme süreci planlanmış ve geliştirilmiştir.

Pipeline aşağıdaki adımlardan oluşmaktadır.

- Görüntünün okunması
- RGB formatına dönüştürülmesi
- 224×224 boyutuna yeniden ölçeklendirilmesi
- ImageNet ortalama ve standart sapma değerleri kullanılarak normalizasyon uygulanması
- Tensor formatına dönüştürülmesi
- PyTorch DataLoader yapısına aktarılması

Bu yapı ilerleyen haftalarda geliştirilecek tüm CNN modelleri tarafından ortak olarak kullanılacaktır.

---

## 3.6 Veri Yükleme Altyapısının Geliştirilmesi

PyTorch tabanlı veri yükleme sistemi geliştirilmiştir.

Bu kapsamda;

- Dataset sınıfı hazırlanmış,
- Scene-Based veri bölme fonksiyonları geliştirilmiş,
- DataLoader altyapısı oluşturulmuş,
- yapılandırma (config) sistemi hazırlanmıştır.

Bu altyapı sayesinde tüm deneylerde aynı veri hazırlama süreci tekrar kullanılabilecektir.

---

## 3.7 Dokümantasyon Çalışmaları

İlk hafta boyunca yalnızca yazılım geliştirme değil, proje dokümantasyonu da eş zamanlı olarak hazırlanmıştır.

Bu kapsamda;

- README dosyası hazırlanmış,
- araştırma günlüğü oluşturulmuş,
- yöntem özeti hazırlanmış,
- proje kapsamı dokümanı oluşturulmuş,
- veri seti analiz notları yazılmıştır.

Bu dokümanlar proje sürecinin sistematik biçimde takip edilebilmesini sağlamaktadır.

---

# 4. Oluşturulan Dosyalar

Bu hafta aşağıdaki temel dosyalar geliştirilmiştir.

## Kaynak Kod

- preprocessing.py
- dataset_split.py
- dataloader.py
- config.py

## Dokümantasyon

- README.md
- arastirma_gunlugu.md
- literatur_notlari.md
- yontem_ozeti.md
- proje_kapsami.md

---

# 5. Karşılaşılan Problemler ve Çözümleri

İlk hafta boyunca aşağıdaki teknik konular üzerinde karar verilmiştir.

### Veri Sızıntısı Riski

Aynı sahneye ait görüntülerin farklı veri kümelerinde bulunmasının model performansını yapay olarak artırabileceği değerlendirilmiştir.

Bu nedenle Scene-Based Split yöntemi uygulanmıştır.

---

### Görüntü Boyutu

Transfer öğrenme modelleriyle uyumluluk sağlamak amacıyla tüm görüntüler 224×224 çözünürlüğe dönüştürülmüştür.

---

### Normalizasyon

ImageNet üzerinde önceden eğitilmiş ağırlıklar kullanılacağından ImageNet normalizasyon parametrelerinin kullanılmasına karar verilmiştir.

---

### Tekrarlanabilirlik

Deneylerin ilerleyen aşamalarda aynı şekilde tekrar edilebilmesi amacıyla Random Seed = 42 kullanılmıştır.

---

# 6. Hafta Sonu Değerlendirmesi

Birinci hafta sonunda proje için gerekli veri hazırlama süreci başarıyla tamamlanmıştır.

Veri kümesi ayrıntılı olarak analiz edilmiş, görüntüler doğrulanmış, veri sızıntısını önleyen veri bölme stratejisi uygulanmış ve tüm CNN modellerinde ortak kullanılacak ön işleme altyapısı geliştirilmiştir.

Bunun yanında PyTorch veri yükleme sistemi hazırlanmış ve proje dokümantasyonu oluşturulmuştur.

İlk hafta sonunda proje, model geliştirme aşamasına geçmeye hazır duruma getirilmiştir.

---

# 7. Sonraki Hafta Planı

İkinci haftada aşağıdaki çalışmaların gerçekleştirilmesi planlanmaktadır.

- VGG16 tabanlı regresyon modelinin geliştirilmesi
- Transfer öğrenme mimarisinin oluşturulması
- Eğitim (training) pipeline'ının hazırlanması
- Checkpoint mekanizmasının geliştirilmesi
- Deney kayıt sisteminin oluşturulması
- İlk baseline modelinin eğitilmesi
- Model değerlendirme (evaluation) altyapısının hazırlanması
- İlk deney sonuçlarının analiz edilmesi

---

# 8. Genel Sonuç

İlk hafta boyunca planlanan tüm çalışmalar başarıyla tamamlanmış ve proje, veri hazırlama aşamasından model geliştirme aşamasına geçebilecek seviyeye ulaştırılmıştır.

Oluşturulan altyapı, ilerleyen haftalarda geliştirilecek VGG16, ResNet50 ve Attention tabanlı modeller için ortak ve yeniden kullanılabilir bir temel oluşturmaktadır.