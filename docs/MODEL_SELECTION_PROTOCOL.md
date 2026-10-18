# Model Seçim Protokolü (Ön Kayıt)

**Tarih:** 18.10.2026. Bu protokol, erken durdurmalı yakınsama deneyleri (`vgg16_e200_p20`, `resnet50_e200_p20`) çalıştırılmadan **önce** yazılmış ve commit edilmiştir. Sonuçlar görüldükten sonra kural, ölçüt veya eşik değiştirilmez.

**Kayıt kapsamı:** 20 ve 50 epoch'luk sonuçlar bu protokol yazılmadan önce görülmüştür. Ön kayıt yalnızca yeni erken durdurmalı deneyleri kapsar. Aynı 14 sahnelik sentetik test bölmesi daha önce kullanıldığından yeni sonuçlar, tamamen yeni ve daha önce görülmemiş bir test kümesinde bağımsız doğrulama olarak sunulmaz.

---

## 1. Araştırma önerisindeki dayanak

| Önerideki ifade | Bölüm | Protokoldeki karşılığı |
|---|---|---|
| "Eğitilen modeller arasından test veri seti üzerinde en düşük MAE değerini veren modeli seçmek" | 1.2 Amaç ve Hedefler; Yöntem 1.4 | Birincil ölçüt: test MAE |
| "TL yöntemi ile … adapte edilen VGG16 ve ResNet50 mimarilerinden hangisi, sentetik ve gerçek dünya veri kümelerinde en düşük MAE değerini sunarak AUS entegrasyonu için daha uygun bir temel oluşturur?" | Araştırma sorusu | Sentetik (birincil) ve FVEI (ikincil) birlikte raporlanır |
| ResNet50'nin "aynı veri seti ve eğitim parametreleri altında VGG16 mimarisine kıyasla istatistiksel olarak anlamlı düzeyde daha düşük MAE değerleri üretmesi" | Hipotez | Eşleştirilmiş anlamlılık testi + aynı eğitim parametreleri |
| Doğrulama kümesi "hiper-parametre ayarlarının (erken durdurma) yapılması için kullanılacaktır" | Yöntem 1.2 | Validation tabanlı erken durdurma |
| Derin evrişim katmanları dondurulur, yalnızca regresyon başlığı eğitilir; kayıp MAE | Yöntem 1.3 | Omurga dondurulmuş, başlık eğitilir, L1 kayıp |
| "AUS için düşük karmaşıklıktaki, en iyi genelleme yeteneğine sahip hazır ağın belirlenmesi" | Özet (1) | Anlamlı fark yoksa ikincil ölçüt: karmaşıklık |

"Aynı eğitim parametreleri" ifadesi aynı öğrenme oranı, batch size, optimizer, kayıp, veri ayrımı ve durdurma kuralı olarak yorumlanır. Sabit ve eşit bir epoch sayısı, daha hızlı yakınsayan mimariyi kayırdığı için kullanılmaz: 20 ve 50 epoch'luk sabit bütçelerde ResNet50'nin en iyi epoch'u 5 seed'in hepsinde son epoch olmuştur.

---

## 2. Birincil karşılaştırma

