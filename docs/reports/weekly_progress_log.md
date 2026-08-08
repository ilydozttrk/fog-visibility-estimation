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
| --- | :---: |
| Veri Hazırlama | ✅ Tamamlandı |
| Ön İşleme Pipeline'ı | ✅ Tamamlandı |
| Veri Bölme Stratejisi | ✅ Tamamlandı |
| VGG16 Baseline | ✅ Tamamlandı |
| VGG16 Evaluation | ✅ Tamamlandı |
| ResNet50 Baseline | ✅ Tamamlandı |
| ResNet50 Evaluation | ✅ Tamamlandı |
| ResNet50 Görsel Hata Analizi | ✅ Tamamlandı |
| Model Karşılaştırması | ⏳ Bekliyor |
| Nihai Baseline Seçimi | ⏳ Bekliyor |
| Attention Mekanizması | ⏳ Bekliyor |
| Gerçek Dünya Değerlendirmesi | ⏳ Bekliyor |
| Flask Prototipi | ⏳ Bekliyor |

---

# Hafta 1 — Veri Hazırlama ve Altyapı

**Durum:** ✅ Tamamlandı

## Gerçekleştirilen Çalışmalar

- FRIDA ve FRIDA2 veri setleri incelendi.
- Veri kümesi analiz edildi.
- Görüntü ve derinlik haritası yapıları doğrulandı.
- Sentetik görüş mesafesi veri kümesi oluşturuldu.
- Scene-based veri bölme stratejisi geliştirildi.
- Ön işleme (Preprocessing) pipeline'ı tasarlandı ve uygulandı.
- PyTorch Dataset ve DataLoader altyapısı geliştirildi.
- Proje dokümantasyonu oluşturuldu.

## Temel Çıktılar

| Özellik | Sonuç |
| --- | ---: |
| Toplam Sahne | **84** |
| Toplam Görüntü | **672** |
| Görüş Mesafesi Seviyesi | **8** |
| Training Görüntüleri | **464** |
| Validation Görüntüleri | **96** |
| Test Görüntüleri | **112** |

## Hafta Sonu Durumu

Veri hazırlama süreci başarıyla tamamlanmış ve proje transfer öğrenme tabanlı model geliştirme aşamasına hazır hâle getirilmiştir.

Aynı temel sahneye ait görüş mesafesi varyasyonlarının farklı veri alt kümelerine dağılmasını önlemek amacıyla scene-based split uygulanmış ve veri sızıntısı riski azaltılmıştır.

---

# Hafta 2 — VGG16 Baseline Modeli

**Durum:** ✅ Tamamlandı

## Gerçekleştirilen Çalışmalar

- VGG16 mimarisi incelendi.
- ImageNet pretrained VGG16 modeli projeye entegre edildi.
- Backbone katmanları donduruldu.
- Regresyon başlığı oluşturuldu.
- Eğitim (training) pipeline'ı geliştirildi.
- Checkpoint sistemi oluşturuldu.
- Deney kayıt sistemi hazırlandı.
- VGG16 baseline modeli 20 epoch boyunca eğitildi.
- Evaluation pipeline geliştirildi.
- Bağımsız test değerlendirmesi gerçekleştirildi.
- Actual vs Predicted grafiği oluşturuldu.
- Prediction Error Histogram oluşturuldu.
- Evaluation çıktıları otomatik olarak kaydedildi.
- README, araştırma günlüğü ve ilgili proje dokümanları güncellendi.

## Temel Sonuçlar

| Metrik | Sonuç |
| --- | ---: |
| Eğitim Epoch Sayısı | **20** |
| En Başarılı Epoch | **18** |
| Best Validation MAE | **69.9705 m** |
| Test MAE | **66.7227 m** |
| Mean Signed Error | **−17.3877 m** |
| Test Görüntü Sayısı | **112** |

## Oluşturulan Çıktılar

- VGG16 model checkpoint'i
- Training log
- Experiment log
- Evaluation pipeline
- Test Prediction CSV
- Evaluation Summary JSON
- Markdown Evaluation Report
- Actual vs Predicted Scatter Plot
- Prediction Error Histogram
- Training / Validation Loss Curve

## Hafta Sonu Durumu

İlk transfer öğrenme tabanlı baseline model başarıyla tamamlanmıştır.

VGG16 modeli:

- **69.9705 m Validation MAE**
- **66.7227 m Test MAE**

elde etmiş ve proje önerisinde belirlenen **MAE < 100 metre** performans hedefini hem validation hem de bağımsız test sonuçları açısından karşılamıştır.

Bu sonuç, sonraki ResNet50 deneyinin karşılaştırılacağı ilk resmi baseline performansı olarak kaydedilmiştir.

---

# Hafta 3 — ResNet50 Baseline ve Karşılaştırmalı Analiz

**Durum:** 🔄 Devam Ediyor

