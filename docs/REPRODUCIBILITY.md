# Tekrar Üretilebilirlik Kılavuzu

Bu kılavuz, projedeki tüm sonuçların hangi sırayla ve hangi komutlarla üretildiğini özetler. Tüm komutlar **depo kök klasöründen** çalıştırılmalıdır.

Veri setlerinin edinilmesi ve yerleştirilmesi için: [`DATASETS.md`](DATASETS.md).

---

## 0. Ortam

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Testler:

```bash
pytest -q
```

### Parçalı FVEI arşivini hazırlama (Windows)

`fog open data_2.7z.001` ile başlayan tüm parçalar (`.001`–`.014`) aynı klasörde bulunmalıdır. 7-Zip ilk parçadan içteki ZIP'i çıkarır:

```powershell
& "C:\Program Files\7-Zip\7z.exe" x "<arşiv klasörü>\fog open data_2.7z.001" "-odata/raw/fvei_source" -aos
Get-FileHash "data/raw/fvei_source/fog open data.zip" -Algorithm SHA256
```

Beklenen SHA256 `docs/DATASETS.md` içinde kayıtlıdır. Sonraki komutlarda `<FVEI.zip>` yerine `data/raw/fvei_source/fog open data.zip` kullanılabilir. Bu klasör Git dışında kalır; mevcut split manifesti kullanılır.

### Yerel doğrulama — 18 Ekim 2026

- `.venv` ortamı: PyTorch `2.13.0+cu126`, CUDA kullanılabilir, NVIDIA GeForce GTX 1650 (4 GiB).
- `python -m pytest -q`: **24 passed**.
- VGG16 sentetik `--dry-run`: başarılı (1 seed, 1 epoch, 2 batch).
- ResNet50 FVEI `--dry-run`: başarılı (2245 train / 480 val; kilitli test okunmadı).
- Çıkarılan FVEI ZIP dosyasının SHA256 değeri kayıtlı değerle eşleşti.
- İstatistik analizi mevcut tahminlerden yeniden üretildi; bu kontroller tam eğitim deneylerinin tamamlandığı anlamına gelmez.

### Tamamlanan sentetik doğrulama deneyleri — 18 Ekim 2026

Bölme seed'i 42; eğitim seed'leri 42, 7, 123, 2024 ve 3407 olarak sabit protokolle çalıştırıldı. Değerler beş koşunun test MAE ortalaması ± örnek standart sapmasıdır.

| Model | Epoch bütçesi | Test MAE (m) | En iyi epoch'lar (seed sırasıyla) |
|---|---:|---:|---|
| VGG16 | 20 | 63,99 ± 1,31 | 19, 19, 20, 20, 20 |
| ResNet50 | 20 | 127,64 ± 3,71 | 20, 20, 20, 20, 20 |
| ResNet50 | 50 | 86,29 ± 2,00 | 50, 50, 50, 50, 50 |

VGG16, eşleşen beş eğitim seed'inin tamamında hem 20 hem 50 epoch ResNet50 koşularından daha düşük test MAE verdi. ResNet50 için ek eğitim farkı azalttı; ancak 50 epoch koşularının tamamı yine son epoch'u seçtiğinden tam yakınsama veya mimarinin tüm eğitim bütçelerinde üstünlüğü sonucu çıkarılamaz. Bu sonuçlar yeni hiperparametre seçiminde kullanılmadı. Koşu başına ayrıntılar `results/multiseed/` altında, istatistiksel karşılaştırmalar `docs/reports/statistical_analysis.md` içindedir.

GPU eğitiminde bazı CUDA işlemleri tam deterministik değildir (`torch.use_deterministic_algorithms(True, warn_only=True)`); bu nedenle sonuçlar bit düzeyinde aynı olmayabilir.

### Tamamlanan FVEI doğrulama deneyleri — 18 Ekim 2026

Her koşu 20 epoch, seed 42 ve mevcut kilitli manifest ile çalıştırıldı. Model seçimi yalnızca validation MAE ile yapıldı; iki yeni koşu test kümesinde birer kez değerlendirildi.

