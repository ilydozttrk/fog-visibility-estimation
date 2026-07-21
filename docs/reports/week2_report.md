# 2. Hafta İlerleme Raporu

**Proje Adı:** Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Destek Programı:** TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı

**Rapor Dönemi:** 2. Hafta

**Hazırlayan:** İlayda Öztürk

---

# 1. Giriş

İkinci hafta boyunca proje kapsamında ilk transfer öğrenme tabanlı temel model (baseline) geliştirilmiştir. Bu süreçte VGG16 mimarisi regresyon problemine uyarlanmış, eğitim altyapısı oluşturulmuş, model eğitilmiş ve bağımsız test kümesi üzerinde değerlendirilmiştir.

Ayrıca deneylerin tekrarlanabilirliğini artırmak amacıyla checkpoint sistemi, deney kayıt mekanizması ve otomatik değerlendirme (evaluation) altyapısı geliştirilmiştir.

Hafta sonunda ilk baseline model başarıyla tamamlanmış ve proje önerisinde hedeflenen performans kriteri karşılanmıştır.

---

# 2. Haftalık Hedefler

İkinci hafta için belirlenen hedefler aşağıdaki gibidir.

- VGG16 mimarisinin incelenmesi
- Transfer öğrenme tabanlı regresyon modelinin geliştirilmesi
- Eğitim (training) pipeline'ının hazırlanması
- Checkpoint sisteminin geliştirilmesi
- Deney kayıt altyapısının oluşturulması
- İlk baseline modelinin eğitilmesi
- Model değerlendirme (evaluation) altyapısının hazırlanması
- Bağımsız test kümesi üzerinde performans analizinin gerçekleştirilmesi
- Sonuçların dokümante edilmesi

Planlanan çalışmaların tamamı başarıyla gerçekleştirilmiştir.

---

# 3. Gerçekleştirilen Çalışmalar

## 3.1 VGG16 Transfer Öğrenme Modelinin Geliştirilmesi

İlk baseline model olarak ImageNet üzerinde önceden eğitilmiş VGG16 mimarisi seçilmiştir.

Sınıflandırma amacıyla tasarlanan son katmanlar kaldırılarak yerine tek bir sürekli değer üreten regresyon başlığı eklenmiştir.

Model yalnızca görüş mesafesi tahmini gerçekleştirecek şekilde yeniden yapılandırılmıştır.

Bu sayede modelin çıktı değeri görüntüye karşılık gelen görünürlük mesafesini metre cinsinden tahmin etmektedir.

---

## 3.2 Eğitim Pipeline'ının Oluşturulması

Model eğitimi için modüler bir eğitim altyapısı geliştirilmiştir.

Bu kapsamda;

- eğitim döngüsü oluşturulmuş,
- validation süreci eklenmiş,
- epoch bazlı performans takibi sağlanmış,
- optimizer ve loss fonksiyonları tanımlanmış,
- cihaz (CPU/GPU) yönetimi eklenmiştir.

Her epoch sonunda eğitim ve doğrulama performansı otomatik olarak hesaplanacak şekilde yapılandırılmıştır.

---

## 3.3 Checkpoint Mekanizmasının Geliştirilmesi

Model eğitimi sırasında en düşük doğrulama hatasına sahip modelin otomatik olarak kaydedilmesi amacıyla checkpoint sistemi geliştirilmiştir.

Checkpoint içerisinde;

- model ağırlıkları,
- optimizer durumu,
- epoch bilgisi,
- validation MAE değeri

saklanmaktadır.

Bu yapı sayesinde en başarılı model daha sonra yeniden yüklenerek değerlendirme aşamasında kullanılabilmektedir.

---

## 3.4 Deney Kayıt Sistemi

Deneylerin düzenli biçimde takip edilebilmesi amacıyla deney kayıt sistemi oluşturulmuştur.

Her eğitim sonunda;

- epoch sayısı,
- öğrenme oranı,
- batch size,
- optimizer,
- validation performansı

kayıt altına alınacak şekilde yapı hazırlanmıştır.

Bu sistem ilerleyen haftalarda gerçekleştirilecek ResNet50 ve Attention deneylerinde ortak olarak kullanılacaktır.

---

## 3.5 Model Eğitimi

Hazırlanan eğitim altyapısı kullanılarak ilk VGG16 baseline modeli eğitilmiştir.

Toplam eğitim süresi boyunca model doğrulama performansı düzenli olarak takip edilmiş ve en başarılı model checkpoint olarak kaydedilmiştir.

Eğitim sonunda;

| Metrik | Sonuç |
|--------|------:|
| Epoch | **20** |
| En Başarılı Epoch | **18** |
| Best Validation MAE | **69.9705 m** |

olarak elde edilmiştir.

Bu sonuç proje önerisinde belirlenen **100 metre altında MAE** hedefini başarıyla karşılamaktadır.

---

## 3.6 Evaluation Pipeline'ının Geliştirilmesi

Eğitim tamamlandıktan sonra bağımsız test kümesi üzerinde değerlendirme yapılabilmesi amacıyla ayrı bir evaluation modülü geliştirilmiştir.

