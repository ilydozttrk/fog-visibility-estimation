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

---

# Gün 7 – VGG16 Transfer Öğrenme Altyapısının Geliştirilmesi

## Tamamlanan Görevler

- VGG16 mimarisi transfer öğrenme yaklaşımı açısından incelendi.
- Eğitim parametrelerini merkezi olarak yönetmek amacıyla `config.py` dosyası oluşturuldu.
- Deneylerin tekrarlanabilirliğini sağlamak için sabit rastgelelik tohumu (random seed) tanımlandı.
- Deterministik PyTorch ayarları etkinleştirildi.
- ImageNet üzerinde önceden eğitilmiş VGG16 modeli projeye entegre edildi.
- VGG16 modelinin evrişimsel (backbone) katmanları donduruldu.
- Sınıflandırma katmanı kaldırılarak tek çıkışlı regresyon başlığı geliştirildi.
- Veri yükleme altyapısı sahne bazlı eğitim, doğrulama ve test kümelerini destekleyecek şekilde güncellendi.
- Eğitim (training) ve doğrulama (validation) döngüleri geliştirildi.
- En düşük doğrulama hatasına sahip modeli otomatik olarak kaydeden checkpoint mekanizması oluşturuldu.
- Eğitim altyapısı bir epoch'luk başlangıç testi ile doğrulandı.
- Geliştirilen kodlar GitHub deposuna aktarıldı.

## Bugün Öğrendiklerim

Transfer öğrenme yaklaşımında önceden eğitilmiş özellik çıkarıcı katmanların korunması ve yalnızca yeni eklenen regresyon katmanlarının eğitilmesi, sınırlı büyüklükteki veri kümelerinde daha kararlı bir başlangıç sağlamaktadır.

Ayrıca veri kümesinin sahne bazlı olarak ayrılması sayesinde aynı temel sahneye ait görüntülerin farklı veri kümelerinde yer alması engellenmiş ve model değerlendirmesinin daha güvenilir olması sağlanmıştır.

## Alınan Teknik Kararlar

- Eğitim parametreleri merkezi bir yapılandırma dosyası (`config.py`) üzerinden yönetilecektir.
- Tüm deneylerde `random_seed = 42` kullanılacaktır.
- Kayıp fonksiyonu olarak Ortalama Mutlak Hata (L1 Loss / MAE) kullanılacaktır.
- En düşük doğrulama hatasına sahip model otomatik olarak checkpoint şeklinde kaydedilecektir.
- VGG16 ve ResNet50 modelleri aynı veri bölünmesi ve aynı temel eğitim parametreleri kullanılarak karşılaştırılacaktır.

## Karşılaşılan Durumlar

Eğitim altyapısı geliştirilirken veri yükleme yapısının yalnızca tek bir DataLoader oluşturduğu görüldü. Model karşılaştırmasının güvenilirliği açısından eğitim, doğrulama ve test kümelerinin sahne bazlı olarak ayrılması gerektiğinden veri yükleme altyapısı yeniden düzenlendi.

Geliştirilen eğitim betiğinin doğru çalıştığını doğrulamak amacıyla tam eğitimden önce tek epoch'luk bir başlangıç testi gerçekleştirildi. Test sonucunda modelin veri okuyabildiği, eğitim yapabildiği, doğrulama gerçekleştirebildiği ve en iyi modeli başarıyla kaydedebildiği doğrulandı.

## Gün Sonu Değerlendirmesi

Bugün geliştirilen eğitim altyapısı sayesinde proje ilk çalışabilir derin öğrenme modeline ulaşmıştır. VGG16 tabanlı temel model veri okuyabilmekte, eğitim gerçekleştirebilmekte, doğrulama yapabilmekte ve en iyi modeli otomatik olarak kaydedebilmektedir.

Böylece veri hazırlama aşamasından model geliştirme aşamasına başarıyla geçilmiş ve VGG16 tabanlı baseline modelin eğitim altyapısı tamamlanmıştır.

## Oluşturulan Dosyalar

- `src/training/config.py`
- `src/training/utils.py`
- `src/training/train_vgg16.py`

## Sonraki Adım

VGG16 modeli tam eğitim süreciyle çalıştırılarak başlangıç performansı değerlendirilecek, deney sonuçları kayıt altına alınacak ve aynı deney koşulları altında ResNet50 modeli ile karşılaştırılacaktır.

---

# Gün 8 – VGG16 Baseline Modelinin İlk Tam Eğitimi ve Performans Değerlendirmesi

## Tamamlanan Görevler

- VGG16 tabanlı baseline modeli tam eğitim süreciyle çalıştırıldı.
- Eğitim sürecinde Adam optimizasyon algoritması ve L1 Loss (MAE) kullanıldı.
- Model toplam 20 epoch boyunca eğitildi.
- Her epoch sonunda eğitim (Training MAE) ve doğrulama (Validation MAE) performansı kaydedildi.
- En düşük doğrulama hatasına sahip model otomatik olarak checkpoint olarak kaydedildi.
- Eğitim geçmişini görselleştiren öğrenme eğrisi (loss_curve.png) oluşturuldu.
- Deney sonuçlarını kayıt altına almak amacıyla experiment_log.xlsx dosyası oluşturuldu.
- Eğitim sürecini özetleyen initial_training_log.md dosyası hazırlandı.

## Bugün Öğrendiklerim

Transfer öğrenme yaklaşımı kullanılarak geliştirilen VGG16 modeli, sentetik görüş mesafesi veri kümesi üzerinde kararlı bir öğrenme davranışı sergilemiştir.

Eğitim sürecinin ilk epochlarında doğrulama hatasında hızlı bir düşüş gözlenirken, ilerleyen epochlarda öğrenme hızının azalarak daha kararlı bir yapıya ulaştığı görülmüştür.

Ayrıca modelin en iyi doğrulama performansına 18. epoch sonunda ulaştığı ve sonraki epochlarda doğrulama hatasında çok küçük dalgalanmalar oluştuğu gözlenmiştir. Bu durum, modelin bu noktadan sonra hafif düzeyde overfitting eğilimi göstermeye başladığını düşündürmektedir.

## Alınan Teknik Kararlar

- Eğitim süresi başlangıç deneyi için 20 epoch olarak belirlendi.
- En düşük Validation MAE değerine sahip model sonraki deneylerde kullanılmak üzere checkpoint olarak saklandı.
- Tüm deney sonuçları standart bir deney kayıt dosyasında tutulacaktır.
- Eğitim performansı her deney sonunda grafik olarak kaydedilecektir.
- Aynı eğitim parametreleri ResNet50 modeli için de korunacaktır.

## Elde Edilen Sonuçlar

- Eğitim süresi: 20 epoch
- En iyi epoch: 18
- En düşük Validation MAE: **69.9705 metre**
- Araştırma önerisinde belirlenen **MAE < 100 metre** hedefi başarıyla karşılandı.

## Karşılaşılan Durumlar

Eğitim süreci boyunca herhangi bir çalışma zamanı (runtime) hatası ile karşılaşılmadı.

Validation MAE değeri 18. epoch sonrasında çok küçük değişimler göstermiş, ancak checkpoint mekanizması sayesinde en iyi model otomatik olarak korunmuştur.

## Gün Sonu Değerlendirmesi

Bugün proje kapsamında geliştirilen VGG16 tabanlı baseline modelinin ilk tam eğitimi başarıyla tamamlanmıştır.

Model, araştırma önerisinde belirlenen performans hedefini karşılayarak **69.9705 metre Validation MAE** değerine ulaşmıştır.

Böylece proje kapsamında geliştirilen ilk temel model başarıyla doğrulanmış ve VGG16 baseline modeli, ResNet50 ile gerçekleştirilecek karşılaştırmalı deneyler için referans model hâline gelmiştir.

## Oluşturulan Dosyalar

- `results/experiment_log.xlsx`
- `results/plots/loss_curve.png`
- `results/logs/initial_training_log.md`

