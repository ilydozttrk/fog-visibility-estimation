# TÜBİTAK 2209-A Final Raporu — İçerik Taslağı

> **Not:** Bu dosya, resmi TÜBİTAK sonuç raporu formuna aktarılmak üzere hazırlanmış içerik taslağıdır. Resmi formun bölüm adları ve karakter sınırları doğrulandıktan sonra nihai metin ilgili alanlara uyarlanacaktır.

---

# A. PROJE BİLGİLERİ

**Proje Başlığı:**
Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

**Program:**
TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı

**Proje Yürütücüsü:**
İlayda Öztürk

**Danışman:**
Songül Karakuş

**Kurum:**
Bitlis Eren Üniversitesi

**Önerilen Proje Dönemi:**
1 Nisan 2026 – 31 Ekim 2026

---

# 1. PROJENİN ÖZETİ

Bu projede sisli hava koşullarında görüntü tabanlı görüş mesafesi tahmini amacıyla transfer öğrenme temelli CNN mimarileri karşılaştırmalı olarak incelenmiştir. Çalışmanın temel amacı, VGG16 ve ResNet50 mimarilerinin aynı problem üzerinde performanslarını nicel olarak karşılaştırmak, daha düşük hata üreten mimari üzerinde dikkat mekanizmalarını değerlendirmek, seçilen modeli gerçek dünya verisine adapte etmek ve elde edilen nihai modeli Flask tabanlı fonksiyonel bir web prototipine dönüştürmektir.

İlk aşamada FRIDA ve FRIDA2 sentetik veri setlerinden 84 sahne ve 672 görüntü içeren sürekli görüş mesafesi regresyon veri yapısı hazırlanmıştır. Aynı sahneye ait farklı sis seviyelerinin farklı veri alt kümelerine dağılmasını önlemek amacıyla scene-based veri ayrımı uygulanmış ve veri 464 eğitim, 96 doğrulama ve 112 test görüntüsüne ayrılmıştır.

VGG16 ve ResNet50 modelleri ImageNet üzerinde önceden eğitilmiş ağırlıklar kullanılarak regresyon problemine adapte edilmiştir. Sentetik test kümesinde VGG16 modeli 66.7227 m MAE, ResNet50 modeli ise 124.6181 m MAE elde etmiştir. Böylece mevcut deney düzeninde VGG16 daha düşük test hatası üreten temel mimari olarak seçilmiştir.

Seçilen VGG16 mimarisi üzerinde CBAM ve SE dikkat mekanizmaları ayrıca değerlendirilmiştir. CBAM modeli 67.6214 m, SE modeli ise 72.4412 m test MAE üretmiştir. Her iki mekanizma da teknik olarak başarıyla uygulanmasına rağmen VGG16 baseline modelinin test MAE değerini iyileştirmemiştir.

Gerçek dünya adaptasyonu aşamasında FVEI veri seti üzerinde veri denetimi, duplicate ve similarity kontrolleri, stratified veri ayrımı ve model fine-tuning işlemleri gerçekleştirilmiştir. Nihai split 2245 eğitim, 480 doğrulama ve 482 kilitli test örneğinden oluşmuştur. Sentetik VGG16 checkpoint'i başlangıç noktası olarak kullanılmış; VGG16'nın ilk dört bloğu dondurulmuş, beşinci blok ve regresyon başlığı gerçek dünya verisi üzerinde ince ayar edilmiştir.

Validation MAE temelinde 12. epoch nihai checkpoint olarak seçilmiş ve 26.4428 m doğrulama MAE elde edilmiştir. Model geliştirme süreci tamamlandıktan sonra açılan 482 görüntülük held-out FVEI test kümesinde nihai model 25.1347 m MAE, 38.4440 m RMSE, 0.894442 R² ve +3.4534 m ortalama bias üretmiştir.

Son aşamada validation tabanlı seçilen FVEI modeli Flask API ve HTML/CSS web arayüzüne entegre edilmiştir. Sistem görüntü yükleme, görüntü önizleme ve metre cinsinden görüş mesafesi tahmini işlevlerini gerçekleştirmektedir. API için geliştirilen otomatik test paketi 6 testin tamamını başarıyla geçmiştir.