Bu modül;

- checkpoint yükleme,
- test veri kümesinin değerlendirilmesi,
- MAE hesaplanması,
- tahmin sonuçlarının kaydedilmesi,
- grafiklerin oluşturulması,
- değerlendirme raporunun hazırlanması

işlemlerini otomatik olarak gerçekleştirmektedir.

Evaluation süreci eğitim kodundan bağımsız olarak tasarlanmış ve gelecekteki tüm modeller tarafından yeniden kullanılabilecek şekilde geliştirilmiştir.

---

## 3.7 Test Değerlendirmesi

En başarılı checkpoint bağımsız test kümesi üzerinde değerlendirilmiştir.

Test sonuçları aşağıdaki gibidir.

| Metrik | Sonuç |
|--------|------:|
| Test Görüntü Sayısı | **112** |
| Test MAE | **66.7227 m** |
| Validation MAE | **69.9705 m** |
| Mean Signed Error | **−17.3877 m** |

Test performansının doğrulama performansına oldukça yakın olması modelin daha önce görmediği sahneler üzerinde başarılı biçimde genelleme yapabildiğini göstermektedir.

---

## 3.8 Otomatik Çıktılar

Evaluation modülü çalıştırıldığında aşağıdaki çıktılar otomatik olarak oluşturulmaktadır.

### Grafikler

- Actual vs Predicted Scatter Plot
- Prediction Error Histogram

### Sayısal Çıktılar

- Test Prediction CSV
- Evaluation Summary JSON

### Rapor

- Markdown Evaluation Report

Bu yapı ilerleyen haftalarda farklı modellerin sonuçlarının doğrudan karşılaştırılmasını kolaylaştıracaktır.

---

## 3.9 Dokümantasyon Güncellemeleri

Hafta boyunca proje dokümantasyonu güncellenmiştir.

Güncellenen dosyalar:

- README
- Araştırma günlüğü
- Yöntem özeti
- Proje kapsamı

Ayrıca GitHub üzerinde geliştirme süreci anlamlı commit'ler halinde kayıt altına alınmıştır.

---

# 4. Oluşturulan Dosyalar

## Kaynak Kod

- train_vgg16.py
- evaluation_vgg16.py
- __init__.py (evaluation)

## Sonuç Dosyaları

- vgg16_baseline_best.pth
- vgg16_test_predictions.csv
- vgg16_evaluation_summary.json
- vgg16_evaluation_report.md
- vgg16_actual_vs_predicted.png
- vgg16_prediction_error_histogram.png

---

# 5. Karşılaşılan Problemler ve Çözümleri

Bu hafta boyunca aşağıdaki teknik konular üzerinde karar verilmiştir.

### Regresyon Başlığının Tasarlanması

VGG16 mimarisi sınıflandırma amacıyla geliştirildiğinden son katman yeniden tasarlanarak sürekli değer üreten regresyon yapısına dönüştürülmüştür.

---

### Checkpoint Seçimi

En iyi modelin yalnızca son epoch yerine en düşük validation MAE değerine göre seçilmesine karar verilmiştir.

---

### Evaluation Altyapısı

Model değerlendirmesinin eğitim kodundan bağımsız tutulmasına karar verilmiştir.

Bu yaklaşım sayesinde aynı değerlendirme prosedürü ResNet50 ve ileride geliştirilecek Attention modeli için de kullanılabilecektir.

---

# 6. Hafta Sonu Değerlendirmesi

İkinci hafta sonunda proje kapsamında ilk transfer öğrenme tabanlı baseline model başarıyla tamamlanmıştır.

Model eğitim süreci tamamlanmış, bağımsız test kümesi üzerinde değerlendirme gerçekleştirilmiş ve proje hedefi olan 100 metrenin altında MAE değeri elde edilmiştir.

Ayrıca geliştirilen evaluation altyapısı sayesinde ilerleyen haftalarda farklı CNN mimarileri aynı prosedür kullanılarak objektif biçimde karşılaştırılabilecektir.

---

# 7. Sonraki Hafta Planı

Üçüncü haftada aşağıdaki çalışmaların gerçekleştirilmesi planlanmaktadır.

- ResNet50 mimarisinin geliştirilmesi
- İkinci baseline modelinin eğitilmesi
- Bağımsız test değerlendirmesinin yapılması
- VGG16 ve ResNet50 performanslarının karşılaştırılması
- Deney sonuçlarının analiz edilmesi

---

# 8. Genel Sonuç

İkinci hafta sonunda proje, yalnızca veri hazırlama aşamasını tamamlamış bir araştırma olmaktan çıkmış; ilk deneysel sonuçlarını üreten, ölçülebilir performans değerlerine sahip bir bilgisayarlı görü çalışmasına dönüşmüştür.

Elde edilen **66.7227 metre Test MAE** değeri, proje önerisinde belirlenen başarı kriterini karşılamakta olup geliştirilecek ResNet50 ve Attention tabanlı modeller için referans (baseline) performansı oluşturmaktadır.