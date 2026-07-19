# Araştırma Günlüğü

## Gün 1 — Proje Temeli ve Araştırma Önerisiyle Uyumluluk

### Tamamlanan Görevler

- Onaylanan TÜBİTAK 2209-A araştırma önerisi incelendi.
- Araştırma sorusu ve proje hipotezi gözden geçirildi.
- Projenin temel amacı, bilimsel kapsamı ve sınırları dokümante edildi.
- Araştırma önerisinde tanımlanan beş aşamalı yöntem akışı proje notlarına aktarıldı.
- Git deposu başlatıldı.
- Python sanal ortamı oluşturuldu.
- Proje klasör yapısı hazırlandı.
- README dosyası oluşturuldu.
- Proje kapsamı ve yöntem özeti dokümante edildi.
- Literatür notlarının tutulacağı dosya yapısı oluşturuldu.

### Bugün Öğrendiklerim

Projenin temel araştırma probleminin sisli hava koşullarında görüntü tabanlı sürekli görüş mesafesi tahmini olduğu netleştirildi.

VGG16 ve ResNet50 mimarilerinin aynı veri ve eğitim koşulları altında karşılaştırılması gerektiği ve temel performans metriğinin metre cinsinden Ortalama Mutlak Hata (MAE) olduğu gözden geçirildi.

Temel model karşılaştırması tamamlanmadan Dikkat Mekanizması entegrasyonuna geçilmeyeceği ve Dikkat Mekanizmasının yalnızca en düşük test MAE değerini sağlayan modele uygulanacağı netleştirildi.

### Alınan Teknik Kararlar

- Proje dokümantasyonunun Türkçe tutulmasına karar verildi.
- Temel problem sürekli regresyon olarak korunacaktır.
- Ana model karşılaştırması VGG16 ve ResNet50 ile sınırlandırılacaktır.
- Temel değerlendirme metriği MAE olacaktır.
- Veri setleri ve model dosyaları doğrudan Git deposunda takip edilmeyecektir.
- Python sanal ortamı `.venv` klasöründe tutulacak ve Git takibinin dışında bırakılacaktır.
- Proje klasör yapısı veri hazırlama, model geliştirme, eğitim, değerlendirme, Dikkat Mekanizması ve API aşamalarını ayrı modüllerde takip edecek şekilde düzenlenmiştir.

### Karşılaşılan Sorunlar

İlk Git commit işlemi sırasında `.venv` sanal ortam klasörünün yanlışlıkla Git tarafından takip edildiği tespit edildi.

Ayrıca bazı dokümantasyon dosyalarının ilk oluşturulduklarında boş olarak commit edildiği fark edildi.

### Uygulanan Çözümler

Proje kök dizininde `.gitignore` dosyası oluşturuldu ve `.venv` klasörü Git takibinin dışında bırakıldı.

`git rm -r --cached .venv` komutu kullanılarak sanal ortam dosyaları yerel sistemden silinmeden Git indeksinden çıkarıldı.

İlk commit `git commit --amend --no-edit` komutu ile düzenlendi.

Boş oluşturulan dokümantasyon dosyaları gerekli içeriklerle doldurulmak üzere yeniden gözden geçirildi.

### Oluşturulan Dosyalar

- `.gitignore`
- `README.md`
- `docs/research_notes/proje_kapsami.md`
- `docs/research_notes/yontem_ozeti.md`
- `docs/research_notes/arastirma_gunlugu.md`
- `docs/literature/literatur_notlari.md`

### Sonraki Adım

FRIDA veri setinin dokümantasyonu incelenecek; veri setinin görüntü yapısı, sis senaryoları, derinlik bilgisi ve sürekli görüş mesafesi regresyon etiketi üretimi açısından projeye uygunluğu araştırılacaktır.

Literatür notları, araştırma önerisinde yer alan ilgili temel çalışmalar incelenerek doldurulacaktır.

---

# Gün 2 — Veri Seti Araştırması ve Envanter Çalışması

## Tamamlanan Görevler

- FRIDA2 veri setinin teknik dokümantasyonu incelendi.
- FVEI veri setinin yapısı, etiketleme yöntemi ve erişilebilirliği araştırıldı.
- FHVI veri setinin yapısı, görünürlük etiketi yaklaşımı ve proje açısından kullanılabilirliği değerlendirildi.
- FRIDA, FRIDA2, FVEI ve FHVI veri setleri teknik açıdan karşılaştırıldı.
- Veri seti seçim kriterleri belirlendi.
- Veri stratejisini özetleyen **veri_seti_envanteri.md** dokümanı hazırlandı.