## Sonraki Adım

Aynı veri bölünmesi ve aynı eğitim parametreleri kullanılarak ResNet50 tabanlı baseline model geliştirilecek ve iki modelin performansları MAE değerleri üzerinden karşılaştırılacaktır.

## Gün 9 — VGG16 Baseline Model Evaluation

Bugün VGG16 tabanlı transfer öğrenme modelinin bağımsız test kümesi üzerindeki performansı değerlendirildi. Eğitim sırasında kaydedilen en iyi checkpoint yüklenerek test görüntüleri üzerinde tahminler üretildi ve modelin genelleme başarısı analiz edildi.

Değerlendirme pipeline'ı `evaluation_vgg16.py` dosyasında geliştirildi. Pipeline kapsamında model checkpoint'inin yüklenmesi, test veri kümesinin değerlendirilmesi, MAE hesaplanması, tahmin sonuçlarının CSV formatında kaydedilmesi, değerlendirme özetinin JSON olarak oluşturulması ve otomatik Markdown raporunun üretilmesi gerçekleştirildi.

Model, 112 görüntüden oluşan bağımsız test kümesi üzerinde **66.7227 metre Test MAE** elde etti. Bu değer eğitim sırasında elde edilen **69.9705 metre Validation MAE** sonucuna oldukça yakın olup modelin daha önce görmediği sahnelere başarılı şekilde genelleme yapabildiğini göstermektedir.

Ek olarak gerçek ve tahmin edilen görünürlük değerlerini karşılaştıran saçılım grafiği ile hata dağılım histogramı oluşturuldu. Bu çıktılar ileride gerçekleştirilecek ResNet50 karşılaştırmaları ve nihai proje raporu için kullanılacaktır.

Bir sonraki aşamada aynı veri kümesi ve değerlendirme prosedürü kullanılarak ResNet50 tabanlı ikinci baseline model geliştirilecektir.

---

# Gün 10 – Haftalık Değerlendirme ve Literatür Güncellemesi

## Tamamlanan Görevler

- İkinci haftada gerçekleştirilen proje çalışmaları ayrıntılı olarak değerlendirildi.
- Haftalık ilerleme raporu (`week2_report.md`) hazırlandı.
- Haftalık gelişim kaydı (`weekly_progress_log.md`) oluşturuldu.
- ResNet50 mimarisi üzerine güncel literatür çalışmaları incelendi.
- İncelenen çalışmalar doğrultusunda literatür notları güncellendi.
- Danışman toplantısı öncesinde proje ilerleme notları hazırlandı.
- Üçüncü hafta çalışma planı oluşturuldu.
- Güncellenen dokümantasyon GitHub deposuna aktarıldı.

## Bugün Öğrendiklerim

Literatür incelemesi sonucunda ResNet50 mimarisinin görüntü tabanlı regresyon problemlerinde yaygın olarak kullanılan güçlü bir transfer öğrenme modeli olduğu görüldü.

Residual (artık) bağlantılar sayesinde derin sinir ağlarında gradyan kaybolması probleminin önemli ölçüde azaltılabildiği ve bunun daha derin mimarilerin daha kararlı şekilde eğitilmesini sağladığı öğrenildi.

İncelenen çalışmalarda temel modeller oluşturulduktan sonra dikkat mekanizmalarının (Attention Mechanism) modele entegre edilerek performansın artırıldığı görüldü. Bu yaklaşımın araştırma önerisinde planlanan çalışma akışı ile uyumlu olduğu değerlendirildi.

## Alınan Teknik Kararlar

- Üçüncü hafta çalışmalarında ResNet50 modeli geliştirilecektir.
- VGG16 ve ResNet50 modelleri aynı veri bölünmesi, aynı eğitim parametreleri ve aynı değerlendirme metriği kullanılarak karşılaştırılacaktır.
- Dikkat Mekanizması entegrasyonu yalnızca temel model karşılaştırmaları tamamlandıktan sonra gerçekleştirilecektir.
- Literatür notları proje süreci boyunca düzenli olarak güncellenecektir.

## Karşılaşılan Durumlar

Literatür incelemesi sırasında farklı çalışmaların farklı veri kümeleri, farklı eğitim stratejileri ve farklı performans metrikleri kullandığı görüldü. Bu durum doğrudan performans karşılaştırmalarını güçleştirmektedir.

Bu nedenle proje kapsamında tüm deneylerin aynı veri kümesi, aynı veri bölünmesi ve aynı eğitim parametreleri altında gerçekleştirilmesine karar verildi.

## Gün Sonu Değerlendirmesi

Bugün gerçekleştirilen haftalık değerlendirme ile ikinci hafta çalışmaları tamamlanmıştır. Proje dokümantasyonu güncellenmiş, literatür incelemesi genişletilmiş ve üçüncü hafta gerçekleştirilecek ResNet50 geliştirme süreci için teknik hazırlık tamamlanmıştır.

Böylece proje, ikinci temel model olan ResNet50'nin geliştirilmesine başlanabilecek aşamaya ulaşmıştır.

## Oluşturulan Dosyalar

- `docs/reports/week2_report.md`
- `docs/reports/weekly_progress_log.md`
- `docs/literature/literatur_notlari.md`

## Sonraki Adım

ResNet50 tabanlı ikinci baseline model geliştirilecek, ImageNet üzerinde önceden eğitilmiş ağırlıklar kullanılacak, modelin backbone katmanları dondurulacak ve VGG16 ile aynı eğitim koşulları altında karşılaştırmalı deneyler gerçekleştirilecektir.

---

# Gün 11 – ResNet50 Transfer Öğrenme Altyapısının Geliştirilmesi

## Tamamlanan Görevler

- ResNet50 mimarisi transfer öğrenme yaklaşımı açısından ayrıntılı olarak incelendi.
- VGG16 ve ResNet50 mimarileri teknik özellikleri bakımından karşılaştırıldı.
- ImageNet üzerinde önceden eğitilmiş ResNet50 modeli projeye entegre edildi.
- ResNet50 modelinin backbone katmanları donduruldu.
- Sınıflandırma katmanı kaldırılarak tek çıkışlı regresyon başlığı geliştirildi.
- ResNet50 modeli için bağımsız eğitim betiği (`train_resnet50.py`) oluşturuldu.
- Eğitim (training) ve doğrulama (validation) döngüleri VGG16 altyapısı temel alınarak uyarlandı.
- Checkpoint mekanizması ResNet50 modeli için yapılandırıldı.
- Deney kayıt sistemi ve eğitim loglarının otomatik oluşturulması sağlandı.
- Öğrenme eğrilerinin kaydedilmesi için gerekli altyapı geliştirildi.
- Kodun doğruluğunu kontrol etmek amacıyla sözdizimi (syntax) testi gerçekleştirildi.
- Model oluşturma (forward pass) testi başarıyla tamamlandı.
- DataLoader uyumluluğu doğrulandı.
- Eğitilebilir ve dondurulmuş parametre sayıları doğrulanarak backbone katmanlarının başarıyla dondurulduğu kontrol edildi.
- Geliştirilen kodlar GitHub deposuna aktarıldı.

## Bugün Öğrendiklerim

ResNet50 mimarisinin residual bağlantılar sayesinde çok daha derin olmasına rağmen kararlı şekilde eğitilebildiği görüldü.

Transfer öğrenme yaklaşımında yalnızca yeni eklenen regresyon katmanlarının eğitilmesi, önceden öğrenilmiş görsel özelliklerin korunmasını sağlamakta ve sınırlı büyüklükteki veri kümelerinde daha güvenilir sonuçlar elde edilmesine katkı sağlamaktadır.

Ayrıca geliştirilen eğitim altyapısının eğitim süreci başlamadan önce çeşitli doğrulama testlerinden geçirilmesinin olası yazılım hatalarının erken aşamada tespit edilmesini sağladığı görüldü.