| Koşu | Seçilen epoch | Validation MAE (m) | Test MAE (m) |
|---|---:|---:|---:|
| Özgün VGG16 sentetik → FVEI (mevcut referans) | 12 | 26,4428 | 25,1347 |
| ResNet50 sentetik → FVEI | 7 | 27,5859 | 27,4770 |
| VGG16 ImageNet → FVEI | 17 | 25,9733 | 24,3330 |

Özgün VGG16 referansına göre MAE farkı ResNet50 için +2,34 m (%95 bootstrap GA 0,62–4,09; Holm düzeltmeli Wilcoxon p=0,0636), doğrudan ImageNet başlangıcı için −0,80 m (GA −1,96–0,38; p=0,0700) oldu. İki karşılaştırma da Holm düzeltmeli Wilcoxon testinde anlamlı değildi. Sentetik ön eğitimin FVEI'ye katkısı bu ablasyonda gösterilemedi. FVEI deneyleri tek eğitim seed'i kullanır; görüntü düzeyindeki bootstrap, bilinmeyen kamera/sahne bağımlılığını gidermez. Test sonuçları eğitim protokolünü veya uygulamadaki özgün checkpoint'i değiştirmek için kullanılmadı.

Yeni sonuçlar `results/fvei/runs/`, ağırlıklar Git dışında kalan `results/checkpoints/fvei_runs/` altındadır. İstatistik raporu ve grafiği tüm yeni tahminlerle yeniden üretildi.

Son bütünlük kontrolü: 15 sentetik koşuda epoch sayıları, validation ile seçilen epoch'lar ve 112 benzersiz test tahmini doğrulandı. İki yeni FVEI koşusunda 482 exact-label test tahmini ile 900 ayrı ceiling tahmini doğrulandı. Korunan 10 özgün checkpoint/manifest dosyasının SHA256 değerleri değişmedi. Açık yayın sürümünde FVEI manifesti ve altı örnek düzeyindeki tahmin CSV'si yerelde tutulur; toplu FVEI metrikleri, istatistikler, eğitim geçmişleri ve grafikler izlenir. Arşivler, ağırlıklar ve dry-run çıktıları Git dışında kalır.

### Açık checkout ve özel FVEI dosyaları

FVEI komutları, veri sağlayıcıdan edinilen ZIP'e ve araştırmacıdan izin kapsamında özel olarak edinilen mevcut kilitli manifeste ihtiyaç duyar. Bu manifest açık depoda bulunmaz ve yeniden üretilmemelidir. Tam FVEI istatistiklerini yeniden hesaplamak için özgün özel tahmin CSV'leri de gerekir. Yayımlanan tam rapor mevcut hesaplamaların kaydı olarak korunur.

Özel dosyalar olmadan sentetik ve çoklu seed istatistiklerini doğrulamak için CI ile aynı komutu kullanın:

```bash
python -m src.evaluation.statistical_analysis --no-figure --output-dir results/ci_statistics
```

Eksik FVEI tahminleri atlanır. Ayrı çıktı klasörü, yayımlanan tam istatistik raporunun ve grafiğinin yalnızca sentetik sonuçlarla değiştirilmesini önler. Özel dosyalar bulunan yerel ortamda Bölüm 4'teki tam analiz komutu kullanılabilir.

18 Ekim 2026 yayın kontrolünde, gönderilecek commit'in özel FVEI dosyalarını içermeyen arşivinden alınan temiz kopyada **25 test geçti**. Yukarıdaki CI komutu sentetik ve çoklu seed istatistiklerini başarıyla hesapladı; tam FVEI raporu, istatistik JSON'u ve grafiğinin hash'leri değişmedi. Yedi özel dosyanın yerel SHA256 değerleri de korundu; bu dosyalar yayımlanacak `main` geçmişinde bulunmuyor.

---

## 1. Sentetik veri ve temel modeller (FRIDA / FRIDA2)

```bash
python -m src.data.generate_visibility_dataset
python -m src.data.verify_generated_dataset

python -m src.training.train_vgg16
python -m src.evaluation.evaluation_vgg16

python -m src.training.train_resnet50
python -m src.evaluation.evaluation_resnet50
```

