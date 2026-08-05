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