Elde edilen sonuçlar, transfer öğrenme tabanlı VGG16 mimarisinin mevcut deney koşullarında hem sentetik hem de FVEI gerçek dünya verisi üzerinde görüş mesafesi regresyonu için uygulanabilir bir temel oluşturduğunu göstermektedir. Bununla birlikte sonuçlar tek ana veri ayrımı ve random seed 42 üzerinden elde edildiğinden istatistiksel anlamlılık iddiasında bulunulmamaktadır.

---

# 2. PROJENİN AMACI VE HEDEFLERİ

Araştırma önerisinde projenin temel amacı, sisli hava koşullarında yol güvenliğini artırmaya yönelik olarak önceden eğitilmiş CNN modellerini transfer öğrenme yöntemi ile görüş mesafesi tahmini görevine adapte etmek, modellerin performanslarını karşılaştırmak ve AUS entegrasyon potansiyelini gösterecek fonksiyonel bir prototip geliştirmek olarak belirlenmiştir.

Bu kapsamda aşağıdaki hedefler gerçekleştirilmiştir:

1. VGG16 ve ResNet50 mimarilerinin görüş mesafesi regresyon problemine adapte edilmesi.
2. Modellerin aynı sentetik veri yapısı altında karşılaştırılması.
3. Test kümesinde daha düşük MAE üreten temel mimarinin belirlenmesi.
4. Seçilen mimari üzerinde dikkat mekanizmalarının değerlendirilmesi.
5. Gerçek dünya görüntülerine dayalı FVEI veri setinin projeye entegre edilmesi.
6. Nihai modelin gerçek dünya verisi üzerinde fine-tuning işlemine tabi tutulması.
7. Validation tabanlı model seçiminin ardından bağımsız held-out test değerlendirmesinin yapılması.
8. Nihai modelin Flask API ve web arayüzüne entegre edilmesi.
9. Deney, raporlama ve değerlendirme pipeline'larının tekrar üretilebilir biçimde dokümante edilmesi.

Araştırma önerisinde belirlenen **MAE < 100 m** performans hedefi hem sentetik VGG16 baseline modelinde hem de FVEI gerçek dünya modelinde karşılanmıştır.

---

# 3. ARAŞTIRMA SORUSU VE HİPOTEZİN DEĞERLENDİRİLMESİ

## 3.1 Araştırma Sorusu

Araştırma önerisinde temel araştırma sorusu şu şekilde tanımlanmıştır:

> Transfer öğrenme yöntemi ile görüntü tabanlı görüş mesafesi tahmini görevine adapte edilen VGG16 ve ResNet50 mimarilerinden hangisi, mevcut deney koşullarında daha düşük MAE değeri üretmektedir?

Sentetik held-out test sonuçları:

| Model | Test MAE |
|---|---:|
| VGG16 | **66.7227 m** |
| ResNet50 | 124.6181 m |

Bu sonuçlara göre mevcut FRIDA/FRIDA2 veri yapısı ve deney koşullarında VGG16, ResNet50'den daha düşük test MAE üretmiştir.

---

## 3.2 Başlangıç Hipotezi

Araştırma önerisinde ResNet50 mimarisinin residual bağlantıları sayesinde VGG16'ya kıyasla daha düşük MAE üretmesi beklenmiştir.

Gerçekleştirilen deneylerde ise bunun tersi gözlenmiştir:

- VGG16 Test MAE: **66.7227 m**
- ResNet50 Test MAE: **124.6181 m**

Dolayısıyla başlangıç hipotezi mevcut deney sonuçları tarafından **desteklenmemiştir**.

Ayrıca çalışma tek ana split ve random seed 42 ile yürütüldüğünden modeller arasındaki fark için istatistiksel anlamlılık iddiasında bulunulmamaktadır.

Bu bulgu, proje açısından önemli bir araştırma sonucudur. Daha derin veya daha karmaşık bir CNN mimarisinin mevcut görev ve veri koşullarında zorunlu olarak daha düşük regresyon hatası üretmediğini göstermektedir.

---

# 4. YÖNTEM

## 4.1 Sentetik Veri Hazırlama

Projenin ilk aşamasında FRIDA ve FRIDA2 veri setleri kullanılmıştır.

Hazırlanan sentetik regresyon veri yapısı:

| Özellik | Değer |
|---|---:|
| Toplam sahne | 84 |
| Toplam görüntü | 672 |
| Eğitim | 464 |
| Doğrulama | 96 |
| Test | 112 |
| Random seed | 42 |