Sahne bazlı bölme: 84 sahne → 464 / 96 / 112 görüntü, seed 42.

## 2. Dikkat mekanizmaları

```bash
python -m src.training.train_vgg16_attention
python -m src.evaluation.evaluation_vgg16_attention

python -m src.training.train_vgg16_se
python -m src.evaluation.evaluation_vgg16_se
```

## 3. Nihai FVEI modeli

```bash
python -m src.training.finetune_vgg16_fvei --zip-path "<FVEI.zip>" --dry-run
python -m src.training.finetune_vgg16_fvei --zip-path "<FVEI.zip>"
python -m src.evaluation.evaluate_vgg16_fvei_final --zip-path "<FVEI.zip>"
```

## 4. Şekiller ve istatistiksel analiz

```bash
python -m src.evaluation.generate_final_figures
python -m src.evaluation.statistical_analysis
```

`statistical_analysis` hiçbir modeli eğitmez; yalnızca kaydedilmiş tahmin dosyalarını okur ve şunları üretir:

- `results/statistics/statistical_analysis.json`
- `docs/reports/statistical_analysis.md`
- `figures/statistical_mae_differences.png`

---

## 5. Ek doğrulama deneyleri

Bu deneyler araştırma önerisindeki açık kalan noktaları kapatmak için eklenmiştir. Hiçbiri mevcut checkpoint'lerin üzerine yazmaz.

### 5.1 Çoklu seed (sentetik)

Sahne ayrımı sabit (seed 42) tutulur, yalnızca eğitim tohumu değişir (42, 7, 123, 2024, 3407).

```bash
python -m src.training.train_synthetic_multiseed --arch vgg16 --dry-run
python -m src.training.train_synthetic_multiseed --arch vgg16
python -m src.training.train_synthetic_multiseed --arch resnet50
python -m src.training.train_synthetic_multiseed --arch resnet50 --epochs 50
```

Son komut, orijinal ResNet50 eğitiminde en iyi epoch'un son epoch (20/20) olması nedeniyle yetersiz eğitim olasılığını kontrol eder. Yarıda kalan bir çalıştırma tekrar başlatıldığında tamamlanmış seed'ler atlanır.

50 epoch'luk ResNet50 çalıştırmalarında da 5 seed'in hepsinde en iyi epoch son epoch (50/50) olmuştur. Yakınsamış modelleri karşılaştırmak için iki omurga da validation tabanlı erken durdurma ile eğitilir (en fazla 200 epoch; validation MAE 20 epoch boyunca iyileşmezse durur). Model seçimi yine yalnızca validation MAE ile yapılır, test her seed için bir kez değerlendirilir.

Karar kuralı [`MODEL_SELECTION_PROTOCOL.md`](MODEL_SELECTION_PROTOCOL.md) dosyasındadır ve yeni eğitimlerden önce commit edilir. Önceki 20/50 epoch sonuçları ön kayıt kapsamında değildir. Protokol kodunun deney öncesi doğrulamasında **36 test geçti**; bunlar beş seed şartını ve erken durmadan epoch bütçesine ulaşan koşuların yakınsamış sayılmamasını da kapsar.

Koşullu ResNet50 dikkat uzantısının deney öncesi doğrulamasında **41 test geçti**. İlk ön kayıt (`a15671d`) sonrasında başlayan VGG16 seed 42 ön koşusu, koşullu deney protokole eklenince 28. epoch'ta, test değerlendirmesi yapılmadan durduruldu; bu koşu sonuçlara dahil edilmedi. İlk commit değiştirilmez. İkinci ön kayıt commit'i de oluşturulup iki commit birlikte push edildikten sonra yakınsama deneyleri aynı seed'lerle baştan çalıştırılır. Kesilen ön koşunun logu yerelde `results/logs/convergence_vgg16_before_second_registration.log` dosyasında saklanır.

```bash
python -m src.training.train_synthetic_multiseed --arch vgg16 --epochs 200 --patience 20
python -m src.training.train_synthetic_multiseed --arch resnet50 --epochs 200 --patience 20
```