## Alınan Teknik Kararlar

- ResNet50 modeli ImageNet üzerinde önceden eğitilmiş ağırlıklarla kullanılacaktır.
- Backbone katmanları dondurulacak ve yalnızca regresyon başlığı eğitilecektir.
- VGG16 ile aynı eğitim parametreleri korunarak adil model karşılaştırması gerçekleştirilecektir.
- Eğitim süreci boyunca en düşük doğrulama hatasına sahip model otomatik olarak checkpoint şeklinde kaydedilecektir.
- Deney sonuçları standart deney kayıt dosyasında saklanacaktır.

## Karşılaşılan Durumlar

ResNet50 mimarisinin VGG16'dan farklı olarak tam bağlantılı sınıflandırma katmanı yerine Global Average Pooling sonrasında tek bir `fc` katmanı kullandığı görüldü. Bu nedenle regresyon başlığının VGG16'dan farklı şekilde yeniden tasarlanması gerekti.

Geliştirilen eğitim betiğinin doğruluğunu kontrol etmek amacıyla Python sözdizimi doğrulaması, model oluşturma testi, DataLoader uyumluluk testi ve eğitilebilir parametre kontrolleri gerçekleştirildi. Yapılan doğrulamalar sonucunda eğitim altyapısının sorunsuz şekilde çalıştığı doğrulandı.

## Gün Sonu Değerlendirmesi

Bugün geliştirilen ResNet50 eğitim altyapısı sayesinde proje kapsamındaki ikinci temel model eğitim için hazır hâle getirilmiştir.

Model başarıyla oluşturulabilmekte, veri yükleme altyapısı ile uyumlu şekilde çalışabilmekte ve eğitim sürecini gerçekleştirebilecek teknik yeterliliğe sahiptir.

Böylece VGG16 ve ResNet50 modellerinin aynı deney koşulları altında karşılaştırılabileceği altyapı tamamlanmış ve bir sonraki aşama olan ResNet50 model eğitimi için hazırlık süreci tamamlanmıştır.

## Oluşturulan Dosyalar

- `src/training/train_resnet50.py`

## Sonraki Adım

ResNet50 tabanlı baseline model tam eğitim süreciyle çalıştırılacak, eğitim ve doğrulama performansı değerlendirilecek, en iyi model checkpoint olarak kaydedilecek ve elde edilen sonuçlar VGG16 modeli ile karşılaştırılacaktır.

---

# Gün 12 – ResNet50 Baseline Modelinin İlk Tam Eğitimi ve Performans Değerlendirmesi

## Tamamlanan Görevler

- ResNet50 tabanlı baseline modeli tam eğitim süreciyle çalıştırıldı.
- Eğitim sürecinde Adam optimizasyon algoritması ve L1 Loss (MAE) kullanıldı.
- Model toplam 20 epoch boyunca eğitildi.
- Her epoch sonunda eğitim (Training MAE) ve doğrulama (Validation MAE) performansı kaydedildi.
- En düşük doğrulama hatasına sahip model otomatik olarak checkpoint olarak kaydedildi.
- Eğitim geçmişini görselleştiren öğrenme eğrisi (`resnet50_loss_curve.png`) oluşturuldu.
- Deney sonuçları `experiment_log.xlsx` dosyasına kaydedildi.
- Eğitim sürecini özetleyen `resnet50_initial_training_log.md` dosyası oluşturuldu.
- Elde edilen performans sonuçları VGG16 baseline modeli ile karşılaştırıldı.

## Bugün Öğrendiklerim

ResNet50 modeli eğitim süreci boyunca kararlı bir öğrenme davranışı sergilemiş ve doğrulama hatası her epoch sonunda düzenli olarak azalmıştır.

Eğitim ve doğrulama hata değerlerinin birbirine oldukça yakın seyretmesi, modelin eğitim veri kümesini ezberlemeden öğrenebildiğini ve belirgin bir overfitting problemi oluşmadığını göstermektedir.

Ayrıca aynı eğitim parametreleri kullanıldığında daha derin bir mimariye sahip olmanın her zaman daha yüksek performans anlamına gelmediği görülmüştür. Bu durum, veri kümesinin yapısı ve seçilen hiperparametrelerin model performansı üzerindeki etkisini bir kez daha ortaya koymuştur.

## Alınan Teknik Kararlar

- ResNet50 modeli başlangıç deneyi için 20 epoch boyunca eğitilecektir.
- En düşük Validation MAE değerine sahip model sonraki deneylerde kullanılmak üzere checkpoint olarak saklanacaktır.
- Eğitim sürecinde kullanılan veri bölünmesi ve hiperparametreler VGG16 modeli ile aynı tutulacaktır.
- Model karşılaştırmaları yalnızca aynı deney koşullarında elde edilen sonuçlar üzerinden gerçekleştirilecektir.

## Elde Edilen Sonuçlar

- Eğitim süresi: **20 epoch**
- En iyi epoch: **20**
- En düşük Validation MAE: **121.8414 metre**

Model eğitim süreci boyunca doğrulama performansı sürekli olarak iyileşmiş ve son epoch sonunda en düşük doğrulama hatasına ulaşılmıştır.

## Karşılaşılan Durumlar

Eğitim süreci boyunca herhangi bir çalışma zamanı (runtime) hatası ile karşılaşılmamıştır.

Checkpoint mekanizması doğrulama performansındaki her iyileşmede başarılı şekilde çalışmış ve en iyi model otomatik olarak kaydedilmiştir.

İlk karşılaştırma sonuçlarına göre ResNet50 modeli, aynı veri kümesi ve aynı eğitim parametreleri altında eğitilen VGG16 modeline göre daha yüksek doğrulama hatası elde etmiştir. Bu durumun mimari farklılıklar, veri kümesinin özellikleri veya kullanılan hiperparametrelerin ResNet50 modeli için en uygun değerler olmamasından kaynaklanabileceği değerlendirilmiştir.

## Gün Sonu Değerlendirmesi

Bugün proje kapsamında geliştirilen ResNet50 tabanlı ikinci baseline modelinin ilk tam eğitimi başarıyla tamamlanmıştır.

Model eğitim süreci boyunca kararlı bir öğrenme davranışı sergilemiş, en iyi modeli otomatik olarak kaydetmiş ve tüm deney çıktıları başarıyla oluşturulmuştur.

İlk karşılaştırma sonuçlarına göre mevcut deney koşullarında VGG16 modeli daha düşük doğrulama hatası elde etmiştir. Bununla birlikte ResNet50 modeli başarıyla eğitilmiş ve proje kapsamında planlanan karşılaştırmalı analizler için ikinci temel model hazır hâle getirilmiştir.

## Oluşturulan Dosyalar

- `results/checkpoints/resnet50_baseline_best.pth`
- `results/plots/resnet50_loss_curve.png`
- `results/logs/resnet50_initial_training_log.md`
- `results/experiment_log.xlsx`

## Sonraki Adım

ResNet50 modelinin bağımsız test kümesi üzerindeki performansı değerlendirilecek, elde edilen Test MAE değeri VGG16 modeli ile karşılaştırılacak ve iki modelin sonuçları ayrıntılı olarak analiz edilecektir. Daha sonra araştırma önerisinde planlanan Dikkat Mekanizması (Attention Mechanism) entegrasyonu gerçekleştirilerek performans iyileştirme çalışmaları başlatılacaktır.

---

# Day 13 — ResNet50 Model Değerlendirmesi ve Baseline Analizi

## Amaç

Bugünkü çalışmanın amacı, eğitilmiş ResNet50 baseline modelini bağımsız test veri kümesi üzerinde değerlendirmek ve modelin test performansını eğitim sırasında elde edilen doğrulama (validation) sonuçlarıyla karşılaştırmaktı.