Görüş mesafesi seviyeleri:

**50, 80, 100, 150, 200, 300, 500 ve 800 metre**

Aynı temel sahneye ait farklı sis varyasyonlarının farklı veri alt kümelerine dağılmasını azaltmak amacıyla scene-based split uygulanmıştır.

---

## 4.2 VGG16 Baseline

ImageNet üzerinde önceden eğitilmiş VGG16 ağırlıkları kullanılmıştır.

Orijinal classification head kaldırılarak tek sürekli değer üreten regresyon başlığı eklenmiştir.

Modelin feature extraction katmanları baseline eğitiminde dondurulmuştur.

20 epoch eğitim sonucunda:

| Metrik | Değer |
|---|---:|
| Best epoch | 18 |
| Validation MAE | 69.9705 m |
| Test MAE | **66.7227 m** |
| Mean signed error | -17.3877 m |

---

## 4.3 ResNet50 Baseline

ResNet50 aynı temel veri ayrımı ve benzer eğitim bütçesi altında regresyon görevine adapte edilmiştir.

20 epoch sonunda:

| Metrik | Değer |
|---|---:|
| Best epoch | 20 |
| Validation MAE | 121.8414 m |
| Test MAE | 124.6181 m |
| Mean signed error | -77.3460 m |

Model özellikle yüksek görüş mesafelerinde sistematik underestimation ve prediction-range compression davranışı göstermiştir.

---

# 5. BASELINE KARŞILAŞTIRMASI

| Model | Validation MAE | Test MAE |
|---|---:|---:|
| VGG16 | 69.9705 m | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

VGG16 mevcut deney koşullarında daha düşük test MAE ürettiği için sonraki aşamalarda temel model olarak seçilmiştir.

![Sentetik model karşılaştırması](../../figures/synthetic_model_test_mae_comparison.png)

---

# 6. DİKKAT MEKANİZMASI DENEYLERİ

Araştırma önerisine uygun olarak seçilen VGG16 mimarisi üzerinde attention mekanizmaları değerlendirilmiştir.

## 6.1 CBAM

CBAM yapısı channel attention ve spatial attention bileşenlerini birlikte kullanacak şekilde VGG16 mimarisine entegre edilmiştir.

Sonuç:

| Metrik | Değer |
|---|---:|
| Validation MAE | **69.3274 m** |
| Test MAE | 67.6214 m |

CBAM validation MAE değerini küçük miktarda düşürmüş ancak held-out test MAE açısından VGG16 baseline modelini geçememiştir.

---

## 6.2 SE Attention

Araştırma önerisinin risk yönetimi planında attention mekanizmasının beklenen iyileşmeyi sağlamaması durumunda kanal odaklı SE-Net alternatifinin uygulanması öngörülmüştür.

Bu B planı proje sırasında uygulanmış ve SE attention modeli geliştirilmiştir.

Sonuç:

| Metrik | Değer |
|---|---:|
| Validation MAE | 70.6083 m |
| Test MAE | 72.4412 m |

SE mekanizması da VGG16 baseline modeline göre test MAE iyileşmesi üretmemiştir.

---

## 6.3 Attention Sonucu

| Model | Test MAE |
|---|---:|
| VGG16 Baseline | **66.7227 m** |
| VGG16 + CBAM | 67.6214 m |
| VGG16 + SE | 72.4412 m |

Bu nedenle gerçek dünya fine-tuning aşamasının başlangıç checkpoint'i olarak **VGG16 baseline** korunmuştur.

Attention entegrasyonunun teknik olarak tamamlanmış olmasıyla birlikte, proje sonuçları attention mekanizmasının mevcut veri ve deney düzeninde test performansını artırmadığını göstermiştir.

---

# 7. GERÇEK DÜNYA VERİSİNE GEÇİŞ

Araştırma önerisinde gerçek dünya verisi olarak FVEI/FHVI veri setlerinin kullanılması planlanmıştır.

FVEI verisine erişim sürecinde CIDET ve Benchmark-Visibility veri setleri yardımcı ve B-plan gerçek dünya deneyleri olarak kullanılmıştır.

Bu deneyler final FVEI modelinin seçimi için kullanılmamış, domain shift ve farklı hedef aralıklarında model davranışını incelemek amacıyla tutulmuştur.

FHVI veri setine erişim proje sürecinde sağlanamadığından final model geliştirme aşamasında kullanılmamıştır.