| Ayar | Değer (iki mimari için aynı) |
|---|---|
| Veri | FRIDA/FRIDA2 sentetik, sahne bazlı ayrım (split seed 42): 464 / 96 / 112 görüntü, 14 test sahnesi |
| Omurga | ImageNet ön eğitimli, tamamen dondurulmuş (ResNet50'de BatchNorm eval modunda) |
| Eğitilen kısım | Regresyon başlığı (512 → 128 → 1, dropout 0.3) |
| Optimizer | Adam, LR 1e-4, weight decay 1e-5 |
| Kayıp | L1 (MAE) |
| Batch size | 16 |
| Durdurma | En fazla 200 epoch; validation MAE 20 epoch boyunca iyileşmezse durur |
| Seçim | Her seed'de en düşük validation MAE'nin görüldüğü epoch |
| Eğitim seed'leri | 42, 7, 123, 2024, 3407 |
| Test | Her seed için seçilen ağırlıklarla **bir kez** |

Komutlar:

```bash
python -m src.training.train_synthetic_multiseed --arch vgg16 --epochs 200 --patience 20
python -m src.training.train_synthetic_multiseed --arch resnet50 --epochs 200 --patience 20
python -m src.evaluation.statistical_analysis
```

---

## 3. Ölçütler ve testler

Fark = MAE(ResNet50) − MAE(VGG16). Pozitif değer VGG16 lehinedir.

1. **Ortalama test MAE ± SS** (5 seed).
2. **Seed bazında yön:** Kaç seed'de hangi mimari daha düşük test MAE verdi?
3. **Anlamlılık:** Her test görüntüsünün mutlak hatası 5 seed üzerinden ortalanır, sahne ortalamasına çevrilir; 14 sahne üzerinde eşleştirilmiş iki yönlü Wilcoxon işaretli sıralar testi uygulanır. Aynı aile içindeki karşılaştırmalara Holm düzeltmesi yapılır. α = 0.05.
4. **Etki büyüklüğü:** MAE farkının sahne düzeyinde küme bootstrap %95 güven aralığı (10 000 yeniden örnekleme, seed 42).

Seed düzeyinde doğrudan anlamlılık testi yapılmaz: 5 seed ile Wilcoxon testinin ulaşabileceği en küçük iki yönlü p değeri 0.0625'tir.

---

## 4. Karar kuralı

| Koşul | Karar |
|---|---|
| 5/5 seed'de VGG16 daha iyi **ve** GA alt sınırı > 0 **ve** Holm p < 0.05 | **VGG16 anlamlı düzeyde daha iyi** |
| 5/5 seed'de ResNet50 daha iyi **ve** GA üst sınırı < 0 **ve** Holm p < 0.05 | **ResNet50 anlamlı düzeyde daha iyi** |
| GA 0'ı dışlıyor veya Holm p < 0.05, ama yukarıdaki koşullar tam sağlanmıyor | Kısmi kanıt; anlamlı fark iddia edilmez |
| Diğer | Anlamlı fark yok |

Bir seed 200 epoch'ta erken durmadan bitirirse (`converged_within_budget = false`) karar bir uyarıyla raporlanır. Bütçe, sonuçlara bakılarak artırılmaz.

Bu kural `src/evaluation/statistical_analysis.py` içindeki `protocol_decision` fonksiyonunda uygulanır ve sonuç `docs/reports/statistical_analysis.md` dosyasında "Protokol kararı" sütununda otomatik yazılır.

### Hipotezin değerlendirilmesi

| Protokol kararı | Hipotez |
|---|---|
| ResNet50 anlamlı düzeyde daha iyi | Desteklendi |
| VGG16 anlamlı düzeyde daha iyi | Desteklenmedi; anlamlı fark ters yönde |
| Kısmi kanıt / anlamlı fark yok | Desteklenmedi; anlamlı fark gösterilemedi |

---

## 5. Gerçek dünya (FVEI) ve AUS için temel seçimi

- FVEI karşılaştırması (her mimari için tek seed, son evrişim aşaması + başlık, validation ile seçim, kilitli testte tek değerlendirme) 18.10.2026'da tamamlanmıştır ve **tekrarlanmaz veya ayarlanmaz**. Tek seed olduğu için ikincil kanıt olarak raporlanır.
- Sentetik ve FVEI sonuçları aynı yöndeyse ortak sonuç raporlanır. Farklı yöndeyse ikisi de olduğu gibi raporlanır ve araştırma sorusuna bu çerçevede yanıt verilir.
- Sentetik karşılaştırmada **anlamlı fark yoksa**, önerideki "düşük karmaşıklık" ölçütüne göre ikincil karşılaştırma yapılır: toplam parametre sayısı, aynı GPU'da görüntü başına çıkarım süresi ve yakınsama için gereken epoch sayısı. Bunlar karar olarak değil, gerekçe olarak raporlanır.

---

## 6. Değişmeyecekler

- Nihai gerçek dünya modeli (`results/checkpoints/vgg16_fvei_block5_best.pth`) bu protokolün sonucundan bağımsız olarak değişmez. Bu model, önerideki iş akışına uygun olarak validation ile seçilmiş ve kilitli testte değerlendirilmiştir. Mimari karşılaştırmasının sonucu bir bulgu olarak raporlanır.
- FVEI kilitli test kümesi hiçbir yeni karar için kullanılmaz.
- 20 ve 50 epoch'luk sabit bütçeli çoklu seed sonuçları duyarlılık analizi olarak raporlanır; birincil karar erken durdurmalı gruplara dayanır.