Ayrıca gelecekte geliştirilecek modellerin aynı deneysel prosedür kullanılarak değerlendirilebilmesini sağlamak amacıyla ResNet50 için değerlendirme (evaluation) pipeline'ı tamamlandı.

---

## Evaluation Pipeline Geliştirilmesi

ResNet50 baseline modeli için özel bir değerlendirme modülü (`evaluation_resnet50.py`) geliştirildi.

Evaluation pipeline, eğitim kodundan bağımsız olacak şekilde tasarlandı ve aşağıdaki işlemleri otomatik olarak gerçekleştirecek biçimde yapılandırıldı:

- En iyi performansa sahip checkpoint'in yüklenmesi
- Bağımsız test veri kümesinin değerlendirilmesi
- Mean Absolute Error (MAE) değerinin hesaplanması
- Tahmin sonuçlarının CSV formatında dışa aktarılması
- Değerlendirme özetinin JSON formatında oluşturulması
- Actual vs Predicted tahmin grafiğinin oluşturulması
- Tahmin hatası histogramının oluşturulması
- İnsan tarafından okunabilir Markdown değerlendirme raporunun üretilmesi

Değerlendirme prosedürü, VGG16 baseline modeli için daha önce kullanılan metodolojiyle aynı şekilde uygulanarak iki model arasında adil bir karşılaştırma yapılması amaçlandı.

---

## Checkpoint Doğrulaması

Değerlendirme işlemine başlamadan önce çeşitli doğrulama kontrolleri gerçekleştirildi.

ResNet50 checkpoint'i başarıyla yüklendi ve checkpoint içerisinde saklanan metadata bilgileri doğrulandı.

Aşağıdaki bilgiler kontrol edildi:

- En iyi checkpoint epoch'u: **20**
- Validation MAE: **121.8414 m**

Evaluation script'inin eğitilmiş model parametrelerini doğru biçimde geri yüklediği doğrulandı.

---

## Bağımsız Test Değerlendirmesi

Eğitilmiş model, daha önce model tarafından görülmemiş **112 görüntüden** oluşan bağımsız test veri kümesi üzerinde değerlendirildi.

Elde edilen sonuçlar aşağıdaki gibidir:

| Metrik | Sonuç |
| --- | ---: |
| Test Örneği Sayısı | **112** |
| Test MAE | **124.6181 m** |
| Validation MAE | **121.8414 m** |
| Mean Signed Error | **−77.3460 m** |

Validation MAE ile Test MAE arasındaki fark yalnızca **2.78 metre** olarak hesaplandı.

Bu sonuç, eğitilen modelin daha önce görmediği sahneler üzerinde önemli bir performans kaybı yaşamadan benzer bir performans gösterdiğini ortaya koymaktadır.

---

## Oluşturulan Çıktılar

Evaluation pipeline çalıştırıldığında aşağıdaki çıktılar otomatik olarak oluşturuldu:

- `resnet50_test_predictions.csv`
- `resnet50_evaluation_summary.json`
- `resnet50_actual_vs_predicted.png`
- `resnet50_prediction_error_histogram.png`
- `resnet50_evaluation_report.md`

Bu dosyalar model performansının hem sayısal hem de görsel olarak incelenebilmesini sağlamaktadır.

Oluşturulan çıktılar ilerleyen aşamada gerçekleştirilecek karşılaştırmalı model analizinde kullanılacaktır.

---

## Deneysel Gözlemler

ResNet50 baseline modeli tüm değerlendirme sürecini başarıyla tamamladı.

Modelin tahmin hatası daha önce geliştirilen VGG16 baseline modelinden yüksek olmasına rağmen değerlendirme sırasında kararlı bir performans gösterdiği gözlemlendi.

Validation ve test performanslarının birbirine yakın olması, modelin bağımsız test veri kümesinde önemli bir performans düşüşü yaşamadığını göstermektedir.

Elde edilen sonuçlar, ResNet50 baseline modelinin resmi referans performansını oluşturmaktadır ve ilerleyen Attention Mechanism deneylerinde yapılacak karşılaştırmalar için kullanılacaktır.

---

## Gün Sonu Sonucu

Bugünkü çalışmalar sonucunda ResNet50 baseline modelinin tüm deneysel süreci tamamlandı.

Bu aşamada hem VGG16 hem de ResNet50 baseline modelleri aynı deneysel koşullar altında başarıyla:

- geliştirildi,
- eğitildi,
- değerlendirildi,
- sonuçları kaydedildi,
- dokümante edildi.

Bir sonraki aşamada iki baseline modelin ayrıntılı performans karşılaştırması gerçekleştirilecek ve elde edilen sonuçlara göre Attention Mechanism entegrasyonunda kullanılacak temel mimari belirlenecektir.


# Day 14 — ResNet50 Değerlendirme Grafikleri ve Hata Analizi

## Amaç

Bugünkü çalışmanın amacı, ResNet50 baseline modelinin performansını yalnızca genel MAE değeri üzerinden değil, eğitim ve değerlendirme sürecinde oluşturulan grafikler üzerinden ayrıntılı biçimde analiz etmekti.

Bu kapsamda ResNet50 modelinin öğrenme eğrisi, Actual vs Predicted grafiği ve tahmin hatası histogramı incelendi.

Analiz sırasında özellikle aşağıdaki sorulara odaklanıldı:

- Modelde belirgin bir overfitting davranışı bulunuyor mu?
- Training ve validation performansları eğitim boyunca nasıl değişiyor?
- Model farklı görüş mesafelerinde benzer tahmin davranışı gösteriyor mu?
- Tahminlerde sistematik bir düşük veya yüksek tahmin eğilimi bulunuyor mu?
- Test MAE değerinin yükselmesine hangi hata davranışları katkıda bulunuyor?

---

## Learning Curve Analizi

ResNet50 modelinin 20 epoch boyunca elde edilen Training MAE ve Validation MAE değerleri incelendi.

Eğitim sürecinde her iki hata değerinin de düzenli biçimde azaldığı görüldü.

Temel sonuçlar aşağıdaki gibidir:

| Metrik | Başlangıç | Son |
| --- | ---: | ---: |
| Training MAE | **271.6411 m** | **122.1239 m** |
| Validation MAE | **269.8412 m** | **121.8414 m** |

Eğitimin özellikle ilerleyen epoch'larında training ve validation eğrilerinin birbirine oldukça yakın ilerlediği gözlemlendi.

20. epoch sonunda Training MAE ile Validation MAE arasındaki fark yaklaşık **0.28 m** olarak hesaplandı.

Validation MAE eğitim boyunca genel olarak azalmaya devam etti ve en iyi validation sonucu **20. epoch'ta** elde edildi.

Bu davranış, training performansı iyileşmeye devam ederken validation performansının kötüleşmesi şeklinde ortaya çıkan klasik overfitting davranışının mevcut deneyde görülmediğini göstermektedir.

---

## Overfitting Analizi

Overfitting değerlendirmesi yalnızca learning curve üzerinden değil, training, validation ve bağımsız test sonuçları birlikte ele alınarak gerçekleştirildi.

Elde edilen değerler:

| Metrik | Sonuç |
| --- | ---: |
| Final Training MAE | **122.1239 m** |
| Best Validation MAE | **121.8414 m** |
| Test MAE | **124.6181 m** |
| Validation–Test MAE Farkı | **2.7767 m** |

Training ve validation performanslarının birbirine oldukça yakın olması ve bağımsız Test MAE değerinin Validation MAE değerinden yalnızca yaklaşık **2.78 m** yüksek olması, mevcut baseline deneyinde belirgin bir overfitting bulgusu olmadığını desteklemektedir.

Bununla birlikte learning curve incelendiğinde Validation MAE değerinin 20. epoch'ta hâlâ düşmeye devam ettiği görülmektedir.

Bu durum, ResNet50 modelinin belirlenen 20 epoch sonunda tamamen yakınsamamış olabileceğini düşündürmektedir.