---

# 8. CIDET YARDIMCI DENEYLERİ

Sentetik VGG16 modelinin CIDET üzerindeki zero-shot performansı:

**MAE: 2258.8934 m**

Fine-tuning deneyleri:

| Strateji | Validation MAE |
|---|---:|
| Head-only + L1 | 446.5714 m |
| Block5 + L1 | 326.6640 m |
| Block5 + Balanced Sampling | 334.9808 m |
| Block5 + Huber | **324.1948 m** |

Bu deneyler, sentetik veriden gerçek görüntülere doğrudan geçişte önemli domain shift bulunduğunu göstermiştir.

---

# 9. BENCHMARK-VISIBILITY STRESS TEST

CIDET development modelinin daha geniş görüş mesafesi aralığına sahip Benchmark-Visibility verisindeki sonuçları:

| Metrik | Değer |
|---|---:|
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Bias | -11310.9893 m |
| Pearson correlation | 0.585183 |
| Prediction range | 97.43–1308.30 m |
| Target range | 112–20000 m |

Model geniş hedef aralığında belirgin prediction-range compression göstermiştir.

Bu deney final model tuning sürecinin parçası olarak kullanılmamıştır.

---

# 10. FVEI VERİ SETİ DENETİMİ

FVEI arşivi projeye dahil edilmeden önce veri bütünlüğü ve etiket tutarlılığı açısından ayrıca incelenmiştir.

Kaynak ZIP SHA256:

`07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d`

Audit özeti:

| Kategori | Örnek |
|---|---:|
| Retained | 4109 |
| Exact-label | 3209 |
| Level-4 / 500 m ayrı analiz grubu | 900 |
| Conflicting duplicate rejected | 229 |
| Outside level range rejected | 32 |
| Redundant identical removed | 130 |

Exact-label veri dağılımı:

| Level | N | Gözlenen Aralık |
|---|---:|---:|
| Level 0 | 785 | 12–49 m |
| Level 1 | 846 | 51–99 m |
| Level 2 | 793 | 101–199 m |
| Level 3 | 785 | 201–499 m |

500 m etiketi taşıyan 900 örnek exact-label regresyon metriklerinden ayrı tutulmuştur.

Bu grubun ceiling/censored etiket semantiği bağımsız kaynak dokümantasyonu ile doğrulanmadan standart exact-label regresyon sonucu olarak yorumlanmamıştır.

---

# 11. FVEI VERİ AYRIMI

Exact-label örnekler visibility level bazında stratified biçimde ayrılmıştır.

İlk split:

- Train: 2245
- Validation: 482
- Test: 482
- 500 m ayrı analiz grubu: 900

Cross-split similarity kontrolünde iki validation örneği şüpheli bulunarak validation setinden çıkarılmıştır.

Test seti değiştirilmemiştir.

Nihai split:

| Split | N |
|---|---:|
| Train | 2245 |
| Validation | 480 |
| Locked Test | 482 |
| Similarity exclusions | 2 |
| 500 m ayrı analiz grubu | 900 |

FVEI veri setinde güvenilir scene/camera ID bilgileri mevcut pipeline'da bulunmadığından residual sample dependence tamamen dışlanamamaktadır.

---

# 12. FVEI FINE-TUNING

Gerçek dünya fine-tuning başlangıç noktası olarak sentetik deneylerde seçilen:

`vgg16_baseline_best.pth`

checkpoint'i kullanılmıştır.

Model stratejisi:

| Model bölümü | Durum |
|---|---|
| VGG16 Blocks 1–4 | Frozen |
| VGG16 Block 5 | Trainable |
| Regression Head | Trainable |

Eğitim konfigürasyonu:

| Parametre | Değer |
|---|---:|
| Epoch | 20 |
| Batch size | 16 |
| Block5 learning rate | 1e-5 |
| Head learning rate | 1e-4 |
| Weight decay | 1e-5 |
| Loss | L1Loss |
| Random seed | 42 |

Model geliştirme sürecinde yalnızca train ve validation split kullanılmıştır.

Locked test split model seçimi sırasında kullanılmamıştır.

---

# 13. MODEL SEÇİMİ

En iyi validation sonucu:

**Epoch 12**

Validation MAE:

**26.4428 m**

Epoch 12 sonrası training MAE düşmeye devam ederken validation MAE kalıcı olarak iyileşmemiştir.

