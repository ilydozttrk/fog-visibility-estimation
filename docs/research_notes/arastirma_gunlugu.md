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