## Bugün Öğrendiklerim

FRIDA ve FRIDA2 veri setleri sentetik olmalarına rağmen kontrollü deney ortamı sağlamaları nedeniyle temel model eğitimi ve VGG16–ResNet50 karşılaştırması için uygun görünmektedir.

FVEI veri seti gerçek otoyol görüntülerinden oluşmakta ve görüş mesafesi bilgisi içermesi nedeniyle gerçek dünya ince ayarı (fine-tuning) için önemli bir adaydır.

FHVI veri seti de gerçek yol görüntüleri içermektedir; ancak temel olarak görünürlük seviyeleri üzerine odaklandığından sürekli görüş mesafesi regresyonu açısından FVEI'den farklı değerlendirilmektedir.

## Alınan Teknik Kararlar

- Başlangıç eğitiminde FRIDA ve FRIDA2 kullanılacaktır.
- Model karşılaştırması tamamlandıktan sonra gerçek dünya değerlendirmesi için öncelikli olarak FVEI kullanılacaktır.
- FHVI, erişim ve uygunluk durumuna bağlı olarak ek doğrulama veri seti olarak değerlendirilecektir.
- Veri setlerinin projedeki rolleri **veri_seti_envanteri.md** dosyasında standartlaştırılmıştır.

## Karşılaşılan Sorunlar

Literatür incelemesi sırasında gerçek dünya veri setlerinin tamamının doğrudan indirilebilir olmadığı görüldü.

Bazı veri setlerine erişim için yayın yazarlarıyla iletişim kurulması gerekebileceği belirlendi.

## Uygulanan Çözümler

Araştırma önerisinde belirtilen risk yönetimi yaklaşımı doğrultusunda, erişim problemi yaşanması durumunda veri seti sahipleri ile iletişime geçilmesi ve sentetik veri setleri üzerinde temel model geliştirme çalışmalarının kesintisiz sürdürülmesi planlandı.

## Oluşturulan Dosyalar

- `docs/research_notes/veri_seti_envanteri.md`

## Sonraki Adım

FRIDA veri seti indirilecek, dosya yapısı incelenecek ve veri bütünlüğü doğrulanacaktır.

Görüntüler, derinlik haritaları ve klasör yapısı analiz edilerek veri hazırlama sürecine başlanacaktır.

---

# Gün 3 — FRIDA Veri Setinin İndirilmesi ve Teknik Analizi

## Tamamlanan Görevler

- FRIDA veri seti resmî kaynağından indirildi.
- Arşiv dosyası başarıyla çıkarıldı.
- Veri setinin klasör ve dosya yapısı incelendi.
- PNG görüntüleri ve FDD derinlik dosyaları tespit edildi.
- Örnek görüntüler açılarak görsel kontrol gerçekleştirildi.
- Etiket ve metadata yapısı incelendi.
- `dataset_analysis.ipynb` notebook'u oluşturuldu ve çalıştırıldı.
- Veri seti bütünlüğü otomatik kontrollerle doğrulandı.

## Teknik Bulgular

- Toplam dosya sayısı: 112
- PNG görüntü sayısı: 90
- FDD dosyası sayısı: 18
- TXT dosyası sayısı: 3
- MATLAB dosyası sayısı: 1
- Görüntü çözünürlüğü: 640 × 480
- Renk modu: RGB
- Bozuk veya okunamayan PNG görüntüsü: 0
- Çözünürlük ve renk modu dağılımları tutarlıdır.

## Etiket Yapısı

FRIDA veri setinde doğrudan kullanılabilecek `labels.csv` veya `annotations.json` benzeri bir sürekli görüş mesafesi etiketi bulunmadığı doğrulandı.

`ImageOwners.txt` dosyasının yalnızca veri seti sahipliği, araştırma amaçlı kullanım koşulları ve iletişim bilgilerini içerdiği görüldü.

Derinlik bilgileri `.fdd` formatındaki dosyalarda tutulmaktadır. Bu dosyaların yapısı ilerleyen veri hazırlama aşamalarında ayrıntılı olarak incelenecektir.

## Alınan Teknik Kararlar

- Ham veri üzerinde değişiklik yapılmayacaktır.
- FRIDA dosyaları `data/raw/frida` altında korunacaktır.
- Ham veri GitHub deposuna yüklenmeyecektir.
- `dataset_analysis.ipynb`, veri setinin ilk teknik referans notebook'u olarak kullanılacaktır.
- Regresyon hedeflerinin oluşturulması, araştırma önerisindeki yönteme bağlı olarak sonraki aşamalarda ele alınacaktır.