## Gerçekleştirilen Çalışmalar

### ResNet50 Mimarisinin Geliştirilmesi

- ResNet50 mimarisi ve residual learning yaklaşımı incelendi.
- VGG16 ve ResNet50 mimari farklılıkları değerlendirildi.
- ImageNet pretrained ResNet50 ağırlıkları yüklendi.
- Backbone katmanları donduruldu.
- Orijinal classification head regresyon başlığı ile değiştirildi.
- `train_resnet50.py` geliştirildi.
- Modelin forward-pass testi gerçekleştirildi.
- Trainable ve frozen parametre sayıları doğrulandı.

Model parametreleri:

| Parametre Türü | Sayı |
| --- | ---: |
| Toplam Parametre | **24,622,913** |
| Eğitilebilir Parametre | **1,114,881** |
| Dondurulmuş Parametre | **23,508,032** |

### DataLoader Uyumluluğu

ResNet50 modelinin mevcut veri pipeline'ı ile uyumluluğu doğrulanmıştır.

Test sırasında:

```text
Images  : [16, 3, 224, 224]
Targets : [16]
Outputs : [16, 1]
```

boyutları elde edilmiş ve modelin mevcut `FogVisibilityDataset` / `DataLoader` altyapısıyla doğru şekilde çalıştığı doğrulanmıştır.

### ResNet50 Eğitimi

ResNet50 baseline modeli VGG16 ile karşılaştırılabilir temel deney koşulları altında **20 epoch** boyunca eğitilmiştir.

Eğitim boyunca Training MAE ve Validation MAE değerleri düzenli olarak azalmıştır.

Başlangıç ve final performansı:

| Metrik | Başlangıç | Final |
| --- | ---: | ---: |
| Training MAE | **271.6411 m** | **122.1239 m** |
| Validation MAE | **269.8412 m** | **121.8414 m** |

En iyi Validation MAE:

**121.8414 m**

ile **20. epochta** elde edilmiştir.

Bu sonuçla ResNet50 baseline modeli mevcut konfigürasyonda proje hedefi olan **MAE < 100 metre** değerine ulaşamamıştır.

### ResNet50 Evaluation

ResNet50 için bağımsız bir evaluation modülü geliştirilmiş ve en başarılı checkpoint bağımsız test kümesi üzerinde değerlendirilmiştir.

Evaluation pipeline aşağıdaki çıktıları otomatik olarak üretmiştir:

- Test Prediction CSV
- Evaluation Summary JSON
- Markdown Evaluation Report
- Actual vs Predicted Plot
- Prediction Error Histogram

Bağımsız test sonuçları:

| Metrik | Sonuç |
| --- | ---: |
| Test Samples | **112** |
| Test MAE | **124.6181 m** |
| Validation MAE | **121.8414 m** |
| Mean Signed Error | **−77.3460 m** |
| Maximum Absolute Error | **602.6687 m** |
| Validation-Test MAE Farkı | **2.7767 m** |

Validation ve Test MAE değerlerinin birbirine yakın olması, bağımsız test kümesinde büyük bir performans düşüşü olmadığını göstermiştir.

### Learning Curve ve Overfitting Analizi

ResNet50 Training ve Validation MAE eğrileri 20 epoch boyunca birlikte azalmıştır.

Eğriler arasında belirgin bir ayrışma gözlenmemiştir.

20. epoch sonunda:

- Training MAE: **122.1239 m**
- Validation MAE: **121.8414 m**

olarak ölçülmüştür.

Aradaki fark yaklaşık **0.28 m** düzeyindedir.

Bu nedenle mevcut deneyde klasik anlamda belirgin bir overfitting davranışı gözlenmemiştir.

En iyi Validation MAE'nin son epochta elde edilmesi modelin mevcut eğitim süresi sonunda tamamen yakınsamamış olabileceğini düşündürmektedir. Bununla birlikte baseline karşılaştırmasının aynı eğitim bütçesi altında gerçekleştirilmesi amacıyla eğitim süresi değiştirilmemiştir.

### Actual vs Predicted Analizi

Actual vs Predicted grafiği modelin özellikle yüksek görüş mesafelerinde gerçek değerleri sistematik biçimde düşük tahmin ettiğini göstermiştir.

Özellikle:

- **500 m**
- **800 m**

ground-truth örneklerinde belirgin underestimation davranışı gözlenmiştir.

800 m ground-truth değerine sahip bazı örneklerde tahminlerin yaklaşık **200–360 m** aralığında yoğunlaştığı görülmüştür.

Model tahminlerinin ground-truth hedef aralığından daha dar bir bölgede yoğunlaşması **prediction-range compression** davranışı olarak kaydedilmiştir.

### Prediction Error Histogram Analizi

Prediction Error Histogram negatif yönde uzun bir hata kuyruğu göstermiştir.

