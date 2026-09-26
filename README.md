# Fog Visibility Estimation using Transfer Learning

TÜBİTAK 2209-A kapsamında yürütülen bu araştırma projesi, sisli hava koşullarında görüntü tabanlı **sürekli görüş mesafesi tahmini** için transfer öğrenme tabanlı CNN mimarilerini incelemektedir.

Çalışmada ilk olarak **VGG16** ve **ResNet50** mimarileri FRIDA/FRIDA2 tabanlı sentetik veri üzerinde karşılaştırılmıştır. Ardından attention mekanizmalarının etkisi **CBAM** ve **SE** modelleri üzerinden incelenmiş, gerçek dünya genellemesi **CIDET** veri seti üzerinde araştırılmış ve bağımsız dış değerlendirme **Benchmark-Visibility** veri seti üzerinde gerçekleştirilmiştir.

Projenin güncel aşamasında eğitilmiş modelin görüntü üzerinden görüş mesafesi tahmini yapmasını sağlayan **Flask tabanlı web prototipi** de geliştirilmiştir.

---

# TÜBİTAK 2209-A Araştırma Projesi

## Proje Başlığı

> **Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi**

## Araştırmanın Amacı

Projenin temel amaçları:

- görüntülerden sürekli görüş mesafesi tahmini gerçekleştirmek,
- transfer öğrenme ile VGG16 ve ResNet50 mimarilerini karşılaştırmak,
- seçilen temel model üzerinde attention mekanizmalarının etkisini incelemek,
- sentetik ve gerçek dünya verileri arasındaki genelleme farkını araştırmak,
- gerçek dünya verileri üzerinde kontrollü fine-tuning stratejilerini değerlendirmek,
- bağımsız bir veri seti üzerinde cross-dataset generalization davranışını incelemek,
- eğitilmiş modeli Flask tabanlı bir web prototipine entegre etmektir.

Temel performans metriği **Mean Absolute Error (MAE)** olarak belirlenmiştir.

---

# Araştırma Akışı

FRIDA / FRIDA2  
↓  
Synthetic Baseline Comparison — VGG16 vs ResNet50  
↓  
Attention Experiments — CBAM + SE  
↓  
Real-World Adaptation — CIDET  
↓  
Independent External Evaluation — Benchmark-Visibility  
↓  
Flask Inference Prototype

FVEI veri setine erişim için ayrıca ilgili çalışmanın yazarına veri erişim talebi gönderilmiştir.

---

# 1. Sentetik Veri: FRIDA / FRIDA2

Projenin kontrollü mimari karşılaştırması FRIDA ve FRIDA2 tabanlı sentetik sis görüntüleri üzerinde gerçekleştirilmiştir.

## Görüş Mesafesi Seviyeleri

50 m, 80 m, 100 m, 150 m, 200 m, 300 m, 500 m ve 800 m.

## Veri Kümesi

| Özellik | Değer |
|---|---:|
| FRIDA temel sahne | 18 |
| FRIDA2 temel sahne | 66 |
| Toplam sahne | 84 |
| Görüş mesafesi seviyesi | 8 |
| Toplam görüntü | 672 |

Aynı temel sahneye ait farklı sis seviyelerinin farklı veri bölümlerine dağılmasını engellemek amacıyla **scene-based splitting** uygulanmıştır.

| Split | Görüntü |
|---|---:|
| Train | 464 |
| Validation | 96 |
| Test | 112 |

Deneylerin tekrarlanabilirliği için **Random Seed = 42** kullanılmıştır.

---

# 2. Synthetic Baseline Comparison

ImageNet üzerinde önceden eğitilmiş VGG16 ve ResNet50 modelleri sürekli görüş mesafesi regresyonuna uyarlanmıştır.

Baseline deneylerinde convolutional backbone dondurulmuş ve classifier bölümü regresyon head'i ile değiştirilmiştir.

## VGG16

