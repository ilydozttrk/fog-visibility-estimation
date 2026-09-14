# VGG16 Baseline ve VGG16 + CBAM Karşılaştırması

## 1. Amaç

Bu deneyin amacı, TÜBİTAK 2209-A projesinin mevcut sentetik deney aşamasında VGG16 tabanlı görünürlük tahmin modeline Convolutional Block Attention Module (CBAM) eklenmesinin model performansı üzerindeki etkisini incelemektir.

Önceki baseline karşılaştırmasında VGG16, ResNet50 modelinden daha düşük test MAE değeri elde ettiği için attention entegrasyonu uygulanacak sentetik baseline model olarak seçilmiştir.

CBAM entegrasyonunun temel hipotezi, kanal ve uzamsal attention mekanizmalarının görünürlük tahmini açısından daha bilgilendirici özellikleri ve görüntü bölgelerini öne çıkararak VGG16 baseline performansını iyileştirebileceğidir.

Bu hipotez deneysel olarak test edilmiş; CBAM'ın performansı iyileştireceği önceden varsayılmamıştır.

---

## 2. Deneysel Koşullar

Adil bir karşılaştırma sağlamak amacıyla VGG16 baseline ve VGG16 + CBAM modellerinde mümkün olduğunca aynı deneysel koşullar korunmuştur.

Ortak yapılandırma:

- Veri kaynağı: FRIDA ve FRIDA2 tabanlı oluşturulmuş sentetik görünürlük veri seti
- Toplam görüntü sayısı: 672
- Eğitim örnekleri: 464
- Validation örnekleri: 96
- Test örnekleri: 112
- Bölme yöntemi: Scene-based split
- Görüntü boyutu: 224 × 224
- Batch size: 16
- Epoch sayısı: 20
- Optimizer: Adam
- Learning rate: 1e-4
- Weight decay: 1e-5
- Loss function: L1Loss (MAE)
- Random seed: 42
- Pretrained weights: ImageNet
- Backbone: Frozen
- Regression output: Tek sürekli görünürlük değeri (metre)

Aynı scene-based veri bölünmesinin kullanılması sayesinde modeller aynı bağımsız test örnekleri üzerinde karşılaştırılmıştır.

---

## 3. CBAM Mimarisi

VGG16 + CBAM modelinde Convolutional Block Attention Module iki ardışık attention bileşeninden oluşmaktadır:

1. Channel Attention
2. Spatial Attention

Channel Attention, hangi özellik kanallarının görünürlük tahmini açısından daha önemli olduğunu öğrenmeyi amaçlamaktadır.

Spatial Attention ise görüntünün hangi uzamsal bölgelerinin tahmin açısından daha önemli olduğunu belirlemeyi amaçlamaktadır.

Kullanılan CBAM yapılandırması:

- Feature channels: 512
- Reduction ratio: 16
- Spatial kernel size: 7
- CBAM trainable parameters: 32,866

CBAM, VGG16'nın son convolutional bloğundan sonra ve son MaxPool katmanından önce uygulanmıştır.

Attention öncesi feature map:

`[B, 512, 14, 14]`

CBAM sonrası:

`[B, 512, 14, 14]`

Son MaxPool sonrası:

`[B, 512, 7, 7]`

Regression head baseline VGG16 ile aynı bırakılmıştır. Böylece temel mimari değişken mümkün olduğunca CBAM entegrasyonu ile sınırlandırılmıştır.

---

## 4. VGG16 + CBAM Eğitim Sonuçları

VGG16 + CBAM modeli 20 epoch boyunca eğitilmiştir.

En iyi validation sonucu:

- Best epoch: 17
- Best validation MAE: 69.3274 m

Epoch 17'den sonra training MAE düşmeye devam ederken validation MAE dalgalanmaya başlamıştır.

Örneğin:

| Epoch | Train MAE (m) | Validation MAE (m) |
|---:|---:|---:|
| 13 | 63.9028 | 76.7301 |
| 14 | 58.9256 | 78.1578 |
| 15 | 52.7865 | 73.7326 |
| 16 | 52.0578 | 73.4611 |
| 17 | 47.8197 | **69.3274** |
| 18 | 44.3514 | 73.6024 |
| 19 | 45.3199 | 69.7572 |
| 20 | 41.0328 | 76.0531 |

Bu davranış, eğitimin son bölümünde training ve validation performansı arasındaki farkın açılmaya başladığını göstermektedir. Bu nedenle değerlendirme için son epoch yerine en düşük validation MAE değerini sağlayan epoch 17 checkpoint'i kullanılmıştır.

---

## 5. Test Sonuçları

VGG16 + CBAM modeli, eğitim sırasında kullanılmayan 112 örnekten oluşan bağımsız test kümesi üzerinde değerlendirilmiştir.

### VGG16 + CBAM

- Test MAE: **67.6214 m**
- Mean signed error: **-10.8501 m**
- Minimum absolute error: **0.4317 m**
- Maximum absolute error: **439.5097 m**
- Test samples: **112**

### VGG16 Baseline

- Test MAE: **66.7227 m**
- Mean signed error: **-17.3877 m**
- Minimum absolute error: **0.8415 m**
- Maximum absolute error: **392.8829 m**
- Test samples: **112**