Bu nedenle epoch 12 checkpoint'i nihai model olarak seçilmiştir.

![FVEI fine-tuning eğrisi](../../figures/fvei_finetuning_mae_curve.png)

---

# 14. NİHAİ FVEI TEST SONUÇLARI

Validation tabanlı model seçimi tamamlandıktan sonra daha önce model geliştirme sürecinde kullanılmayan 482 görüntülük locked test split değerlendirilmiştir.

| Metrik | Sonuç |
|---|---:|
| Test samples | 482 |
| MAE | **25.1347 m** |
| RMSE | **38.4440 m** |
| R² | **0.894442** |
| Bias | **+3.4534 m** |

Test sonucu görüldükten sonra model checkpoint'i, hiperparametreler veya eğitim stratejisi üzerinde yeniden tuning yapılmamıştır.

Araştırma önerisinde gerçek dünya değerlendirmesi için belirlenen **MAE < 100 m** hedefi karşılanmıştır.

---

# 15. LEVEL-BASED HATA ANALİZİ

| Level | N | MAE | RMSE | Bias |
|---|---:|---:|---:|---:|
| Level 0 | 118 | 11.1879 m | 14.2664 m | +7.5328 m |
| Level 1 | 127 | 12.5699 m | 15.7690 m | -3.7466 m |
| Level 2 | 119 | 21.8013 m | 29.4082 m | +8.4794 m |
| Level 3 | 118 | 55.9664 m | 68.5106 m | +2.0548 m |

En yüksek hata Level 3 grubunda gözlenmiştir.

Level 3 bias değerinin MAE ve RMSE değerlerine kıyasla düşük kalması, hataların yalnızca tek yönlü sistematik bir sapmayla açıklanamayacağını göstermektedir.

![FVEI level-wise error](../../figures/fvei_levelwise_error_comparison.png)

---

# 16. 500 m AYRI ANALİZ GRUBU

900 görüntülük bu grup exact-label test metriklerinden ayrı değerlendirilmiştir.

| Metrik | Sonuç |
|---|---:|
| Samples | 900 |
| Mean prediction | 563.4542 m |
| Median prediction | 559.8888 m |
| Prediction >= 500 m | 840 / 900 |
| Oran | 93.33% |
| Mean shortfall below 500 m | 1.6444 m |

Bu sonuçlar veri setindeki 500 m etiketinin kesin semantiği bağımsız olarak doğrulanmadığından MAE/RMSE/R² biçiminde değerlendirilmemiştir.

---

# 17. NİHAİ MODEL

Final gerçek dünya modeli:

**VGG16 FVEI Block5 Fine-Tuned**

Checkpoint:

`vgg16_fvei_block5_best.pth`

Seçilen epoch:

**12**

Final sonuçlar:

- Validation MAE: **26.4428 m**
- Held-out Test MAE: **25.1347 m**
- Held-out Test RMSE: **38.4440 m**
- Held-out Test R²: **0.894442**
- Held-out Test Bias: **+3.4534 m**

---

# 18. WEB TABANLI PROTOTİP

Araştırma önerisinde planlanan Flask tabanlı prototip geliştirilmiştir.

Nihai prototip:

- `GET /`
- `GET /health`
- `POST /predict`

endpoint'lerini içermektedir.

Kullanıcı:

1. görüntü yükleyebilmekte,
2. görüntüyü web arayüzünde görebilmekte,
3. model inference işlemini başlatabilmekte,
4. görüş mesafesi tahminini metre cinsinden alabilmektedir.

Web arayüzünün inference pipeline'ı nihai:

**VGG16 FVEI Block5 Fine-Tuned**

modelini kullanmaktadır.

API test paketi:

**6 / 6 passed**

sonucunu vermiştir.

Gerçek checkpoint ile gerçekleştirilen ayrı smoke testte `/predict` endpoint'i HTTP 200 yanıtı üretmiş ve model inference zincirinin uçtan uca çalıştığı doğrulanmıştır.

---

# 19. İŞ PAKETLERİNİN GERÇEKLEŞME DURUMU