| Metrik | Sonuç |
|---|---:|
| Best Epoch | 18 |
| Validation MAE | 69.9705 m |
| Test MAE | **66.7227 m** |
| Mean Signed Error | -17.3877 m |
| Maximum Absolute Error | 392.8829 m |

VGG16, sentetik test kümesinde proje kapsamında hedeflenen **MAE < 100 m** kriterini karşılamıştır.

## ResNet50

| Metrik | Sonuç |
|---|---:|
| Best Epoch | 20 |
| Validation MAE | 121.8414 m |
| Test MAE | **124.6181 m** |
| Mean Signed Error | -77.3460 m |

## Karşılaştırma

| Model | Validation MAE | Test MAE |
|---|---:|---:|
| **VGG16** | **69.9705 m** | **66.7227 m** |
| ResNet50 | 121.8414 m | 124.6181 m |

Mevcut kontrollü sentetik deney koşullarında VGG16 daha düşük MAE üretmiştir.

Bu nedenle **Selected Synthetic Baseline: VGG16** olarak belirlenmiştir.

Bu sonuç VGG16'nın genel olarak ResNet50'den üstün olduğu anlamına gelmemektedir; sonuç yalnızca mevcut veri, split ve deney koşulları için geçerlidir.

---

# 3. Attention Experiments

Sentetik baseline karşılaştırmasının ardından VGG16 üzerinde attention mekanizmalarının etkisi incelenmiştir.

İki farklı yaklaşım değerlendirilmiştir:

- CBAM — Convolutional Block Attention Module
- SE — Squeeze-and-Excitation

## Sentetik Test Sonuçları

| Model | Test MAE |
|---|---:|
| **VGG16 Baseline** | **66.7227 m** |
| VGG16 + CBAM | 67.6214 m |
| VGG16 + SE | 72.4412 m |
| ResNet50 Baseline | 124.6181 m |

Attention mekanizmaları modele başarıyla entegre edilmiş olsa da mevcut sentetik test koşullarında VGG16 baseline'ın test MAE değerini iyileştirmemiştir.

Dolayısıyla attention entegrasyonu teknik olarak başarıyla gerçekleştirilmiş, ancak performans açısından baseline VGG16 en düşük sentetik test MAE değerini korumuştur.

Tek bir random seed ve tek bir split kullanıldığı için küçük performans farkları için istatistiksel anlamlılık iddiasında bulunulmamaktadır.

---

# 4. Real-World Evaluation: CIDET

Sentetik ortamda gerçekleştirilen kontrollü deneylerin ardından gerçek dünya genellemesi **CIDET** veri seti üzerinde incelenmiştir.

CIDET; gerçek dünya gözetim kamerası görüntülerini, profesyonel meteoroloji istasyonu ölçümlerini ve metre cinsinden manuel görüş mesafesi anotasyonlarını içermektedir.

Veri setindeki geçerli örnekler üzerinde zaman kaynaklı veri sızıntısını azaltmak amacıyla **day-grouped temporal split** oluşturulmuştur.

## CIDET Temporal Split

| Split | Örnek | Oran |
|---|---:|---:|
| Train | 685 | 70.11% |
| Validation | 147 | 15.05% |
| Test | 145 | 14.84% |

Split'ler arasında tarih çakışması bulunmamaktadır.

CIDET görüş mesafesi aralığı yaklaşık **84–3915 m** seviyesindedir.

---

# 5. Synthetic → Real-World Zero-Shot Transfer

Sentetik FRIDA/FRIDA2 üzerinde eğitilmiş VGG16 modeli ilk olarak CIDET test görüntülerine herhangi bir adaptasyon yapılmadan uygulanmıştır.

| Metrik | Sonuç |
|---|---:|
| MAE | 2258.8934 m |
| RMSE | 2472.9176 m |
| Median Absolute Error | 2778.4081 m |
| Mean Signed Error | -2258.8851 m |

Bu sonuç sentetik ve gerçek dünya görüntüleri arasında ciddi bir **domain shift** ve target-range shift bulunduğunu göstermiştir.