Ancak VGG16 ve ResNet50 baseline deneylerinin aynı deneysel koşullar altında karşılaştırılabilmesi amacıyla ResNet50 modeli bu aşamada daha uzun süre yeniden eğitilmeyecektir.

Daha uzun eğitim süresinin etkisi ileride incelenirse bu çalışma mevcut baseline deneyinden ayrı bir deney olarak kaydedilecektir.

---

## Actual vs Predicted Grafiğinin Analizi

Modelin farklı görüş mesafelerindeki tahmin davranışını incelemek amacıyla `resnet50_actual_vs_predicted.png` grafiği analiz edildi.

Grafikteki kesikli diyagonal çizgi ideal tahmin durumunu temsil etmektedir:

```text
Predicted Visibility = Ground Truth Visibility
```

Düşük ve orta görüş mesafelerinde, özellikle yaklaşık **50–200 m** aralığında, tahminlerin önemli bir bölümünün ideal çizgiye görece yakın olduğu gözlemlendi.

Ancak ground-truth görüş mesafesi yükseldikçe model tahminlerinin ideal çizginin altında kalmaya başladığı görüldü.

Bu davranış özellikle **500 m** ve **800 m** görüş mesafesine sahip örneklerde belirginleşmektedir.

500 m ground-truth değerine sahip görüntülerde tahminlerin önemli bir bölümü gerçek değerin oldukça altında kalırken, 800 m ground-truth değerine sahip örneklerde model tahminlerinin yaklaşık **200–360 m** aralığında kaldığı gözlemlendi.

Bu sonuç, ResNet50 modelinin özellikle yüksek görüş mesafelerinde sistematik bir **underestimation (düşük tahmin)** davranışı gösterdiğini ortaya koymaktadır.

---

## Prediction Range Compression Gözlemi

Actual vs Predicted grafiğinde dikkat çeken diğer bir davranış tahmin aralığının daralmasıdır.

Ground-truth değerleri yaklaşık **50–800 m** arasında değişirken model tahminlerinin büyük bölümü bundan çok daha dar bir aralıkta kalmaktadır.

Model özellikle yüksek görüş mesafelerini hedef değişkenin gerçek dinamik aralığına kadar taşıyamamaktadır.

Bu davranış, modelin çıktı değerlerinin daha dar bir bölgede toplanması anlamına gelen **prediction-range compression** olarak değerlendirildi.

Bu gözlem, yüksek görüş mesafelerinde oluşan büyük tahmin hatalarının önemli bir göstergesidir.

---

## Prediction Error Histogram Analizi

Modelin tahmin hatalarının dağılımını incelemek amacıyla `resnet50_prediction_error_histogram.png` grafiği analiz edildi.

Hata aşağıdaki şekilde tanımlanmaktadır:

```text
Prediction Error = Predicted Visibility - Ground Truth Visibility
```

Bu nedenle:

- `0 m` → ideal tahmin,
- negatif değer → gerçek değerden düşük tahmin,
- pozitif değer → gerçek değerden yüksek tahmin

anlamına gelmektedir.

Histogram incelendiğinde test örneklerinin önemli bir bölümünün sıfır hata çevresinde ve görece düşük hata aralıklarında toplandığı görüldü.

Bununla birlikte dağılımın negatif yönde oldukça uzun bir kuyruğa sahip olduğu gözlemlendi.

Bazı tahmin hataları yaklaşık **−600 m** seviyesine kadar ulaşırken pozitif tarafta benzer büyüklükte bir hata kuyruğu bulunmamaktadır.

Bu nedenle hata dağılımının belirgin biçimde asimetrik olduğu görüldü.

---

## Mean Signed Error ile İlişki

Evaluation aşamasında ResNet50 için hesaplanan Mean Signed Error değeri:

**−77.3460 m**

olarak elde edilmişti.

Actual vs Predicted grafiği ve hata histogramı birlikte değerlendirildiğinde bu negatif değerin nedeni daha açık biçimde görülmektedir.

Modelin hataları yalnızca ground-truth değerlerinin çevresinde rastgele dağılmamaktadır.

Özellikle yüksek görüş mesafesine sahip bazı örneklerde model çok büyük negatif tahmin hataları üretmektedir.

Bu durum hata dağılımını negatif yönde kaydırmakta ve Mean Signed Error değerinin negatif olmasına katkıda bulunmaktadır.

Evaluation sırasında hesaplanan **602.6687 m maksimum mutlak hata** değeri de histogramda gözlemlenen yaklaşık −600 m seviyesindeki büyük negatif hata kuyruğuyla uyumludur.

---

## Birleşik Değerlendirme

Learning curve, Actual vs Predicted grafiği ve Prediction Error Histogram birlikte değerlendirildiğinde ResNet50 baseline modelinin davranışı daha ayrıntılı biçimde ortaya çıkmaktadır.

Learning curve:

- Eğitim sürecinin kararlı ilerlediğini,
- Training ve Validation MAE değerlerinin birlikte azaldığını,
- Belirgin bir training-validation ayrışması bulunmadığını

göstermektedir.

Actual vs Predicted grafiği:

- Düşük ve orta görüş mesafelerinde daha başarılı tahminler üretildiğini,
- Yüksek görüş mesafelerinde sistematik underestimation oluştuğunu,
- Tahmin aralığının gerçek hedef aralığına kıyasla sıkıştığını

göstermektedir.

Prediction Error Histogram ise:

- Hataların önemli bir bölümünün düşük hata bölgelerinde toplandığını,
- Bununla birlikte büyük negatif hataların bulunduğunu,
- Hata dağılımının negatif yönde uzun bir kuyruğa sahip olduğunu

göstermektedir.

Bu sonuçlar birlikte değerlendirildiğinde ResNet50 baseline modelinin temel sınırlılığının klasik overfitting olmadığı görülmektedir.

Mevcut baseline konfigürasyonunda temel problem, modelin özellikle yüksek görüş mesafelerini yeterli doğrulukla temsil edememesi, bu örneklerde sistematik olarak düşük tahmin üretmesi ve tahmin aralığının sıkışmasıdır.

---

## Bulguların Yorumlanmasında Dikkat Edilecek Nokta

Mevcut grafikler model davranışının nasıl gerçekleştiğini göstermesine rağmen bu davranışın kesin nedenini tek başına açıklamamaktadır.

Örneğin;

- hedef değer dağılımı,
- frozen backbone kullanımı,
- eğitim süresi,
- model mimarisinin özellikleri

gibi faktörler bu davranış üzerinde etkili olabilir.

Ancak mevcut deneyler bu olası nedenleri birbirinden ayıracak şekilde tasarlanmadığından bunlar kesin sonuç olarak değil, ileride araştırılabilecek hipotezler olarak değerlendirilecektir.

---

## Deneysel Karar

ResNet50 modelinin Validation MAE değeri 20. epoch'ta hâlâ iyileşiyor olmasına rağmen mevcut baseline model daha uzun epoch sayısı ile yeniden eğitilmeyecektir.

VGG16 ve ResNet50 modelleri;

- aynı veri bölünmesi,
- aynı preprocessing pipeline,
- aynı random seed,
- aynı eğitim süresi,
- aynı temel hiperparametreler,
- aynı evaluation prosedürü

altında değerlendirilmiştir.

Bu deneysel koşulların korunması, iki baseline mimarinin adil biçimde karşılaştırılması açısından önemlidir.

Daha uzun eğitim süresinin ResNet50 performansına etkisi araştırılacaksa bu çalışma ayrı bir deney olarak gerçekleştirilecektir.

---

## Gün Sonu Sonucu

Bugünkü çalışmalar sonucunda ResNet50 baseline modelinin görsel ve davranışsal performans analizi tamamlandı.

Elde edilen temel bulgular:

- Belirgin bir overfitting davranışı gözlenmedi.
- Training ve Validation MAE değerleri eğitim boyunca düzenli biçimde azaldı.
- Validation ve Test MAE değerleri birbirine yakın bulundu.
- Yüksek görüş mesafelerinde sistematik underestimation tespit edildi.
- Modelde prediction-range compression davranışı gözlemlendi.
- Hata dağılımında negatif yönde uzun bir kuyruk bulundu.
- **−77.3460 m Mean Signed Error** değeri görsel analizlerle uyumlu bulundu.
- Maksimum mutlak hata **602.6687 m** olarak kaydedildi.
- Modelin 20 epoch sonunda tamamen yakınsamamış olması mümkün görülmesine rağmen baseline karşılaştırmasının adil olması amacıyla mevcut eğitim konfigürasyonunun korunmasına karar verildi.

Bu analizler, sonraki aşamada gerçekleştirilecek VGG16–ResNet50 karşılaştırmasında ve Attention Mechanism entegrasyonu için temel mimarinin seçiminde kullanılacaktır.

# Day 15 — VGG16 ve ResNet50 Baseline Karşılaştırması

## Amaç

Bugünkü çalışmanın amacı, proje kapsamında geliştirilen VGG16 ve ResNet50 baseline modellerinin performanslarını karşılaştırmak ve mevcut sentetik veri aşamasında Attention Mechanism entegrasyonu için kullanılacak en başarılı temel mimariyi belirlemekti.

---

## Baseline Sonuçlarının Karşılaştırılması

Karşılaştırmaya başlamadan önce her iki modele ait sonuçlar doğrudan evaluation JSON dosyalarından doğrulandı.

Elde edilen temel sonuçlar:

| Metrik | VGG16 | ResNet50 |
| --- | ---: | ---: |
| Validation MAE | **69.9705 m** | 121.8414 m |
| Test MAE | **66.7227 m** | 124.6181 m |
| Mean Signed Error | **−17.3877 m** | −77.3460 m |
| Maximum Absolute Error | **392.8829 m** | 602.6687 m |

VGG16 ve ResNet50 arasındaki Validation MAE farkı **51.8709 m**, Test MAE farkı ise **57.8954 m** olarak hesaplandı.

VGG16, ResNet50 baseline sonucuna kıyasla Test MAE'de yaklaşık **%46.46 azalma** sağladı.

---

## Hata Davranışlarının Değerlendirilmesi

Her iki modelde de negatif Mean Signed Error gözlenmesi, gerçek görüş mesafesini ortalama olarak olduğundan düşük tahmin etme eğilimi bulunduğunu gösterdi.

Ancak bu davranış ResNet50 modelinde daha belirgindi.

Day 14 kapsamında incelenen değerlendirme grafiklerinde de ResNet50'nin özellikle yüksek görüş mesafelerinde sistematik underestimation ve prediction-range compression davranışı gösterdiği gözlenmişti.

Bu görsel bulgular bugünkü sayısal karşılaştırma sonuçlarıyla tutarlı bulundu.

---

## Araştırma Hipotezinin Değerlendirilmesi

Projenin başlangıç hipotezinde ResNet50'nin residual learning yapısı ve daha derin mimarisi nedeniyle VGG16'ya kıyasla daha düşük MAE üretmesi bekleniyordu.

Ancak mevcut FRIDA/FRIDA2 kaynaklı sentetik veri üzerinde gerçekleştirilen deneyler bu hipotezi desteklemedi.

Bu sonuç ResNet50'nin genel olarak daha kötü bir mimari olduğu anlamına gelmemektedir. Elde edilen sonuç yalnızca mevcut veri kümesi, frozen backbone transfer learning yaklaşımı ve kullanılan eğitim koşulları kapsamında değerlendirilmiştir.

---

## Baseline Model Seçimi

Bağımsız test kümesindeki MAE temel seçim kriteri olarak kullanıldı.

VGG16 **66.7227 m Test MAE**, ResNet50 ise **124.6181 m Test MAE** elde etti.

Bu nedenle **VGG16, mevcut FRIDA/FRIDA2 kaynaklı sentetik veri aşamasında Attention Mechanism entegrasyonu için kullanılacak en başarılı baseline mimarisi olarak seçildi.**

Bu karar projenin nihai gerçek dünya model seçimi değildir. FVEI/FHVI veya uygun alternatif gerçek dünya verileriyle gerçekleştirilecek sonraki fine-tuning ve değerlendirme aşamalarında modelin gerçek dünya genelleme performansı ayrıca incelenecektir.

---

## Günlük Çıktı

Baseline karşılaştırmasının ayrıntılı sonuçlarını belgelemek amacıyla:

`baseline_comparison.md`

dosyası oluşturuldu.

Dosyada ortak deney koşulları, Validation ve Test MAE karşılaştırmaları, hata davranışları, hipotez değerlendirmesi ve baseline seçim kararı dokümante edildi.

---

## Gün Sonu Sonucu

Day 15 sonunda VGG16 ve ResNet50 baseline karşılaştırması tamamlandı.

**Selected Synthetic Baseline: VGG16**

**VGG16 Test MAE: 66.7227 m**

**ResNet50 Test MAE: 124.6181 m**

Başlangıç hipotezinin aksine VGG16 mevcut sentetik deney koşullarında daha başarılı sonuç verdi ve Attention Mechanism aşamasında kullanılacak temel mimari olarak seçildi.

Proje böylece baseline model karşılaştırma aşamasını tamamlayarak Attention Mechanism geliştirme aşamasına geçmeye hazır hâle geldi.


# Day 16 — CBAM Attention Mekanizmasının VGG16 Mimarisine Entegrasyonu

## Amaç

Bugünkü çalışmanın amacı, Day 15 kapsamında sentetik veri üzerinde en başarılı baseline model olarak seçilen VGG16 mimarisine Attention Mechanism entegre etmek ve yeni modelin eğitim öncesi teknik doğrulamalarını gerçekleştirmekti.

Attention yaklaşımı olarak Channel Attention ve Spatial Attention bileşenlerini birlikte kullanan CBAM (Convolutional Block Attention Module) seçildi.

---

## Attention Mekanizması Seçimi

CNN tabanlı attention yaklaşımları incelendi ve SE ile CBAM yöntemleri karşılaştırıldı.

SE temel olarak channel attention uygularken CBAM:

- Channel Attention
- Spatial Attention

bileşenlerini ardışık biçimde kullanmaktadır.

Görüş mesafesi tahmininde hem hangi feature channel'larının hem de görüntünün hangi uzamsal bölgelerinin önemli olabileceği değerlendirildiğinden CBAM kullanılmasına karar verildi.

CBAM'ın performansı artıracağı önceden varsayılmadı; katkısının sonraki eğitim ve bağımsız test değerlendirmesi sonucunda ölçülmesine karar verildi.

---

## VGG16 Entegrasyon Tasarımı

CBAM, VGG16'nın son convolutional feature map'inden sonra ve final MaxPool katmanından önce konumlandırıldı.

224 × 224 giriş görüntüsü için attention giriş boyutu:

`[B, 512, 14, 14]`

olarak belirlendi.

Genel mimari:

Input Image → Frozen VGG16 Feature Extractor → CBAM (Channel Attention + Spatial Attention) → Final MaxPool → Regression Head → Visibility Prediction

Regression head, baseline VGG16 ile kontrollü karşılaştırma yapılabilmesi amacıyla değiştirilmeden korundu.

---

## CBAM Implementasyonu

`src/models/attention.py` dosyasında aşağıdaki modüller geliştirildi:

- `ChannelAttention`
- `SpatialAttention`
- `CBAM`

Channel Attention için Average Pooling ve Max Pooling birlikte kullanıldı. Reduction Ratio değeri **16** olarak belirlendi ve channel dönüşümü **512 → 32 → 512** şeklinde yapılandırıldı.

Spatial Attention için channel-wise average projection ve maximum projection birlikte kullanıldı. Birleştirilen feature map üzerinde **7 × 7 convolution** ve sigmoid aktivasyonu uygulandı.

