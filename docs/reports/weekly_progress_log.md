# Haftalık İlerleme Günlüğü

**Proje Adı:** Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Destek Programı:** TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı

---

# Amaç

Bu doküman, proje süresince gerçekleştirilen haftalık çalışmaların kronolojik özetini içermektedir.

Her haftanın ayrıntılı teknik açıklamaları ilgili hafta raporlarında (`week1_report.md`, `week2_report.md` vb.) yer almaktadır. Bu belge ise projenin genel ilerleme durumunu hızlı ve düzenli bir şekilde takip edebilmek amacıyla hazırlanmıştır.

---

# Genel İlerleme

| Aşama | Durum |
|-------|:-----:|
| Veri Hazırlama | ✅ Tamamlandı |
| Ön İşleme Pipeline'ı | ✅ Tamamlandı |
| Veri Bölme Stratejisi | ✅ Tamamlandı |
| VGG16 Baseline | ✅ Tamamlandı |
| VGG16 Evaluation | ✅ Tamamlandı |
| ResNet50 Baseline | ⏳ Devam Ediyor |
| ResNet50 Evaluation | ⏳ Bekliyor |
| Model Karşılaştırması | ⏳ Bekliyor |
| Attention Mekanizması | ⏳ Bekliyor |
| Flask Prototipi | ⏳ Bekliyor |

---

# Hafta 1 — Veri Hazırlama ve Altyapı

**Durum:** ✅ Tamamlandı

## Gerçekleştirilen Çalışmalar

- FRIDA ve FRIDA2 veri setleri incelendi.
- Veri kümesi analiz edildi.
- Görüntü doğrulama işlemleri tamamlandı.
- Sentetik görüş mesafesi veri kümesi oluşturuldu.
- Scene-Based veri bölme stratejisi geliştirildi.
- Ön işleme (Preprocessing) pipeline'ı tasarlandı.
- PyTorch DataLoader altyapısı geliştirildi.
- Proje dokümantasyonu oluşturuldu.

## Temel Çıktılar

| Özellik | Sonuç |
|---------|------:|
| Toplam Sahne | **84** |
| Toplam Görüntü | **672** |
| Görüş Mesafesi Seviyesi | **8** |
| Train Görüntüleri | **464** |
| Validation Görüntüleri | **96** |
| Test Görüntüleri | **112** |

## Hafta Sonu Durumu

Veri hazırlama süreci başarıyla tamamlanmış, proje model geliştirme aşamasına hazır hale getirilmiştir.

---

# Hafta 2 — VGG16 Baseline Modeli

**Durum:** ✅ Tamamlandı

## Gerçekleştirilen Çalışmalar

- VGG16 transfer öğrenme modeli geliştirildi.
- Regresyon başlığı oluşturuldu.
- Eğitim (training) pipeline'ı geliştirildi.
- Checkpoint sistemi oluşturuldu.
- Deney kayıt sistemi hazırlandı.
- İlk baseline modeli eğitildi.
- Evaluation pipeline geliştirildi.
- Test değerlendirmesi gerçekleştirildi.
- Grafikler ve otomatik raporlar oluşturuldu.
- README ve araştırma dokümanları güncellendi.

## Temel Sonuçlar

| Metrik | Sonuç |
|--------|------:|
| Eğitim Epoch Sayısı | **20** |
| En Başarılı Epoch | **18** |
| Validation MAE | **69.9705 m** |
| Test MAE | **66.7227 m** |
| Test Görüntü Sayısı | **112** |

## Oluşturulan Çıktılar

- VGG16 eğitim modeli (Checkpoint)
- Evaluation Pipeline
- Test Prediction CSV
- Evaluation Summary JSON
- Markdown Evaluation Report
- Actual vs Predicted Scatter Plot
- Prediction Error Histogram

## Hafta Sonu Durumu

İlk transfer öğrenme tabanlı baseline model başarıyla tamamlanmıştır. Model, proje önerisinde belirlenen **100 metrenin altında MAE** hedefini hem doğrulama hem de bağımsız test kümesi üzerinde karşılamıştır.

---

# Hafta 3 — ResNet50 Baseline

**Durum:** ⏳ Henüz Başlanmadı

## Planlanan Çalışmalar

- ResNet50 transfer öğrenme modelinin geliştirilmesi
- Eğitim pipeline'ının uyarlanması
- Model eğitimi
- Evaluation süreci
- VGG16 ile performans karşılaştırması

---

# Hafta 4 — Attention Mekanizması ve Proje Tamamlama

**Durum:** ⏳ Henüz Başlanmadı

## Planlanan Çalışmalar

- Attention mekanizmasının entegrasyonu
- Fine-tuning çalışmaları
- Nihai model değerlendirmesi
- Flask tabanlı web prototipi
- Son performans analizi
- Proje raporunun hazırlanması

---

# Güncel Proje Durumu

- Veri hazırlama süreci tamamlandı.
- İlk baseline model (VGG16) başarıyla geliştirildi.
- İlk deneysel sonuçlar elde edildi.
- Değerlendirme altyapısı tamamlandı.
- İkinci baseline model (ResNet50) geliştirme aşamasına geçilmeye hazırdır.