# Agent Instructions — fog-visibility-estimation

TÜBİTAK 2209-A projesi: VGG16 / ResNet50 transfer öğrenme ile sisli görüntülerden görüş mesafesi regresyonu. GitHub: https://github.com/ilydozttrk/fog-visibility-estimation

## Ortam

- Windows, Python sanal ortamı `.venv` (`.venv\Scripts\activate`).
- Tüm komutlar depo kökünden `python -m ...` biçiminde çalıştırılır (`src/training/dataloader.py` göreli `data/generated` yolu kullanır).
- Komut sırası ve tüm deneyler: `docs/REPRODUCIBILITY.md`. Veri setleri: `docs/DATASETS.md`.

## Kesin kurallar

1. **Kilitli FVEI test kümesi**: Test sonuçlarına bakarak hiperparametre, checkpoint, eğitim stratejisi veya **nihai model** değiştirme. `evaluate_fvei.py --force` kullanma. Model seçimi yalnızca validation MAE ile yapılır. (ImageNet→FVEI VGG16 testte biraz daha düşük MAE verdi; bu, nihai modeli değiştirmek için gerekçe DEĞİLDİR. Nihai model `vgg16_fvei_block5_best.pth` olarak kalır.)
2. **Mevcut checkpoint'lerin üzerine yazma**: `results/checkpoints/*_best.pth` dosyaları raporlanan sonuçların kaynağıdır. Yeni deneyler `results/checkpoints/fvei_runs/` ve `results/multiseed/` altına yazar.
3. `data/processed/fvei/fvei_final_split_manifest.csv` dosyasını yeniden üretme veya değiştirme.
4. `docs/reports/tubitak_final_report_*.md` ve `docs/reports/final_results_summary.md` dosyalarını kullanıcı açıkça istemedikçe düzenleme.
5. Veri seti görüntülerini (`data/raw`, `results/**/*.jpg`), `*.pth` dosyalarını ve lisans netleşene kadar FVEI split manifestini ile FVEI görüntü bazlı tahmin CSV'lerini commit etme. `codex/private-fvei-validation-backup` dalını push etme.
6. Commit öncesi `python scripts/sanitize_result_paths.py` çalıştır (mutlak `C:\...` yollarını temizler).
7. **Model seçim protokolü**: VGG16–ResNet50 kararı yalnızca `docs/MODEL_SELECTION_PROTOCOL.md` kuralına göre verilir. Protokolü, eşikleri veya `protocol_decision` fonksiyonunu sonuçları gördükten sonra değiştirme.
8. Sentetik deneylerde öğrenme oranı, batch size, kayıp fonksiyonu ve dondurma stratejisi önceki protokolle aynı kalır; yalnızca epoch bütçesi ve erken durdurma değişir.

## Tamamlanan işler (2026-10-18, commit 2086153)

- Çoklu seed: `vgg16_e20`, `resnet50_e20`, `resnet50_e50` (5 seed). ResNet50'de tüm seed'lerde en iyi epoch = son epoch (yakınsamamış).
- FVEI: `resnet50_fvei_synthetic_lastblock_s42` (test MAE 27.48 m), `vgg16_fvei_imagenet_lastblock_s42` (test MAE 24.33 m); nihai VGG16 25.13 m. Holm sonrası farklar anlamlı değil.

## Bekleyen işler (sırayla)