Bu nedenle gerçek dünya adaptasyonu için kontrollü fine-tuning deneyleri gerçekleştirilmiştir.

---

# 6. CIDET Fine-Tuning Experiments

CIDET üzerinde birden fazla kontrollü adaptasyon stratejisi değerlendirilmiştir.

## Experiment 1 — Head-Only Fine-Tuning

Synthetic VGG16 checkpoint'i başlangıç noktası olarak kullanılmış ve convolutional backbone dondurularak yalnızca regression head eğitilmiştir.

**Validation MAE: 446.5714 m**

## Experiment 2 — Block5 Fine-Tuning

VGG16'nın Blocks 1–4 bölümleri dondurulmuş, Block5 ve regression head birlikte eğitilmiştir.

**Validation MAE: 326.6640 m**

## Experiment 3 — Balanced Sampling

Block5 fine-tuning stratejisine visibility-range tabanlı weighted sampling eklenmiştir.

**Validation MAE: 334.9808 m**

Balanced sampling mevcut deney koşullarında standart sampling yaklaşımını iyileştirmemiştir.

## Experiment 4 — Block5 + Huber Loss

Block5 ve regression head birlikte eğitilmiş ve L1Loss yerine Huber tabanlı SmoothL1Loss kullanılmıştır.

**Huber Beta: 200**

**Validation MAE: 324.1948 m**

---

# 7. CIDET Validation Comparison

| Adaptasyon Stratejisi | Validation MAE |
|---|---:|
| Head-only + L1 | 446.5714 m |
| Block5 + L1 | 326.6640 m |
| Block5 + Balanced Sampling + L1 | 334.9808 m |
| **Block5 + Huber** | **324.1948 m** |

Block5 + Huber modeli mevcut CIDET geliştirme deneyleri içerisinde gözlenen en düşük validation MAE değerini üretmiştir.

Bununla birlikte Block5 + L1 modeline göre fark yalnızca yaklaşık **2.47 m (%0.76)** seviyesindedir.

Bu nedenle sonuç güçlü veya istatistiksel olarak anlamlı bir üstünlük olarak yorumlanmamaktadır.

Güncel CIDET development checkpoint:

> **VGG16 + Block5 Fine-Tuning + Huber Loss**

olarak tutulmaktadır.

---

# 8. CIDET Error Analysis

Block5 + Huber modeli için CIDET validation sonuçları:

| Metrik | Sonuç |
|---|---:|
| MAE | 324.1948 m |
| RMSE | 490.3078 m |
| Median Absolute Error | 211.4893 m |
| Mean Signed Error | -53.6124 m |
| Pearson Correlation | 0.897810 |

Validation setinde bazı günlerde ve meteorolojik koşullarda daha yüksek tahmin hataları gözlenmiştir.

Bu ilişkiler korelasyon düzeyinde değerlendirilmekte ve nedensellik iddiasında bulunulmamaktadır.

CIDET üzerinde proje hedefi olan **MAE < 100 m** seviyesine ulaşılamamıştır.

Buna karşılık sentetik FRIDA/FRIDA2 test kümesinde VGG16 baseline ile **Test MAE = 66.7227 m** elde edilerek bu hedef sentetik deney koşullarında karşılanmıştır.

---

# 9. Independent External Evaluation: Benchmark-Visibility

CIDET üzerinde model geliştirme tamamlandıktan sonra mevcut checkpoint'in bağımsız bir veri setindeki davranışını incelemek amacıyla **Benchmark-Visibility** kullanılmıştır.

Bu değerlendirmede Benchmark-Visibility; model eğitimi, fine-tuning, calibration, hyperparameter selection veya checkpoint selection için kullanılmamıştır.

Dolayısıyla deney bağımsız bir **cross-dataset external evaluation / stress test** olarak gerçekleştirilmiştir.

## Dataset

| Özellik | Değer |
|---|---:|
| Görüntü | 1856 |
| Gün | 29 |
| Minimum Visibility | 112 m |
| Median Visibility | 12562.5 m |
| Maximum Visibility | 20000 m |

