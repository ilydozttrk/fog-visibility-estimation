# Agent Instructions — fog-visibility-estimation

TÜBİTAK 2209-A projesi: VGG16 / ResNet50 transfer öğrenme ile sisli görüntülerden görüş mesafesi regresyonu. GitHub: https://github.com/ilydozttrk/fog-visibility-estimation

## Ortam

- Windows, Python sanal ortamı `.venv` (`.venv\Scripts\activate`).
- Tüm komutlar depo kökünden `python -m ...` biçiminde çalıştırılır (`src/training/dataloader.py` göreli `data/generated` yolu kullanır).
- Komut sırası ve tüm deneyler: `docs/REPRODUCIBILITY.md`. Veri setleri: `docs/DATASETS.md`.

## Kesin kurallar

1. **Kilitli FVEI test kümesi**: Test sonuçlarına bakarak hiperparametre, checkpoint veya eğitim stratejisi değiştirme. `evaluate_fvei.py --force` kullanma. Model seçimi yalnızca validation MAE ile yapılır.
2. **Mevcut checkpoint'lerin üzerine yazma**: `results/checkpoints/*_best.pth` dosyaları raporlanan sonuçların kaynağıdır. Yeni deneyler `results/checkpoints/fvei_runs/` ve `results/multiseed/` altına yazar.
3. `data/processed/fvei/fvei_final_split_manifest.csv` dosyasını yeniden üretme veya değiştirme.
4. `docs/reports/tubitak_final_report_*.md` dosyalarını kullanıcı açıkça istemedikçe düzenleme.
5. Veri seti görüntülerini (`data/raw`, `results/**/*.jpg`) ve `*.pth` dosyalarını commit etme; `.gitignore` buna göre ayarlı.
6. Commit öncesi `python scripts/sanitize_result_paths.py` çalıştır (mutlak `C:\...` yollarını temizler).

## Bekleyen işler (sırayla)

1. `pytest -q` — `tests/test_regression_models.py` ve `tests/test_statistics.py` yeni eklendi, torch'lu ortamda henüz çalıştırılmadı.
2. Dry-run doğrulamaları:
   - `python -m src.training.train_synthetic_multiseed --arch vgg16 --dry-run`
   - `python -m src.training.finetune_fvei --arch resnet50 --zip-path "<FVEI.zip>" --dry-run`
   Hata çıkarsa yeni scriptleri (`src/models/regression_models.py`, `src/training/finetune_fvei.py`, `src/training/train_synthetic_multiseed.py`, `src/evaluation/evaluate_fvei.py`) düzelt; mevcut eski scriptlerin davranışını değiştirme.
3. GPU deneyleri (`docs/REPRODUCIBILITY.md` Bölüm 5): çoklu seed (vgg16, resnet50, resnet50 --epochs 50), ResNet50 FVEI ince ayar + tek seferlik değerlendirme, VGG16 ImageNet→FVEI ablasyonu.
4. `python -m src.evaluation.statistical_analysis` ile `docs/reports/statistical_analysis.md` yeniden üret.
5. `scripts/ci_tests.yml` dosyasını `.github/workflows/tests.yml` olarak taşı.
6. Sonuçları özetle; README'deki "Validation experiments" kontrol listesini güncelle; commit at (push için kullanıcıya sor).

FVEI ZIP yolu bilinmiyorsa kullanıcıya sor.