Yalnızca bu birincil karşılaştırmanın protokol kararı "ResNet50 anlamlı düzeyde daha iyi" çıkarsa, dikkat mekanizmaları ResNet50 üzerinde aynı protokolle denenir ([`MODEL_SELECTION_PROTOCOL.md`](MODEL_SELECTION_PROTOCOL.md) Bölüm 7):

```bash
python -m src.training.train_synthetic_multiseed --arch resnet50_cbam --epochs 200 --patience 20
python -m src.training.train_synthetic_multiseed --arch resnet50_se --epochs 200 --patience 20
```

Çıktı: `results/multiseed/<arch>_e<epochs>[_p<patience>]/seed_<n>/`. İstatistik raporu, erken durdurmalı grupları yalnızca aynı patience değerine sahip gruplarla eşleştirir ve her grup için bütçe içinde yakınsayan seed sayısını gösterir.

### 5.2 ResNet50'nin FVEI üzerinde ince ayarı

Araştırma sorusu karşılaştırmayı hem sentetik hem gerçek dünya verisinde istemektedir. ResNet50, VGG16 ile aynı protokolle (son evrişim aşaması + regresyon başlığı, 20 epoch, validation MAE ile seçim) FVEI'ye uyarlanır:

```bash
python -m src.training.finetune_fvei --arch resnet50 --init synthetic --zip-path "<FVEI.zip>" --dry-run
python -m src.training.finetune_fvei --arch resnet50 --init synthetic --zip-path "<FVEI.zip>"
python -m src.evaluation.evaluate_fvei --run-name resnet50_fvei_synthetic_lastblock_s42 --zip-path "<FVEI.zip>"
```

### 5.3 Kademeli veri stratejisinin katkısı (ablasyon)

Öneride sentetik → gerçek kademeli strateji önerilmiştir. Sentetik ön eğitimin katkısını ölçmek için VGG16 doğrudan ImageNet ağırlıklarından FVEI'ye uyarlanır:

```bash
python -m src.training.finetune_fvei --arch vgg16 --init imagenet --zip-path "<FVEI.zip>"
python -m src.evaluation.evaluate_fvei --run-name vgg16_fvei_imagenet_lastblock_s42 --zip-path "<FVEI.zip>"
```

### 5.4 Kilitli test kuralı

- `finetune_fvei` test kümesini hiç yüklemez.
- `evaluate_fvei` her çalıştırmayı **bir kez** değerlendirir; `evaluation.json` oluştuktan sonra tekrar değerlendirmeyi reddeder.
- Test sonuçlarına bakarak hiperparametre veya checkpoint değiştirilmemelidir.

Tüm deneyler bittikten sonra:

```bash
python -m src.evaluation.statistical_analysis
```

---

## 6. Sonuçları depoya eklemeden önce

Eski scriptler sonuç dosyalarına `C:\projects\...` biçiminde mutlak yollar yazmıştır. Bunları depo-göreli yollara çevirmek için:

```bash
python scripts/sanitize_result_paths.py --check
python scripts/sanitize_result_paths.py
```

`.gitignore`, sentetik tahminleri ve küçük toplu sonuç dosyalarını (json, csv, md, png, xlsx) izler. FVEI split manifesti, FVEI örnek düzeyindeki tahmin CSV'leri, model ağırlıkları (`*.pth`) ve veri setinden türetilmiş görüntüler (`results/**/*.jpg`) yerelde tutulur.

---

## 7. Yaklaşık süreler

| Deney | Yaklaşık iş yükü |
|---|---|
| Çoklu seed, 5 seed × 20 epoch × 464 görüntü | VGG16 ve ResNet50 için ayrı ayrı; dondurulmuş omurga ile kısa sürer |
| ResNet50 50 epoch, 5 seed | Yukarıdakinin yaklaşık 2,5 katı |
| FVEI ince ayar, 20 epoch × 2245 görüntü | Orijinal VGG16 FVEI eğitimiyle aynı mertebede |
