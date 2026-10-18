# Veri Setleri

Bu depoda **hiçbir veri seti görüntüsü dağıtılmaz**. Aşağıdaki veri setleri kendi lisans ve kullanım koşullarına tabidir; her biri kaynağından ayrı olarak edinilmeli ve belirtilen klasöre yerleştirilmelidir.

Depoda görüntü içermeyen sentetik etiketler ve toplu FVEI denetim özeti izlenir:

| Dosya | İçerik |
|---|---|
| `data/generated/labels.csv` | Sentetik veri kümesinin dosya adı, sahne ve görüş mesafesi etiketleri |
| `data/processed/fvei/manifest.json` | FVEI denetim özeti ve kaynak ZIP SHA256 değeri |

---

## 1. FRIDA ve FRIDA2 (sentetik, ana model karşılaştırması)

| | FRIDA | FRIDA2 |
|---|---|---|
| Sahip | INRETS-LCPC | IFSTTAR (eski INRETS-LCPC) |
| Yazarlar | J.-P. Tarel, A. Cord, H. Halmaoui, D. Gruyer, N. Hautière | aynı |
| Kullanım | Yalnızca araştırma amaçlı, web sitesinde kayıt sonrası | Yalnızca araştırma amaçlı |
| Projedeki sahne | 18 | 66 |
| Klasör | `data/raw/frida/` | `data/raw/frida2/` |

Veri setleriyle birlikte gelen README dosyasında istenen atıf:

> J.-P. Tarel, N. Hautière, A. Cord, D. Gruyer and H. Halmaoui, "Improved Visibility of Road Scene Images under Heterogeneous Fog", *Proceedings of IEEE Intelligent Vehicles Symposium (IV'10)*, San Diego, CA, USA, 2010.

Sentetik veri kümesi, derinlik haritaları kullanılarak 8 görüş mesafesi seviyesi (50, 80, 100, 150, 200, 300, 500, 800 m) için üretilir:

```bash
python -m src.data.generate_visibility_dataset
python -m src.data.verify_generated_dataset
```

Çıktı: `data/generated/images/` (672 görüntü, izlenmez) ve `data/generated/labels.csv` (izlenir).

---

## 2. FVEI (gerçek dünya, nihai model)

| | |
|---|---|
| Kullanım | Gerçek dünya ince ayar ve kilitli test değerlendirmesi |
| Erişim | Veri seti sahiplerinden alınan orijinal ZIP arşivi |
| Kaynak yayın | W. Yang, Y. Zhao, Q. Li, F. Zhu ve Y. Su, “Multi visual feature fusion based fog visibility estimation for expressway surveillance using deep learning network”, *Expert Systems with Applications*, 234, 121151, 2023 |
| DOI | [10.1016/j.eswa.2023.121151](https://doi.org/10.1016/j.eswa.2023.121151) |
| Projede kullanılan paylaşım | `fog open data.zip`: 4500 görüntülük kısmi paylaşım; yayında tanımlanan tam FVEI kümesi 15000 görüntüdür |
| Kaynak ZIP SHA256 | `07a04256b5e7df5319549e9546cf91da47817d978f52a36b6b53f6e43f36154d` |
| Okuma | Görüntüler ZIP içinden doğrudan okunur, açılmaz |

### Paylaşım koşullarının durumu — 18 Ekim 2026

Kaynak yayın ve projede kullanılan kısmi arşiv doğrulandı. Arşivde ayrıca bir README/lisans dosyası bulunmadı. İncelenen kaynaklarda, özgün dosya adlarının ve etiketlerin başka bir açık depoda yeniden dağıtılmasına ilişkin açık lisans veya bu alanları kapsayan yazılı izin doğrulanamadı. Bu, paylaşımın yasak olduğunun tespiti değildir; doğrulanmamış bir izin alanıdır. Erişilebilir bir veri paylaşımını, yeniden dağıtım lisansı olarak varsaymıyoruz. Projenin MIT lisansı üçüncü taraf veri setine uygulanmaz.

**Açık yayın sürümünde kod, dokümanlar, toplu metrikler ve grafikler bulunur.** Aşağıdaki FVEI örnek düzeyindeki dosyalar yerelde tutulur ve gönderilecek Git geçmişinden çıkarılır:

- `data/processed/fvei/fvei_final_split_manifest.csv`: özgün ZIP üyesi/dosya adı, görüş seviyesi, metre etiketi, SHA256 ve split ataması.
- `results/fvei/vgg16_fvei_final_test_predictions.csv` ve `results/fvei/vgg16_fvei_ceiling_predictions.csv`: dosya adıyla ilişkilendirilen etiket ve model tahminleri.
- `results/fvei/runs/*/test_predictions.csv` ve `results/fvei/runs/*/ceiling_predictions.csv`: iki yeni koşunun aynı türde örnek düzeyindeki kayıtları; toplam altı FVEI tahmin CSV'si.

Bu metadata CSV'leri ancak yeniden dağıtım kapsamı doğrulandıktan sonra açık depoya eklenmelidir. 500 m etiketinin kesin ölçüm mü yoksa üst sınır mı olduğu da bağımsız kaynakla doğrulanmış değildir; mevcut ceiling değerlendirmesi bu sınırlamayla raporlanır.

Kilitli yerel manifest değiştirilmez veya yeniden üretilmez. Yalnızca dosyaları sonraki bir commit'te silmek yeterli olmadığından, gönderilmemiş deney commit'i bu yedi dosyayı içermeyecek biçimde düzenlenir. Araştırmanın tam yerel kaydı yalnızca yerel bir yedek dalda saklanır; bu dal yayımlanmaz.

### Açık depodan tekrar üretilebilirlik sınırı

Sentetik istatistikler ve çoklu seed özetleri yayımlanan sonuç dosyalarından yeniden hesaplanabilir. FVEI için toplu metrikler, güven aralıkları ve eğitim geçmişleri erişilebilirdir; bootstrap karşılaştırmaları özel tahmin CSV'leri olmadan yeniden hesaplanamaz. Aynı FVEI bölmesini kullanmak için arşive ek olarak mevcut kilitli manifestin de izin kapsamında özel olarak edinilmesi gerekir; yalnızca arşivi indirmek aynı bölmeyi sağlamaz.

Özel FVEI dosyaları olmayan bir checkout'ta aşağıdaki komut eksik FVEI tahminlerini atlar ve yayımlanan tam raporu değiştirmeden ayrı çıktı üretir:

```bash
python -m src.evaluation.statistical_analysis --no-figure --output-dir results/ci_statistics
```

ZIP'in doğruluğunu kontrol etmek için (Windows PowerShell):

```powershell
Get-FileHash "<FVEI.zip>" -Algorithm SHA256
```

Denetim ve bölme adımları:

```bash
python -m src.data.prepare_fvei "<fog open data.zip>"
python -m src.data.split_fvei
```

Nihai bölme, iki şüpheli validation örneğinin çıkarılmasıyla oluşturulan `fvei_final_split_manifest.csv` dosyasıdır (ayrıntılar: [`docs/reports/fvei_real_world_evaluation.md`](reports/fvei_real_world_evaluation.md)). **Kilitli test kümesini korumak için bu dosya yeniden üretilmemeli; izin kapsamında özel olarak edinilen mevcut manifest kullanılmalıdır. Dosya açık depoda dağıtılmaz.**

---

## 3. CIDET (yardımcı gerçek dünya deneyleri)

| | |
|---|---|
| Ad | CIDET VO3 Visibility Dataset |
| Yayıncı | University of Pardubice |
| Yazarlar | J. Kopecká, D. Kopecký, P. Doležel, Z. Rácová |
| DOI | [10.5281/zenodo.15494899](https://doi.org/10.5281/zenodo.15494899) |
| Lisans | CC BY 4.0 |
| İçerik | Sabit kameradan 1000 RGB görüntü + meteorolojik ölçümler + elle etiketlenmiş görüş mesafesi |
| Klasör | `data/raw/cidet/` |

İlgili yayın: "Estimation of Atmospheric Visibility by Deep Learning Model Using Multimodal Dataset".

---

## 4. Benchmark-Visibility (yardımcı stres testi)

| | |
|---|---|
| Kaynak yayın | Y. Wang, L. Zhou, Z. Xu, "Traffic Road Visibility Retrieval in the Internet of Video Things through Physical Feature Based Learning Network", *IEEE Transactions on Intelligent Transportation Systems*, 26(3), 3629–3642, 2025 |
| Bağlantı | <https://ieeexplore.ieee.org/document/10817150> |
| Klasör | `data/raw/benchmark_visibility/` |

---

## 5. FHVI

Proje süresince FHVI veri setine erişim sağlanamamıştır; projede kullanılmamıştır.