Benchmark-Visibility'ın hedef aralığı CIDET'ten çok daha geniştir:

**CIDET:** yaklaşık 84–3915 m  
**Benchmark-Visibility:** 112–20000 m

---

# 10. Benchmark-Visibility Results

CIDET validation sonucuna göre önceden seçilmiş Block5 + Huber checkpoint'i hiçbir ek adaptasyon yapılmadan Benchmark-Visibility üzerinde değerlendirilmiştir.

| Metrik | Sonuç |
|---|---:|
| MAE | 11314.7801 m |
| RMSE | 13148.0802 m |
| Median Absolute Error | 11981.6470 m |
| Mean Signed Error | -11310.9893 m |
| Pearson Correlation | 0.585183 |
| Prediction Range | 97.43–1308.30 m |
| Target Range | 112–20000 m |

Model özellikle yüksek görüş mesafelerinde ciddi sistematik düşük tahmin davranışı göstermiştir.

Model prediction range'i yaklaşık **97–1308 m** arasında sıkışırken gerçek hedefler **112–20000 m** arasında değişmektedir.

Bu sonuç modelin CIDET üzerinde öğrendiği mutlak görüş mesafesi ölçeğini çok daha geniş Benchmark-Visibility dağılımına taşıyamadığını göstermektedir.

Pearson korelasyonunun pozitif olması bazı sıralama bilgisinin transfer edildiğine işaret etse de bu durum başarılı mutlak metrik kalibrasyonu anlamına gelmemektedir.

Benchmark sonucu model seçimini değiştirmek veya yeni hyperparameter tuning yapmak için kullanılmamıştır.

Negatif external evaluation sonucu araştırmanın cross-dataset generalization bulgusu olarak korunmaktadır.

---

# 11. FVEI Dataset Access

Proje önerisinde gerçek dünya değerlendirmesi için planlanan veri kaynaklarından biri FVEI veri setidir.

FVEI veri paylaşım bağlantısına teknik erişim sağlanamadığı için ilgili çalışmanın yazarına veri erişim talebi gönderilmiştir.

Yanıt beklenirken gerçek dünya deneyleri erişilebilir CIDET veri seti üzerinde yürütülmüş ve bağımsız cross-dataset değerlendirmesi Benchmark-Visibility üzerinde gerçekleştirilmiştir.

FVEI erişimi sağlanırsa veri seti ayrıca proposal-aligned external real-world evaluation amacıyla projeye dahil edilecektir.

---

# 12. Flask Web Prototype

Eğitilmiş modelin gerçek görüntüler üzerinde kullanılabilmesi için Flask tabanlı bir inference prototipi geliştirilmiştir.

Web uygulaması:

- JPG / JPEG / PNG görüntü yükleme,
- görüntü önizleme,
- model inference,
- metre cinsinden görüş mesafesi tahmini,
- REST-style prediction endpoint,
- model health endpoint

özelliklerini desteklemektedir.

## Kullanılan Model

Web prototipi güncel CIDET development checkpoint'ini kullanmaktadır:

> **VGG16 + CIDET Block5 Fine-Tuning + Huber Loss**

Model checkpoint'i CIDET validation performansına göre seçilmiştir.

## API Endpoints

- `GET /`
- `GET /health`
- `POST /predict`

`/predict` endpoint'i multipart form üzerinden `image` alanını kabul etmektedir.

Örnek JSON çıktı:

{
  "visibility_m": 3333.15,
  "unit": "m",
  "model": "VGG16 CIDET Block5 Huber",
  "checkpoint_epoch": 12
}

Web arayüzünde araştırma MAE değerleri tek bir görüntünün hata payı olarak yanlış yorumlanmaması için prediction sonucu ile birlikte gösterilmemektedir.

---

# 13. Preprocessing

Model inference pipeline'ında:

RGB Conversion  
↓  
Resize 224 × 224  
↓  
ToTensor  
↓  
ImageNet Normalization  
↓  
VGG16  
↓  
Visibility Regression