Bazı örneklerde tahmin hatası yaklaşık **−600 m** seviyesine ulaşmıştır.

Bu gözlem:

- Mean Signed Error: **−77.3460 m**
- Maximum Absolute Error: **602.6687 m**

sonuçlarıyla uyumludur.

Mevcut deneysel bulgulara göre ResNet50'nin temel sınırlılığı klasik overfitting yerine özellikle yüksek görüş mesafelerinde ortaya çıkan sistematik underestimation ve prediction-range compression davranışıdır.

Bu davranışın kesin nedeni mevcut deneylerden belirlenmemiştir.

---

## Hafta 3 Mevcut Baseline Sonuçları

| Metrik | VGG16 | ResNet50 |
| --- | ---: | ---: |
| Best Epoch | **18** | **20** |
| Best Validation MAE | **69.9705 m** | **121.8414 m** |
| Test MAE | **66.7227 m** | **124.6181 m** |
| Mean Signed Error | **−17.3877 m** | **−77.3460 m** |
| MAE < 100 m | **Evet** | **Hayır** |

Mevcut bağımsız test sonuçlarına göre VGG16, ResNet50'den daha düşük MAE üretmiştir.

İki model arasındaki Test MAE farkı:

```text
124.6181 − 66.7227 = 57.8954 m
```

olarak hesaplanmaktadır.

Day 14 itibarıyla VGG16 mevcut deneysel sonuçlarda daha güçlü baseline adayıdır.

---

## Hafta 3 Kalan Çalışmalar

- [x] ResNet50 mimarisinin geliştirilmesi
- [x] Eğitim pipeline'ının uyarlanması
- [x] ResNet50 baseline eğitimi
- [x] ResNet50 evaluation pipeline'ının geliştirilmesi
- [x] Bağımsız test değerlendirmesi
- [x] Evaluation grafiklerinin oluşturulması
- [x] Learning curve analizi
- [x] Overfitting analizi
- [x] Prediction davranışının incelenmesi
- [ ] VGG16 ve ResNet50'nin resmi karşılaştırmalı analizinin tamamlanması
- [ ] Nihai baseline mimarisinin seçilmesi
- [ ] Hafta 3 raporunun hazırlanması

---

# Hafta 4 — Attention Mekanizması ve Proje Tamamlama

**Durum:** ⏳ Henüz Başlanmadı

## Planlanan Çalışmalar

- Seçilen baseline mimariye Attention Mechanism entegrasyonu
- Attention modelinin eğitilmesi
- Attention modelinin bağımsız test değerlendirmesi
- Baseline ve Attention model performanslarının karşılaştırılması
- Gerçek dünya veri setlerinin erişilebilirlik ve uygunluk durumunun değerlendirilmesi
- Uygun olması durumunda gerçek dünya evaluation / fine-tuning
- Flask tabanlı web prototipinin geliştirilmesi
- Nihai performans analizi
- Proje dokümantasyonunun tamamlanması
- Nihai proje raporunun hazırlanması

---

# Güncel Proje Durumu — Day 14

Day 14 itibarıyla projenin iki temel CNN baseline modeli başarıyla geliştirilmiş, eğitilmiş ve bağımsız test veri kümesi üzerinde değerlendirilmiştir.

Mevcut durum:

- ✅ Veri hazırlama tamamlandı.
- ✅ 672 görüntülük sentetik regresyon veri kümesi oluşturuldu.
- ✅ Scene-based split tamamlandı.
- ✅ Preprocessing ve DataLoader altyapısı tamamlandı.
- ✅ VGG16 baseline tamamlandı.
- ✅ VGG16 evaluation tamamlandı.
- ✅ VGG16 Test MAE: **66.7227 m**
- ✅ ResNet50 baseline tamamlandı.
- ✅ ResNet50 evaluation tamamlandı.
- ✅ ResNet50 Test MAE: **124.6181 m**
- ✅ ResNet50 learning curve ve hata analizi tamamlandı.
- ✅ ResNet50 için yüksek görüş mesafelerinde underestimation gözlemlendi.
- ✅ Prediction-range compression davranışı dokümante edildi.
- 🔄 VGG16–ResNet50 karşılaştırmalı analiz aşamasına gelindi.
- ⏳ Nihai baseline seçimi bekliyor.
- ⏳ Attention Mechanism aşaması bekliyor.
- ⏳ Gerçek dünya değerlendirmesi bekliyor.
- ⏳ Flask prototipi bekliyor.

Mevcut bağımsız test sonuçlarına göre **VGG16, ResNet50'den 57.8954 metre daha düşük Test MAE** elde etmiş ve Day 14 itibarıyla en güçlü baseline adayı hâline gelmiştir.

Bir sonraki aşamada iki modelin performans ve hata davranışları doğrudan karşılaştırılacak, nihai baseline mimari seçilecek ve Attention Mechanism entegrasyonuna geçilecektir.