1. `pytest -q`. Yeni değişiklikler: `src/models/regression_models.py` (`resnet50_cbam`, `resnet50_se` varyantları), `src/evaluation/statistical_analysis.py` (dikkat karşılaştırma ailesi, gerçek mimari adına göre eşleştirme), `src/training/finetune_fvei.py` (yalnızca vgg16/resnet50), `tests/test_regression_models.py`, `tests/test_statistics.py`, `docs/MODEL_SELECTION_PROTOCOL.md` (Bölüm 7: koşullu dikkat deneyi), `docs/REPRODUCIBILITY.md`, `AGENTS.md`.
2. **Deneylerden ÖNCE** bu değişiklikleri ikinci bir ön kayıt commit'i olarak kaydet (mesaj: "Pre-register conditional ResNet50 attention experiment"). Önceki `a15671d` commit'ini değiştirme (amend etme). Kullanıcı push'u onayladı: `main` dalını (her iki ön kayıt commit'iyle) deneylerden önce push et. Push öncesi `git show --stat` ile FVEI manifesti, FVEI görüntü bazlı tahmin CSV'leri, `*.pth` veya `.tmp` dosyası olmadığını doğrula. `codex/private-fvei-validation-backup` dalını push etme.
3. Dry-run: `python -m src.training.train_synthetic_multiseed --arch vgg16 --dry-run --patience 20` ve `python -m src.training.train_synthetic_multiseed --arch resnet50_cbam --dry-run --patience 20`
4. Yakınsama deneyleri (GPU, 5 seed):
   - `python -m src.training.train_synthetic_multiseed --arch vgg16 --epochs 200 --patience 20`
   - `python -m src.training.train_synthetic_multiseed --arch resnet50 --epochs 200 --patience 20`
   Bir seed 200 epoch'a erken durmadan ulaşırsa (`converged_within_budget: false`) bütçeyi kendiliğinden artırma; durumu kullanıcıya bildir.
5. `python -m src.evaluation.statistical_analysis` (çıktı dizini vermeden). `docs/reports/statistical_analysis.md` içindeki "Mimari" ailesinde `vgg16_e200_p20` / `resnet50_e200_p20` satırının "Protokol kararı" birincil sonuçtur.
6. **Koşullu adım (protokol Bölüm 7):** Birincil karar tam olarak "ResNet50 anlamlı düzeyde daha iyi" ise:
   - `python -m src.training.train_synthetic_multiseed --arch resnet50_cbam --epochs 200 --patience 20`
   - `python -m src.training.train_synthetic_multiseed --arch resnet50_se --epochs 200 --patience 20`
   - `python -m src.evaluation.statistical_analysis` ile raporu yeniden üret ("Dikkat" ailesi satırları).
   Karar başka bir şeyse bu adımı atla ve README'de "koşul sağlanmadığı için çalıştırılmadı" diye belirt. Dikkat varyantlarını FVEI'de eğitme veya değerlendirme.
7. Protokol kararı "Anlamlı fark yok" veya "Kısmi kanıt" ise protokol Bölüm 5'teki ikincil ölçütleri ölç (toplam parametre sayısı, aynı GPU'da görüntü başına ortalama çıkarım süresi, yakınsama epoch'u) ve küçük bir tablo olarak `docs/reports/statistical_analysis_secondary.md` dosyasına yaz.
8. README güncellemesi:
   - "Statistical Analysis and Validation Experiments" bölümündeki "Open point / Script" tablosunu sonuç tablosuyla değiştir: birincil karşılaştırma (erken durdurmalı gruplar, protokol kararı), sabit bütçeli duyarlılık sonuçları (`e20`, `e50`, yakınsama uyarısıyla), varsa ResNet50 + CBAM/SE sonuçları, FVEI ResNet50 vs VGG16 (MAE, fark, 95% GA, Holm p), ImageNet→FVEI ablasyonu. `docs/MODEL_SELECTION_PROTOCOL.md` dosyasına bağlantı ver.
   - "Main Research Findings" bölümüne yeni maddeler ekle: (a) protokol kararı ve hipotezin durumu (protokol Bölüm 4 tablosuna göre), (b) sabit bütçede ResNet50'nin yakınsamadığı ve farkın bütçeye duyarlı olduğu, (c) koşullu dikkat deneyi çalıştırıldıysa sonucu (Bölüm 7 tablosuna göre), (d) FVEI'de iki mimari arasındaki farkın küçük ve Holm sonrası anlamlı olmadığı, (e) sentetik ön eğitimin FVEI'de ölçülebilir fayda sağlamadığı, (f) nihai modelin test sonucuna göre değiştirilmediği.
   - Sonuç VGG16 lehine çıkmazsa bunu olduğu gibi raporla.
   - "Validation experiments" listesindeki test sayısını gerçek `pytest` çıktısıyla düzelt.
9. Depo kökündeki geçici `.tmp` dosyalarını (`.publication_snapshot.tmp` vb.) ve `results/ci_statistics/` klasörünü sil; gerekli değillerse kullanıcıya listeleyip onay al.
10. `python scripts/sanitize_result_paths.py`, ardından commit. Bu son push için yine kullanıcıya sor.