---

## 6. VGG16 ve VGG16 + CBAM Karşılaştırması

| Metric | VGG16 Baseline | VGG16 + CBAM |
|---|---:|---:|
| Best Validation MAE (m) | 69.9705 | **69.3274** |
| Test MAE (m) | **66.7227** | 67.6214 |
| Mean Signed Error (m) | -17.3877 | **-10.8501** |
| Minimum Absolute Error (m) | 0.8415 | **0.4317** |
| Maximum Absolute Error (m) | **392.8829** | 439.5097 |

CBAM modeli validation kümesinde VGG16 baseline'a göre yaklaşık **0.6431 m** daha düşük MAE elde etmiştir.

Buna karşılık bağımsız test kümesinde VGG16 baseline, VGG16 + CBAM modelinden yaklaşık **0.8987 m** daha düşük MAE elde etmiştir.

Dolayısıyla validation kümesinde gözlenen küçük iyileşme bağımsız test performansına yansımamıştır.

---

## 7. Hata Davranışının Değerlendirilmesi

CBAM entegrasyonu toplam test MAE değerini iyileştirmemiş olsa da hata davranışında bazı farklılıklar gözlenmiştir.

Mean signed error:

- VGG16: -17.3877 m
- VGG16 + CBAM: -10.8501 m

Her iki modelde de negatif mean signed error bulunması, ortalama olarak gerçek görünürlük değerlerinin altında tahmin yapma eğiliminin devam ettiğini göstermektedir.

Ancak CBAM modelinde signed error değerinin sıfıra yaklaşması, ortalama düşük tahmin eğiliminin azaldığını göstermektedir.

Diğer taraftan maksimum mutlak hata:

- VGG16: 392.8829 m
- VGG16 + CBAM: 439.5097 m

olarak ölçülmüştür.

Bu nedenle CBAM modeli ortalama tahmin yanlılığını azaltmış olsa da bazı test örneklerinde baseline modelden daha büyük uç hatalar üretmiştir.

Bu sonuç, attention entegrasyonunun hata dağılımını değiştirdiğini ancak mevcut yapılandırmada genel test doğruluğunu artırmadığını göstermektedir.

---

## 8. Sonuç

VGG16 + CBAM modeli, validation kümesinde VGG16 baseline'a göre çok küçük bir iyileşme göstermiştir. Ancak bu kazanım bağımsız test kümesinde korunmamıştır.

Test sonuçları:

- VGG16: **66.7227 m MAE**
- VGG16 + CBAM: **67.6214 m MAE**

şeklindedir.

İki model arasındaki test MAE farkı yalnızca 0.8987 m olmakla birlikte, mevcut tek deney koşulu ve tek random seed üzerinden bu farkın istatistiksel anlamlılığı hakkında bir çıkarım yapılmamaktadır.

Bu nedenle mevcut sentetik FRIDA/FRIDA2 deneyleri kapsamında CBAM entegrasyonunun VGG16 modelinin genel görünürlük tahmin doğruluğunu iyileştirdiği sonucuna varılamaz.

Bununla birlikte CBAM:

- başarıyla VGG16 mimarisine entegre edilmiştir,
- aynı deney protokolü altında eğitilmiş ve değerlendirilmiştir,
- validation performansında küçük bir iyileşme göstermiştir,
- mean signed error değerini sıfıra yaklaştırarak ortalama düşük tahmin eğilimini azaltmıştır,
- ancak test MAE değerini iyileştirmemiş ve maksimum mutlak hatayı artırmıştır.

Dolayısıyla attention mekanizmasının katkısına ilişkin başlangıç hipotezi, mevcut sentetik deney sonuçları tarafından genel test MAE açısından desteklenmemiştir.

---

## 9. Mevcut Sentetik Model Sıralaması

Mevcut FRIDA/FRIDA2 tabanlı sentetik test sonuçlarına göre modeller:

| Model | Test MAE (m) |
|---|---:|
| **VGG16 Baseline** | **66.7227** |
| VGG16 + CBAM | 67.6214 |
| ResNet50 Baseline | 124.6181 |

Bu nedenle mevcut sentetik deney aşamasında en düşük test MAE değerine sahip model **VGG16 baseline** modelidir.

Bu seçim yalnızca mevcut sentetik FRIDA/FRIDA2 deney sonuçları için geçerlidir ve gerçek dünya görünürlük görüntüleri üzerindeki performansı temsil etmemektedir.

---

## 10. Araştırma Açısından Çıkarım

Bu deney, daha karmaşık bir mimarinin veya attention mekanizmasının otomatik olarak daha yüksek tahmin doğruluğu sağlamadığını göstermektedir.

VGG16 + CBAM modeli baseline performansına oldukça yakın sonuç üretmiş, ancak attention entegrasyonu bağımsız test MAE değerinde iyileşme sağlamamıştır.

Bu negatif/neutral sonuç araştırma sürecinin geçerli bir çıktısıdır ve attention mekanizmasının etkisinin kontrollü bir deney ile sınandığını göstermektedir.

Bir sonraki aşamada mevcut modellerin özellikle hata dağılımları, yüksek görünürlük örneklerindeki davranışları ve gerçek dünya verilerine genellenebilirlikleri dikkate alınmalıdır.