## Sonuç

FRIDA veri setinin eksiksiz ve okunabilir olduğu doğrulandı.

Tüm otomatik kontroller uygun sonuç verdi:

- Beklenen dosya dağılımı: UYGUN
- Beklenen çözünürlük dağılımı: UYGUN
- Beklenen renk modu dağılımı: UYGUN
- Görüntü bütünlüğü: UYGUN

Veri seti sonraki veri hazırlama çalışmalarına geçmek için teknik olarak hazırdır.

## Oluşturulan Dosya

- `notebooks/dataset_analysis.ipynb`

## Sonraki Adım

FRIDA veri setindeki görüntü, sahne ve derinlik dosyası ilişkileri ayrıntılı biçimde incelenecek; veri hazırlama ve regresyon hedefi oluşturma süreci için gerekli teknik yapı belirlenecektir.

---

# Gün 4 — Ön İşleme Pipeline Tasarımı

## Tamamlanan Görevler

- Görüntü ön işleme süreci literatür doğrultusunda incelendi.
- VGG16 ve ResNet50 modelleri için ortak giriş boyutu değerlendirildi.
- Görüntü yeniden boyutlandırma (resize) stratejisi belirlendi.
- Model uyumlu normalizasyon yaklaşımı seçildi.
- Veri hazırlama iş akışı (workflow) tasarlandı.
- Eğitim, doğrulama ve test veri bölme stratejisi planlandı.
- Ön işleme sürecini açıklayan `preprocessing_pipeline_taslagi.md` dokümanı oluşturuldu.

## Bugün Öğrendiklerim

Transfer öğrenme projelerinde ön işleme adımları model performansını doğrudan etkilemektedir.

Görüntü boyutlandırma, normalizasyon ve veri bölme stratejilerinin model eğitiminden önce belirlenmesi deneylerin tekrarlanabilirliği ve adil model karşılaştırması açısından önem taşımaktadır.

Ayrıca aynı temel sahneye ait görüntülerin farklı veri kümelerinde bulunmasının veri sızıntısına neden olabileceği görüldü.

Bu nedenle eğitim, doğrulama ve test ayrımının sahne bazlı yapılmasına karar verildi.

## Alınan Teknik Kararlar

- Ham görüntüler korunacaktır.
- Görüntüler ortak giriş boyutuna dönüştürülecektir.
- Modele uygun resmi preprocessing yöntemi kullanılacaktır.
- Veri bölme işlemi sahne bazlı gerçekleştirilecektir.
- Veri artırma yalnızca eğitim kümesine uygulanacaktır.
- Aynı ön işleme süreci hem VGG16 hem de ResNet50 modelleri için kullanılacaktır.

## Oluşturulan Dosya

- `docs/research_notes/preprocessing_pipeline.md`

## Sonraki Adım

FRIDA veri seti için gerçek ön işleme kodu geliştirilecek ve `preprocessing.py` dosyasında görüntü okuma, yeniden boyutlandırma ve normalizasyon işlemleri uygulanacaktır.

# Gün 5 – Sentetik Veri Kümesinin Oluşturulması

## Bugün Öğrendiklerim

FRIDA ve FRIDA2 veri setleri doğrudan sürekli görüş mesafesi regresyonu için yeterli çeşitlilikte etiket içermemektedir. Bu nedenle derinlik haritalarından yararlanılarak farklı görüş mesafelerini temsil eden sentetik görüntüler üretilebileceği öğrenildi.

Atmosferik saçılım modeli kullanılarak açık hava görüntülerinden farklı sis yoğunluklarında yeni görüntüler üretilebilmekte ve her görüntüye karşılık gelen görüş mesafesi değeri doğrudan etiket olarak kullanılabilmektedir. Böylece regresyon problemi için sürekli etiketlere sahip bir veri kümesi oluşturulabilmektedir.

Ayrıca veri üretim sürecinin doğrulanmasının, model eğitimine geçmeden önce olası veri hatalarının erken tespit edilmesi açısından önemli olduğu görüldü.

---

## Alınan Teknik Kararlar

- FRIDA ve FRIDA2 veri setleri birlikte kullanılmasına karar verildi.
- Görüş mesafesi seviyeleri **50, 80, 100, 150, 200, 300, 500 ve 800 metre** olarak belirlendi.
- Atmosferik saçılım modeli kullanılarak sentetik sis görüntüleri üretildi.
- Üretilen görüntülere ait görüş mesafesi etiketleri `labels.csv` dosyasında saklandı.
- Veri kümesinin doğruluğunu kontrol etmek amacıyla ayrı bir doğrulama betiği geliştirildi. (verify_generated_dataset.py)