CBAM'ın feature map boyutunu değiştirmediği yapılan shape testi ile doğrulandı:

`[2, 512, 14, 14] → [2, 512, 14, 14]`

---

## Attention-Enhanced VGG16 Modeli

`src/models/vgg16_attention.py` dosyası oluşturularak CBAM mekanizması VGG16 regresyon mimarisine entegre edildi.

Model üzerinde gerçekleştirilen forward-pass testinde:

`[2, 3, 224, 224] → [2, 1]`

sonucu elde edildi.

Böylece modelin sürekli görüş mesafesi regresyonu için beklenen tek çıkış değerini doğru biçimde ürettiği doğrulandı.

---

## Trainable ve Frozen Parametre Kontrolü

Transfer learning stratejisinin doğru uygulanıp uygulanmadığı ayrıca kontrol edildi.

Elde edilen parametre değerleri:

| Parametre Grubu | Sayı |
| --- | ---: |
| Total Parameters | **27,658,915** |
| Frozen Parameters | **14,714,688** |
| Trainable Parameters | **12,944,227** |
| CBAM Trainable Parameters | **32,866** |
| Regression Head Trainable Parameters | **12,911,361** |

Ayrıca yapılan doğrudan kontrolde:

- Feature extractor trainable: **False**
- CBAM trainable: **True**
- Regression head trainable: **True**

sonuçları elde edildi.

Böylece pretrained VGG16 feature extractor'ın dondurulduğu, yalnızca CBAM ve regression head parametrelerinin eğitilebilir durumda olduğu doğrulandı.

---

## Training Pipeline Hazırlığı

Attention modeli için ayrı bir `train_vgg16_attention.py` training pipeline'ı oluşturuldu.

Baseline karşılaştırmasının kontrollü kalması amacıyla temel deney ayarları korundu:

- Image Size: **224 × 224**
- Batch Size: **16**
- Epoch: **20**
- Optimizer: **Adam**
- Learning Rate: **1e-4**
- Weight Decay: **1e-5**
- Loss Function: **L1Loss / MAE**
- Random Seed: **42**
- Frozen Backbone: **True**

Attention modeli için ayrı bir `vgg16_attention_best.pth` checkpoint yolu tanımlandı.

Training script üzerinde syntax ve import testleri başarıyla tamamlandı.

Gerçek DataLoader batch'i ile gerçekleştirilen uyumluluk testinde:

- Images: `[16, 3, 224, 224]`
- Targets: `[16]`
- Outputs: `[16, 1]`

boyutları elde edildi.

Bu sonuç, mevcut veri pipeline'ının yeni Attention-enhanced VGG16 modeliyle uyumlu olduğunu doğruladı.

---

## Dokümantasyon

Attention mimarisi ve alınan teknik kararları belgelemek amacıyla `attention_architecture_notes.md` dosyası oluşturuldu.

Bu dokümanda CBAM seçim gerekçesi, Channel ve Spatial Attention yapıları, VGG16 entegrasyon noktası, parameter freeze stratejisi ve gerçekleştirilen teknik doğrulamalar kayıt altına alındı.

---

## Gün Sonu Sonucu

Day 16 sonunda VGG16 + CBAM attention mimarisinin tasarımı ve ilk implementasyonu tamamlandı.

CBAM mekanizması geliştirildi, VGG16 mimarisine entegre edildi, forward-pass ve tensor shape testleri başarıyla tamamlandı, frozen/trainable parametre yapısı doğrulandı, training pipeline hazırlandı ve DataLoader uyumluluğu test edildi.

Henüz Attention modelinin tam 20 epoch eğitimi gerçekleştirilmedi.

Bir sonraki aşamada VGG16 + CBAM modeli mevcut sentetik veri kümesi ve baseline deneyleriyle aynı temel koşullar altında eğitilecek, en başarılı checkpoint Validation MAE değerine göre seçilecek ve bağımsız test performansı mevcut **66.7227 m VGG16 baseline Test MAE** referansı ile karşılaştırılacaktır.

## Day 17 — VGG16 + CBAM Eğitimi

VGG16 baseline üzerinde tasarlanan CBAM attention mimarisinin 20 epoch eğitim süreci tamamlandı. Karşılaştırmanın adil olması amacıyla baseline deneyleriyle aynı scene-based veri bölünmesi ve temel eğitim ayarları korundu.

### Eğitim Yapılandırması

- Eğitim örneği: 464
- Validation örneği: 96
- Batch size: 16
- Epoch: 20
- Optimizer: Adam
- Learning rate: 1e-4
- Loss: L1Loss (MAE)
- Random seed: 42
- Backbone: Frozen
- CBAM reduction ratio: 16
- CBAM spatial kernel: 7

Model toplam 27,658,915 parametre içerirken 12,944,227 parametre eğitilebilir durumda tutuldu.

### Sonuç

En iyi checkpoint epoch 17'de elde edildi:

- Best epoch: 17
- Best validation MAE: **69.3274 m**
- Epoch 17 train MAE: **47.8197 m**

Epoch 17 sonrasında training MAE düşmeye devam ederken validation MAE dalgalanmaya başladı. Epoch 20'de training MAE 41.0328 m'ye düşmesine rağmen validation MAE 76.0531 m olarak ölçüldü. Bu nedenle bağımsız test değerlendirmesinde epoch 17 checkpoint'i kullanılmasına karar verildi.

VGG16 baseline'ın en iyi validation MAE değeri 69.9705 m iken VGG16 + CBAM 69.3274 m elde etti. Attention modeli validation aşamasında yaklaşık 0.6431 m daha düşük MAE üretmiş olsa da CBAM'ın gerçek katkısı hakkında karar vermek için bağımsız test sonucu beklenmiştir.

---

## Day 18 — VGG16 + CBAM Test Değerlendirmesi

VGG16 + CBAM modelinin epoch 17'de kaydedilen en iyi checkpoint'i, baseline modellerle aynı 112 örnekten oluşan bağımsız scene-based test kümesi üzerinde değerlendirildi.

Değerlendirme için `src/evaluation/evaluation_vgg16_attention.py` oluşturuldu. Script; tahmin sonuçlarını, özet metrikleri, Actual vs Predicted grafiğini, hata histogramını ve Markdown değerlendirme raporunu üretmektedir.

### Test Sonuçları

- Test samples: 112
- Test MAE: **67.6214 m**
- Mean signed error: **-10.8501 m**
- Minimum absolute error: **0.4317 m**
- Maximum absolute error: **439.5097 m**

### VGG16 Baseline ile Karşılaştırma

| Metric | VGG16 | VGG16 + CBAM |
|---|---:|---:|
| Best Validation MAE (m) | 69.9705 | **69.3274** |
| Test MAE (m) | **66.7227** | 67.6214 |
| Mean Signed Error (m) | -17.3877 | **-10.8501** |
| Maximum Absolute Error (m) | **392.8829** | 439.5097 |

CBAM validation MAE değerini küçük ölçüde iyileştirmiş olsa da bu kazanım bağımsız test kümesine yansımadı. VGG16 baseline test MAE değeri 66.7227 m, VGG16 + CBAM test MAE değeri ise 67.6214 m oldu. Test MAE farkı yaklaşık 0.8987 m olarak hesaplandı.

CBAM modelinin mean signed error değerinin -17.3877 m'den -10.8501 m'ye yaklaşması ortalama düşük tahmin eğiliminin azaldığını gösterirken, maksimum mutlak hatanın 392.8829 m'den 439.5097 m'ye yükseldiği gözlendi.

Mevcut tek deney ve random seed üzerinden farkların istatistiksel anlamlılığı hakkında çıkarım yapılmadı.

### Araştırma Kararı

CBAM attention mekanizması teknik olarak başarıyla entegre edilmiş ve kontrollü koşullarda değerlendirilmiştir. Ancak mevcut sentetik FRIDA/FRIDA2 deneylerinde genel test MAE açısından VGG16 baseline üzerinde performans artışı sağlamamıştır.