uygulanmaktadır.

ImageNet normalization değerleri:

- Mean = `[0.485, 0.456, 0.406]`
- Std = `[0.229, 0.224, 0.225]`

---

# 14. Technology Stack

- Python
- PyTorch
- Torchvision
- Flask
- Pillow
- NumPy
- Pandas
- SciPy
- Scikit-learn
- Matplotlib
- OpenCV
- HTML
- CSS
- JavaScript

---

# 15. Repository Structure

.
├── data/
│   ├── generated/
│   ├── interim/
│   ├── processed/
│   ├── raw/
│   └── splits/
├── docs/
│   ├── literature/
│   ├── research_notes/
│   └── reports/
├── figures/
├── notebooks/
├── results/
├── src/
│   ├── api/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── app.py
│   │   └── inference.py
│   ├── data/
│   ├── evaluation/
│   ├── models/
│   └── training/
├── README.md
└── requirements.txt

---

# 16. Important Research Reports

Detaylı deney kayıtları `docs/reports/` altında tutulmaktadır.

Önemli raporlar:

- `docs/reports/baseline_comparison.md`
- `docs/reports/attention_comparison.md`
- `docs/reports/se_attention_comparison.md`
- `docs/reports/cidet_real_world_evaluation.md`
- `docs/reports/benchmark_visibility_external_evaluation.md`

Araştırma sürecine ait ayrıntılı geliştirme notları `docs/research_notes/arastirma_gunlugu.md` dosyasında tutulmaktadır.

---

# 17. Current Research Findings

1. VGG16, mevcut sentetik FRIDA/FRIDA2 deneylerinde ResNet50'den daha düşük MAE üretmiştir.

2. Sentetik VGG16 baseline test MAE değeri **66.7227 m** olmuş ve sentetik ortamda MAE < 100 m hedefi karşılanmıştır.

3. CBAM ve SE attention mekanizmaları başarıyla uygulanmış ancak mevcut sentetik test koşullarında VGG16 baseline performansını iyileştirmemiştir.

4. Sentetik modelin CIDET'e zero-shot aktarımında ciddi domain ve target-range shift gözlenmiştir.

5. CIDET üzerinde kontrollü fine-tuning, zero-shot performansa göre önemli iyileşme sağlamıştır.

6. Mevcut CIDET geliştirme deneylerinde en düşük validation MAE **324.1948 m** ile Block5 + Huber modelinde gözlenmiştir.

7. CIDET gerçek dünya validation setinde MAE < 100 m hedefi karşılanmamıştır.

8. Benchmark-Visibility external evaluation, modelin çok daha geniş görüş mesafesi dağılımında prediction-range compression ve sistematik düşük tahmin davranışı gösterdiğini ortaya koymuştur.

9. Benchmark sonucu model geliştirme amacıyla kullanılmamış ve negatif cross-dataset sonucu araştırma bulgusu olarak korunmuştur.

10. Güncel CIDET checkpoint'i Flask tabanlı çalışan web prototipine entegre edilmiştir.

---

# 18. Completed Work

- [x] Literature review
- [x] FRIDA / FRIDA2 analysis
- [x] Synthetic fog generation pipeline
- [x] Synthetic dataset generation
- [x] Scene-based splitting
- [x] Shared preprocessing pipeline
- [x] VGG16 baseline
- [x] ResNet50 baseline
- [x] Baseline evaluation
- [x] VGG16 vs ResNet50 comparison
- [x] Synthetic baseline selection
- [x] CBAM implementation
- [x] CBAM training and evaluation
- [x] SE implementation
- [x] SE training and evaluation
- [x] Attention comparison
- [x] CIDET dataset audit
- [x] CIDET temporal split
- [x] Synthetic → CIDET zero-shot evaluation
- [x] CIDET head-only fine-tuning
- [x] CIDET Block5 fine-tuning
- [x] Balanced sampling experiment
- [x] Huber loss experiment
- [x] CIDET validation error analysis
- [x] Meteorological association analysis
- [x] Benchmark-Visibility dataset audit
- [x] Independent Benchmark external evaluation
- [x] Model inference wrapper
- [x] Flask inference API
- [x] Web interface
- [x] Image upload and prediction workflow
- [x] Flask API integration tests