| İş Paketi | Önerilen Hedef | Gerçekleşen Durum |
|---|---|---|
| İP1 | Ortam kurulumu ve veri hazırlığı | **Tamamlandı.** FRIDA/FRIDA2 pipeline, preprocessing, scene split ve DataLoader geliştirildi. |
| İP2 | VGG16/ResNet50 geliştirme ve MAE karşılaştırması | **Tamamlandı.** VGG16 66.7227 m, ResNet50 124.6181 m test MAE elde etti. |
| İP3 | Attention optimizasyonu ve Flask prototipi | **Tamamlandı.** CBAM ve SE denendi; baseline test MAE iyileşmedi. Flask prototipi geliştirildi. |
| İP4 | Gerçek dünya fine-tuning ve MAE < 100 m | **Tamamlandı.** FVEI üzerinde final Test MAE 25.1347 m elde edildi. |
| İP5 | Nihai test, değerlendirme ve raporlama | **Büyük ölçüde tamamlandı.** Locked test, hata analizi, API testleri, repo ve teknik raporlar tamamlandı. TÜBİTAK final raporu ve yayın taslağı hazırlık aşamasındadır. |

---

# 20. RİSK YÖNETİMİNİN GERÇEKLEŞME DURUMU

## Risk 1 — Gerçek Dünya Verisine Erişim

Öneride FVEI/FHVI erişiminin kısıtlı olması bir risk olarak tanımlanmıştır.

FVEI verisine ulaşılana kadar:

- FRIDA/FRIDA2 ana sentetik karşılaştırması tamamlanmış,
- CIDET yardımcı gerçek dünya veri kaynağı olarak kullanılmış,
- Benchmark-Visibility üzerinde ek stress test yapılmıştır.

Daha sonra FVEI verisi projeye başarıyla dahil edilmiştir.

FHVI final model geliştirme sürecinde kullanılmamıştır.

---

## Risk 2 — MAE Hedefine Ulaşılamaması

Öneride kritik eşik olarak **MAE < 100 m** hedefi belirlenmiştir.

Bu hedef:

- sentetik VGG16 testinde **66.7227 m**,
- FVEI gerçek dünya testinde **25.1347 m**

ile karşılanmıştır.

Bu nedenle ilgili B planına geçilmesine ihtiyaç duyulmamıştır.

---

## Risk 3 — Flask Entegrasyon Sorunları

Öneride entegrasyon zorluğu halinde daha basit fonksiyonel Python arayüzüne geçilebileceği belirtilmiştir.

Flask tabanlı API ve web arayüzü başarıyla tamamlandığından bu B planına ihtiyaç duyulmamıştır.

---

## Risk 4 — Attention Mekanizmasının İyileşme Sağlamaması

Bu risk proje sırasında gerçekleşmiştir.

CBAM test MAE:

**67.6214 m**

VGG16 baseline test MAE:

**66.7227 m**

olduğundan CBAM nihai test metriğini iyileştirmemiştir.

Öneride tanımlanan B planına uygun olarak SE attention uygulanmıştır.

SE test MAE:

**72.4412 m**

olarak ölçülmüş ve bu yöntem de baseline'ı geçememiştir.

Böylece risk planında tanımlanan alternatif teknik yaklaşım uygulanmış ve sonucu deneysel olarak raporlanmıştır.

---

# 21. PROJE HEDEFLERİNE ULAŞMA DURUMU

| Hedef | Durum |
|---|:---:|
| VGG16 adaptasyonu | ✅ |
| ResNet50 adaptasyonu | ✅ |
| Karşılaştırmalı baseline analizi | ✅ |
| En iyi temel modelin belirlenmesi | ✅ |
| Attention mekanizması uygulanması | ✅ |
| Attention alternatif B planının uygulanması | ✅ |
| Gerçek dünya verisinin entegrasyonu | ✅ |
| MAE < 100 m | ✅ |
| Final held-out test | ✅ |
| Flask API | ✅ |
| Web arayüzü | ✅ |
| Teknik dokümantasyon | ✅ |
| Akademik yayın / makale taslağı | ⏳ Hazırlanacak |

---

# 22. BİLİMSEL BULGULARIN GENEL DEĞERLENDİRMESİ

Çalışmanın en önemli bulgularından biri, daha derin ResNet50 mimarisinin mevcut görüş mesafesi regresyon problemi ve deney koşullarında VGG16'dan daha yüksek hata üretmesidir.

Bu sonuç, mimari karmaşıklığın tek başına daha yüksek regresyon başarısı garanti etmediğini göstermektedir.

İkinci önemli bulgu, attention mekanizmalarının teknik olarak başarıyla entegre edilmesine rağmen held-out test MAE değerini iyileştirmemesidir.

