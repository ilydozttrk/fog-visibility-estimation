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