---

# 19. Remaining Work

Ana deneysel geliştirme büyük ölçüde tamamlanmıştır.

Kalan temel çalışmalar:

- [ ] FVEI erişim talebinin sonucunun takip edilmesi
- [ ] FVEI erişimi sağlanırsa ek external real-world evaluation
- [ ] Final TÜBİTAK project report
- [ ] Research paper / publication-oriented manuscript
- [ ] Final figures and result tables
- [ ] Final project documentation

FVEI erişiminin sağlanmaması durumunda mevcut CIDET ve Benchmark-Visibility deneyleri gerçek dünya ve cross-dataset değerlendirme bulguları olarak raporlanacaktır.

---

# 20. Reproducibility

Kontrollü deneylerde temel random seed **42** olarak kullanılmıştır.

Mümkün olan deneylerde:

- aynı veri split'leri,
- aynı preprocessing pipeline,
- aynı temel model initialization,
- kontrollü optimizer ayarları,
- ayrı checkpoint'ler,
- validation-based model selection

kullanılarak karşılaştırmaların tekrarlanabilirliği korunmaya çalışılmıştır.

Benchmark-Visibility değerlendirmesinde model seçimi veya tuning yapılmamış, checkpoint değerlendirmeden önce sabitlenmiştir.

---

# 21. Methodological Notes

Sonuçlar yorumlanırken aşağıdaki noktalar dikkate alınmalıdır:

- Sentetik ve gerçek dünya MAE değerleri doğrudan aynı dağılımın performansı olarak yorumlanmamalıdır.
- FRIDA/FRIDA2 görüş mesafesi aralığı 50–800 m'dir.
- CIDET yaklaşık 84–3915 m aralığındadır.
- Benchmark-Visibility 112–20000 m aralığındadır.
- CIDET development experiments aynı validation split üzerinde karşılaştırılmıştır.
- Küçük validation farkları istatistiksel üstünlük olarak yorumlanmamaktadır.
- Benchmark-Visibility yalnızca bağımsız external evaluation amacıyla kullanılmıştır.
- Tek seed/split ile elde edilen sentetik sonuçlar için istatistiksel anlamlılık iddiasında bulunulmamaktadır.

---

# 22. Disclaimer

Bu repository aktif olarak geliştirilen akademik bir TÜBİTAK 2209-A araştırma projesini içermektedir.

Model performansı kullanılan veri setine ve görüş mesafesi dağılımına önemli ölçüde bağlıdır.

Web prototipinden elde edilen tekil tahminler bir meteorolojik görüş sensörünün veya sertifikalı ölçüm sisteminin yerine geçmemektedir.

Repository'de raporlanan MAE değerleri ilgili deney veri setlerinin toplu performans metrikleridir ve web arayüzünde yüklenen tek bir görüntünün hata payını temsil etmez.

---

# License and Dataset Usage

Bu proje TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı kapsamında akademik araştırma amacıyla geliştirilmektedir.

Kullanılan üçüncü taraf veri setlerinin kendi lisans ve kullanım koşulları geçerlidir.

Özellikle Benchmark-Visibility kaynak materyalinde akademik / nonprofit kullanım kısıtları bulunduğundan ilgili veri seti ve kaynak kodları kendi kaynak koşulları kapsamında değerlendirilmelidir.

Bu repository kapsamında proje için özgün olarak geliştirilen yazılım ve dokümantasyon **MIT License** altında lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakınız.

Üçüncü taraf veri setleri, kaynak materyalleri, önceden eğitilmiş model bileşenleri ve diğer üçüncü taraf kaynaklar MIT License kapsamında yeniden lisanslanmamaktadır; bunların kendi lisans, atıf ve kullanım koşulları geçerlidir.