Bu nedenle mevcut sentetik aşamadaki model sıralaması:

1. **VGG16 Baseline — 66.7227 m**
2. **VGG16 + CBAM — 67.6214 m**
3. **ResNet50 Baseline — 124.6181 m**

Attention mekanizmasının performansı artıracağı hipotezi mevcut sentetik test sonuçları tarafından desteklenmemiştir. Mevcut sentetik aşamada en iyi model olarak VGG16 baseline korunmuştur.

Ayrıntılı attention karşılaştırması `docs/reports/attention_comparison.md` dosyasında dokümante edilmiştir.

### Üretilen Çıktılar

- `src/evaluation/evaluation_vgg16_attention.py`
- `results/evaluation/vgg16_attention_test_predictions.csv`
- `results/evaluation/vgg16_attention_evaluation_summary.json`
- `results/plots/vgg16_attention_actual_vs_predicted.png`
- `results/plots/vgg16_attention_prediction_error_histogram.png`
- `results/logs/vgg16_attention_evaluation_report.md`
- `docs/reports/attention_comparison.md`


## Gün 19 — SE-Net Risk Yönetimi Deneyi ve Nihai Sentetik Attention Karşılaştırması

### Amaç

Kabul edilen TÜBİTAK 2209-A proje önerisinde, seçilen attention mekanizmasının model performansını iyileştirmemesi durumunda daha basit ve kanal odaklı bir alternatif olarak Squeeze-and-Excitation (SE-Net) mekanizmasının denenmesi risk yönetimi planında belirtilmişti.

Önceki VGG16 + CBAM deneyinde validation MAE değerinde küçük bir iyileşme elde edilmesine rağmen test MAE değeri VGG16 baseline modelinden daha kötü sonuç verdi. Bu nedenle proje önerisinde belirtilen alternatif plan uygulanarak SE-Net tabanlı VGG16 modeli geliştirildi ve aynı deney koşullarında değerlendirildi.

### SE-Net Entegrasyonu

VGG16 mimarisine kanal bazlı özellik yeniden ağırlıklandırması yapan bir Squeeze-and-Excitation bloğu eklendi.

Entegrasyon sırası:

VGG16 feature extractor  
→ SE bloğu  
→ final MaxPool  
→ VGG16 avgpool  
→ regression head

SE bloğu, VGG16'nın son convolution bloğundan sonra ve final MaxPool işleminden önce konumlandırıldı. Bu konum daha önce CBAM için kullanılan entegrasyon noktasıyla aynı tutularak iki attention mekanizmasının mümkün olduğunca eşit mimari koşullar altında karşılaştırılması sağlandı.

Deney konfigürasyonu:

- SE reduction ratio: 16
- ImageNet pretrained VGG16
- VGG16 backbone: frozen
- SE bloğu: trainable
- Regression head: trainable
- Baseline VGG16 ile aynı regression head
- Aynı training, validation ve test bölünmesi
- Random seed: 42
- Aynı optimizer
- Aynı learning rate
- Aynı weight decay
- Aynı batch size
- Aynı 20 epoch eğitim bütçesi

Parametre sayıları:

- Toplam parametre: 27,658,817
- Eğitilebilir parametre: 12,944,129
- Dondurulmuş parametre: 14,714,688
- SE parametreleri: 32,768
- Regression head parametreleri: 12,911,361

### Eğitim Sonuçları

Model toplam 20 epoch boyunca eğitildi.

En iyi checkpoint:

- En iyi epoch: 19
- En iyi validation MAE: 70.6083 m

20. epoch sonuçları:

- Training MAE: 50.1878 m
- Validation MAE: 70.7658 m

Validation MAE değeri 19. epoch'a kadar düzenli olarak azaldı. 20. epoch'ta küçük bir artış meydana geldiği için epoch 19'da kaydedilen checkpoint en iyi model olarak korundu.

### Bağımsız Test Değerlendirmesi

En iyi SE checkpoint'i, önceki modellerde kullanılan ve değiştirilmemiş olan 112 görüntülük scene-based test seti üzerinde değerlendirildi.

Test sonuçları:

- Test örneği: 112
- Test MAE: 72.4412 m
- Ortalama signed error: -12.9774 m
- Minimum absolute error: 0.1255 m
- Maximum absolute error: 423.1353 m

Negatif ortalama signed error değeri, modelin gerçek görüş mesafesini ortalama olarak düşük tahmin etme eğiliminin devam ettiğini göstermektedir.

### Nihai Sentetik Model Karşılaştırması

| Model | En İyi Validation MAE | Test MAE |
|---|---:|---:|
| VGG16 baseline | 69.9705 m | **66.7227 m** |
| VGG16 + CBAM | **69.3274 m** | 67.6214 m |
| VGG16 + SE | 70.6083 m | 72.4412 m |
| ResNet50 baseline | 121.8414 m | 124.6181 m |

SE modeli, VGG16 baseline modeline göre test MAE açısından 5.7185 m daha yüksek hata üretmiştir. Bu değer yaklaşık %8.57 daha yüksek test hatasına karşılık gelmektedir.

SE modeli ayrıca VGG16 + CBAM modelinden 4.8198 m daha yüksek test MAE üretmiştir.

### Bulguların Yorumlanması

Mevcut sentetik FRIDA/FRIDA2 deney düzeninde ne CBAM ne de SE mekanizması, temel VGG16 modelinin birincil model seçim metriği olan test MAE performansını iyileştirebilmiştir.

CBAM modeli 69.3274 m ile en düşük validation MAE değerini üretmiş ancak bu iyileşme bağımsız test setine aynı şekilde yansımamıştır. CBAM'ın test MAE değeri 67.6214 m ile baseline VGG16'nın 66.7227 m değerinden biraz daha yüksek kalmıştır.

SE modeli ise hem validation hem de test MAE açısından baseline VGG16'yı geçememiştir.

Bu nedenle mevcut sentetik deney aşamasında en başarılı mimari VGG16 baseline olarak kalmıştır.

### Risk Yönetimi Planının Sonucu

Kabul edilen TÜBİTAK proje önerisindeki attention mekanizmasına ilişkin risk yönetimi planı uygulanmıştır:

1. VGG16 üzerine CBAM attention mekanizması entegre edildi.
2. CBAM modeli aynı deney koşullarında eğitildi ve değerlendirildi.
3. CBAM test MAE açısından baseline VGG16'yı geçemedi.
4. Bunun üzerine proje önerisindeki alternatif plan doğrultusunda SE-Net uygulandı.
5. SE-Net aynı deney koşullarında eğitildi ve değerlendirildi.
6. SE-Net de test MAE açısından baseline VGG16'yı geçemedi.

Dolayısıyla attention mekanizmalarının mevcut sentetik deney düzeninde test MAE açısından avantaj sağladığı hipotezi desteklenmemiştir.

Mevcut karşılaştırmalar tek bir deterministic veri bölünmesi ve tek random seed üzerinden gerçekleştirildiği için sonuçlar hakkında istatistiksel anlamlılık iddiasında bulunulmamaktadır.

### Karar

Sentetik veri aşamasında seçilen model:

**VGG16 baseline — Test MAE: 66.7227 m**

Sentetik baseline karşılaştırması ve attention mekanizması deneyleri bu aşamayla tamamlanmıştır.

Projenin bir sonraki ana araştırma aşaması, kabul edilen TÜBİTAK 2209-A proje önerisinde belirtildiği şekilde gerçek dünya verileri üzerinde modelin genellenebilirliğinin incelenmesidir. Bu kapsamda FVEI/FHVI veri setlerinin erişilebilirliği değerlendirilecek, uygun gerçek dünya veri seti hazırlanacak ve seçilen model üzerinde gerçek dünya validation/fine-tuning deneylerine geçilecektir.