---

## Karşılaşılan Durumlar

İlk veri üretim denemesinde FRIDA veri setindeki `.fdd` dosyalarının başında bulunan MATLAB yorum satırları nedeniyle okuma hatası oluştu. Derinlik haritaları okunurken yorum satırlarının göz ardı edilmesi sağlanarak problem giderildi.

Düzeltmenin ardından FRIDA ve FRIDA2 veri setleri başarıyla işlendi. FRIDA ve FRIDA2 veri setlerinde yer alan toplam 84 temel sahne kullanılarak, her sahne için sekiz farklı görüş mesafesi oluşturulmuş ve toplam 672 sentetik görüntü üretilmiştir. Veri doğrulama sürecinde eksik dosya veya hatalı etiket bulunmadığı doğrulandı.

---

## Gün Sonu Değerlendirmesi

Bugün proje kapsamında kullanılacak sentetik veri kümesi başarıyla oluşturuldu ve doğrulandı. Elde edilen veri kümesi sürekli görüş mesafesi etiketleriyle birlikte model eğitimine hazır hâle getirildi. Bir sonraki aşamada bu veri kümesini PyTorch tabanlı veri yükleme altyapısına entegre ederek model eğitim sürecine geçilecektir.

---

## Oluşturulan Dosyalar

- src/data/generate_visibility_dataset.py
- src/data/verify_generated_dataset.py
- data/generated/labels.csv

# Gün 6 – Veri Yükleme Altyapısı

## Bugün Öğrendiklerim

Transfer öğrenme tabanlı derin öğrenme modellerinde veri yükleme süreci, model eğitiminin temel bileşenlerinden biridir. Görüntülerin standart bir boyuta dönüştürülmesi, uygun normalizasyon işlemlerinin uygulanması ve etiketlerle birlikte doğru şekilde modele aktarılması, eğitim sürecinin güvenilir ve tekrarlanabilir olmasını sağlamaktadır.

PyTorch'un `Dataset` ve `DataLoader` yapıları sayesinde büyük veri kümeleri bellek kullanımını optimize edecek şekilde yönetilebilmekte, veriler eğitim sırasında batch'ler hâlinde modele aktarılabilmektedir.

Ayrıca regresyon problemlerinde etiketlerin `float32` veri tipinde tutulmasının, modelin sürekli görüş mesafesi değerlerini doğru şekilde öğrenebilmesi açısından önemli olduğu görüldü.

---

## Alınan Teknik Kararlar

- PyTorch tabanlı özel bir `FogVisibilityDataset` sınıfı geliştirildi.
- Görüntüler eğitim öncesinde **224×224** piksel boyutuna yeniden ölçeklendirildi.
- VGG16 ve ResNet50 ile uyumluluk sağlamak amacıyla **ImageNet normalizasyonu** kullanıldı.
- Görüş mesafesi etiketleri `float32` veri tipinde tutuldu.
- DataLoader için başlangıç aşamasında `batch_size=16` ve `num_workers=0` değerleri tercih edildi. `batch_size=16` başlangıç değeri olarak seçilmiş olup deneysel sonuçlara göre ilerleyen aşamalarda güncellenebilecektir.
- Veri kümesi `labels.csv` dosyası üzerinden okunacak şekilde yapılandırıldı.

---

## Karşılaşılan Durumlar

DataLoader testleri sırasında veri kümesindeki **672 görüntünün** tamamının başarıyla yüklendiği doğrulandı. Oluşturulan veri paketlerinin `(16, 3, 224, 224)` boyutunda olduğu ve görüş mesafesi etiketlerinin **50 m ile 800 m** arasında doğru şekilde modele aktarıldığı görüldü.

PyTorch tarafından verilen `pin_memory` uyarısının hata olmadığı, yalnızca sistemde CUDA destekli bir GPU bulunmadığı için belleğin sabitlenmediğini ifade ettiği belirlendi. Bu nedenle mevcut CPU tabanlı geliştirme ortamında herhangi bir değişiklik yapılmasına gerek görülmedi.

---

## Gün Sonu Değerlendirmesi

Bugün geliştirilen veri yükleme altyapısı sayesinde sentetik veri kümesi PyTorch modelleri tarafından doğrudan kullanılabilecek duruma getirildi. Böylece veri hazırlama süreci tamamlanmış oldu. Bir sonraki aşamada oluşturulan DataLoader kullanılarak VGG16 tabanlı temel modelin eğitilmesine başlanacaktır.

---

## Oluşturulan Dosyalar

- src/training/dataloader.py