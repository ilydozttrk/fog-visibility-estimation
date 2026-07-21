# Danışman Toplantı Notları

**Proje Adı:** Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Toplantı:** Hafta 2 Değerlendirme

**Tarih:** … / … / 2026

**Hazırlayan:** İlayda Öztürk

---

# 1. Toplantının Amacı

Bu toplantının amacı, proje kapsamında ilk iki haftada gerçekleştirilen çalışmaları sunmak, elde edilen ilk deneysel sonuçları değerlendirmek ve üçüncü hafta için planlanan çalışmalara ilişkin danışman görüşlerini almaktır.

---

# 2. Projenin Mevcut Durumu

Proje şu anda planlanan takvime uygun şekilde ilerlemektedir.

Tamamlanan ana aşamalar:

- Veri setinin incelenmesi
- Veri analizi
- Ön işleme (Preprocessing) pipeline'ı
- Scene-Based veri bölme stratejisi
- PyTorch DataLoader altyapısı
- VGG16 transfer öğrenme modeli
- Eğitim (Training) pipeline'ı
- Checkpoint sistemi
- Evaluation pipeline'ı
- Otomatik raporlama sistemi

Proje şu anda ikinci baseline model (ResNet50) geliştirme aşamasına geçmeye hazır durumdadır.

---

# 3. Veri Kümesi Özeti

Kullanılan veri kümesi:

**FRIDA + FRIDA2**

| Özellik | Değer |
|---------|------:|
| Toplam Sahne | 84 |
| Toplam Görüntü | 672 |
| Görüş Mesafesi Seviyesi | 8 |

Veri kümesi Scene-Based Split yöntemi kullanılarak bölünmüştür.

| Küme | Görüntü Sayısı |
|------|---------------:|
| Train | 464 |
| Validation | 96 |
| Test | 112 |

Bu yöntem ile aynı sahnenin farklı veri kümelerinde bulunması engellenmiş ve veri sızıntısı (data leakage) riski azaltılmıştır.

---

# 4. Tamamlanan Teknik Çalışmalar

## Veri Hazırlama

- Veri seti analiz edildi.
- Görüntüler doğrulandı.
- Ön işleme pipeline'ı geliştirildi.
- Normalizasyon işlemleri belirlendi.
- Veri yükleme altyapısı oluşturuldu.

---

## Model Geliştirme

İlk baseline model olarak VGG16 mimarisi kullanılmıştır.

Yapılan geliştirmeler:

- Transfer Learning
- Regression Head
- Training Pipeline
- Checkpoint Sistemi
- Evaluation Pipeline
- Otomatik Raporlama

---

# 5. İlk Deney Sonuçları

VGG16 modeli toplam 20 epoch boyunca eğitilmiştir.

Elde edilen sonuçlar aşağıdadır.

| Metrik | Sonuç |
|--------|------:|
| En Başarılı Epoch | 18 |
| Validation MAE | 69.9705 m |
| Test MAE | 66.7227 m |
| Mean Signed Error | -17.3877 m |

Test performansının doğrulama performansına yakın olması modelin daha önce görmediği sahneler üzerinde başarılı biçimde genelleme yapabildiğini göstermektedir.

Proje önerisinde belirlenen **100 metrenin altında MAE** hedefi başarıyla sağlanmıştır.

---

# 6. Oluşturulan Çıktılar

Kod

- Training Pipeline
- Evaluation Pipeline
- Checkpoint Sistemi

Sonuçlar

- Model ağırlıkları (.pth)
- Prediction CSV
- Evaluation Summary JSON
- Markdown Evaluation Report
- Scatter Plot
- Error Histogram

Dokümantasyon

- README
- Araştırma Günlüğü
- Literatür Notları
- Yöntem Özeti
- Haftalık Raporlar

---

# 7. Karşılaşılan Teknik Kararlar

Proje sürecinde aşağıdaki önemli teknik kararlar alınmıştır.

- Scene-Based veri bölme yöntemi kullanılmıştır.
- ImageNet ön eğitimli ağırlıklar tercih edilmiştir.
- 224×224 giriş boyutu kullanılmıştır.
- ImageNet normalizasyon değerleri uygulanmıştır.
- En iyi model Validation MAE değerine göre seçilmektedir.
- Evaluation modülü eğitim kodundan bağımsız geliştirilmiştir.

---

# 8. Sonraki Hafta Planı

Planlanan çalışmalar:

- ResNet50 transfer öğrenme modelinin geliştirilmesi
- Model eğitimi
- Test değerlendirmesi
- VGG16 ile performans karşılaştırması
- Karşılaştırma raporunun hazırlanması

---

# 9. Danışmandan Görüş Alınması Planlanan Konular

Toplantı sırasında aşağıdaki konular hakkında görüş alınması planlanmaktadır.

- Veri kümesi seçiminin uygunluğu
- VGG16 sonuçlarının değerlendirilmesi
- ResNet50 mimarisine geçiş planı
- Kullanılacak hiperparametreler
- Attention mekanizmasının entegrasyonu
- Sonraki deneylerin planlanması

---

# 10. Danışman Geri Bildirimleri

> Toplantı sonrasında doldurulacaktır.

### Öneriler

-

### İstenen Revizyonlar

-

### Yeni Görevler

-

### Sonraki Toplantıya Kadar Yapılacaklar

-