CBAM validation performansında küçük bir iyileşme üretmiş olsa da test performansında baseline modelin gerisinde kalmıştır. Alternatif SE mekanizması da baseline'ı geçememiştir.

Üçüncü önemli bulgu sentetik ve gerçek dünya veri dağılımları arasındaki domain farklılığıdır. CIDET ve Benchmark-Visibility deneyleri özellikle hedef aralığının genişlediği koşullarda prediction-range compression ve yüksek görüş mesafelerinde underestimation davranışını ortaya koymuştur.

FVEI üzerinde doğrudan fine-tuning uygulanması ise gerçek dünya test MAE değerini 25.1347 m seviyesine taşımıştır.

Bu sonuç, transfer öğrenmede hedef veri dağılımına özgü adaptasyonun önemini göstermektedir.

---

# 23. SINIRLILIKLAR

Çalışmanın sonuçları değerlendirilirken aşağıdaki sınırlılıklar dikkate alınmalıdır:

1. Ana deneyler tek random seed ve ana veri ayrımı üzerinden yürütülmüştür.
2. Sonuçlar için çoklu seed veya cross-validation tabanlı istatistiksel anlamlılık analizi gerçekleştirilmemiştir.
3. FVEI verisinde güvenilir scene/camera identity bilgileri mevcut pipeline'da bulunmadığından residual örnek bağımlılığı tamamen dışlanamamaktadır.
4. 500 m etiketli FVEI grubunun ceiling/censored semantiği bağımsız kaynak dokümantasyonu ile doğrulanmadan exact-label regresyon metriği olarak kullanılmamıştır.
5. Benchmark-Visibility veri setinin hedef aralığı eğitim verisinden çok daha geniş olduğundan bu deney doğrudan aynı dağılımdaki performans karşılaştırması olarak değerlendirilmemektedir.
6. FHVI veri seti final çalışma kapsamında kullanılamamıştır.
7. CUDA tarafında bazı operasyonların strict deterministic implementation sunmaması nedeniyle bit-bit aynı GPU sonucu garanti edilmemektedir.
8. Flask prototipi araştırma ve gösterim amaçlıdır; üretim ortamına yönelik güvenlik, ölçeklenebilirlik ve deployment optimizasyonu projenin kapsamı dışındadır.

---

# 24. PROJE ÇIKTILARI

## 24.1 Bilimsel / Akademik Çıktılar

Proje kapsamında:

- VGG16–ResNet50 karşılaştırmalı analiz sonuçları,
- CBAM ve SE attention deneyleri,
- sentetik-gerçek dünya domain geçişi incelemesi,
- FVEI fine-tuning ve held-out test sonuçları,
- level-wise hata analizi

üretilmiştir.

Bu sonuçların akademik makale veya bildiri formatına dönüştürülmesi planlanmaktadır.

Henüz yayınlanmış veya kabul edilmiş bir makale olduğu iddia edilmemektedir.

---

## 24.2 Yazılım ve Prototip Çıktıları

Aşağıdaki teknik çıktılar geliştirilmiştir:

- veri hazırlama pipeline'ı,
- scene-based sentetik split,
- VGG16 training ve evaluation pipeline,
- ResNet50 training ve evaluation pipeline,
- CBAM attention modeli,
- SE attention modeli,
- CIDET gerçek dünya adaptation pipeline,
- Benchmark-Visibility stress test,
- FVEI audit pipeline,
- FVEI stratified split ve similarity screening,
- FVEI DataLoader,
- FVEI fine-tuning pipeline,
- final held-out test evaluation pipeline,
- sonuç grafikleri üretim script'i,
- Flask API,
- HTML/CSS web arayüzü,
- otomatik API testleri,
- teknik araştırma günlüğü ve deney raporları.

---

# 25. YAYGIN ETKİ

Proje, mevcut kamera görüntülerinden görüş mesafesi tahmini yapılabileceğini gösteren düşük maliyetli bir araştırma prototipi ortaya koymuştur.

Elde edilen model ve Flask tabanlı prototip, daha ileri çalışmalar için:

- yol gözetleme kameraları,
- sis algılama sistemleri,
- erken uyarı uygulamaları,
- Akıllı Ulaşım Sistemleri,
- gerçek zamanlı görüntü tabanlı meteorolojik analiz

alanlarında başlangıç noktası oluşturabilecek niteliktedir.

Bununla birlikte mevcut prototip araştırma amaçlıdır ve gerçek trafik güvenliği uygulamasında doğrudan kullanılmadan önce daha büyük ve bağımsız veri setlerinde ek doğrulama yapılması gerekmektedir.

---

# 26. SONUÇ

Bu çalışmada transfer öğrenme tabanlı CNN mimarilerinin sisli görüntülerden görüş mesafesi tahminindeki performansı sistematik olarak incelenmiştir.

Sentetik FRIDA/FRIDA2 deneylerinde VGG16 modeli **66.7227 m Test MAE** ile ResNet50 modelinden daha düşük hata üretmiştir.

Başlangıç araştırma hipotezinin aksine ResNet50 daha başarılı olmamış ve mevcut deney düzeninde VGG16 temel model olarak seçilmiştir.

VGG16 üzerine entegre edilen CBAM ve SE attention mekanizmaları teknik olarak başarıyla uygulanmış ancak held-out test MAE değerini iyileştirmemiştir.

Gerçek dünya adaptasyonu kapsamında FVEI verisi üzerinde gerçekleştirilen fine-tuning sonucunda validation MAE **26.4428 m** seviyesine ulaşmış ve epoch 12 nihai checkpoint olarak seçilmiştir.

Bağımsız locked FVEI test değerlendirmesinde:

- MAE: **25.1347 m**
- RMSE: **38.4440 m**
- R²: **0.894442**
- Bias: **+3.4534 m**

elde edilmiştir.

Böylece proje önerisinde belirlenen **MAE < 100 m** gerçek dünya performans hedefi karşılanmıştır.

Nihai model Flask API ve web arayüzüne entegre edilerek görüntüden görüş mesafesi tahmini yapan fonksiyonel bir prototip geliştirilmiştir.

Sonuç olarak proje, öneride belirtilen temel model karşılaştırması, attention değerlendirmesi, gerçek dünya adaptasyonu, nicel performans analizi ve fonksiyonel prototip geliştirme hedeflerinin büyük bölümünü gerçekleştirmiştir.

---

# 27. NİHAİ RAPORA AKTARILACAK TEMEL SAYILAR

| Sonuç | Değer |
|---|---:|
| Sentetik veri | 672 görüntü / 84 sahne |
| VGG16 Test MAE | **66.7227 m** |
| ResNet50 Test MAE | **124.6181 m** |
| CBAM Test MAE | **67.6214 m** |
| SE Test MAE | **72.4412 m** |
| FVEI Train | 2245 |
| FVEI Validation | 480 |
| FVEI Locked Test | 482 |
| Selected Epoch | 12 |
| FVEI Validation MAE | **26.4428 m** |
| FVEI Test MAE | **25.1347 m** |
| FVEI Test RMSE | **38.4440 m** |
| FVEI Test R² | **0.894442** |
| FVEI Test Bias | **+3.4534 m** |
| Flask automated tests | **6 / 6 passed** |

---

# 28. RAPORLAMA İÇİN KULLANILACAK ŞEKİLLER

1. `figures/visibility_levels_sample.png`
2. `figures/synthetic_model_test_mae_comparison.png`
3. `figures/fvei_finetuning_mae_curve.png`
4. `figures/fvei_levelwise_error_comparison.png`

---

# 29. KAYNAKÇA NOTU

Nihai resmi raporda kaynakça hazırlanırken araştırma önerisi formundaki kaynaklar temel alınacaktır.

FVEI veri setinin özellikle 500 m etiket semantiğine ilişkin kaynak bilgisi, bilimsel yayın veya resmi veri seti dokümantasyonu üzerinden ayrıca doğrulanmadan kesin metodolojik iddia olarak yazılmamalıdır.

Kaynakların bibliyografik biçimi final rapor tesliminden önce tek formatta düzenlenmelidir.

---

# 30. SONRAKİ RAPORLAMA ADIMI

Bu içerik taslağı aşağıdaki işlemler için ana kaynak olacaktır:

1. Resmi TÜBİTAK sonuç raporu formuna aktarım,
2. şekil ve tabloların rapora yerleştirilmesi,
3. akademik dil ve uzunluk optimizasyonu,
4. kaynakça doğrulaması,
5. danışman incelemesi,
6. nihai PDF hazırlanması.
