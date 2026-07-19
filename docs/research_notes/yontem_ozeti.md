# Yöntem Özeti

## Aşama 1 — Veri Seti Analizi ve Hazırlığı

Proje kapsamında öncelikle FRIDA ve FRIDA2 sentetik veri setleri detaylı olarak analiz edilmiştir.

Her iki veri setindeki açık hava görüntüleri, derinlik haritaları ve klasör yapıları incelenmiş; model eğitiminde kullanılacak görüntüler doğrulanmıştır.

FRIDA veri setinden **18**, FRIDA2 veri setinden **66** temel sahne olmak üzere toplam **84 sahne** belirlenmiştir.

Hazır sürekli görüş mesafesi etiketleri bulunmadığından, araştırma önerisinde planlandığı şekilde derinlik haritaları kullanılarak yeni regresyon hedefleri oluşturulmuştur.

Atmosferik saçılım modeli uygulanarak her sahne için aşağıdaki görüş mesafelerini temsil eden sentetik görüntüler üretilmiştir.

- 50 m
- 80 m
- 100 m
- 150 m
- 200 m
- 300 m
- 500 m
- 800 m

Bu süreç sonunda toplam **672 sentetik görüntüden** oluşan yeni bir veri kümesi hazırlanmış ve tüm etiketler `labels.csv` dosyasında saklanmıştır.

Üretilen veri kümesi doğrulanmış, eksik dosya ve hatalı etiket kontrolü başarıyla tamamlanmıştır.

---

## Aşama 2 — Veri Ön İşleme ve Veri Yükleme

Üretilen veri kümesi model eğitimine uygun hâle getirilmiştir.

Bu kapsamda;

- görüntüler **224×224** piksel boyutuna yeniden ölçeklendirilmiştir,
- RGB formatına dönüştürülmüştür,
- ImageNet ortalama ve standart sapma değerleri kullanılarak normalize edilmiştir.

Model eğitiminde kullanılmak üzere PyTorch tabanlı özel bir `FogVisibilityDataset` sınıfı geliştirilmiş ve veri kümesinin batch'ler hâlinde yüklenmesini sağlayan `DataLoader` altyapısı hazırlanmıştır.

Bu yapı ilerleyen aşamalarda VGG16, ResNet50 ve Attention tabanlı modeller tarafından ortak olarak kullanılacaktır.

---

## Aşama 3 — Eğitim, Doğrulama ve Test Veri Ayrımı

Hazırlanan veri kümesi sahne bazlı olarak eğitim, doğrulama ve test kümelerine ayrılacaktır.

Planlanan veri dağılımı aşağıdaki şekildedir.

- Eğitim kümesi: %70–80
- Doğrulama kümesi: %10–15
- Test kümesi: %10–15

Sahne bazlı ayrım uygulanarak aynı temel sahneye ait görüntülerin farklı veri kümelerinde bulunması engellenecek ve veri sızıntısının önüne geçilecektir.

---

## Aşama 4 — Transfer Öğrenme ile Model Adaptasyonu

VGG16 ve ResNet50 modelleri ImageNet üzerinde önceden eğitilmiş ağırlıklarla yüklenecektir.

Başlangıç aşamasında evrişimsel katmanlar korunacak, son sınıflandırma katmanları kaldırılarak tek çıkışlı regresyon başlığı eklenecektir.

Modeller oluşturulan sentetik veri kümesi üzerinde eğitilecek ve kayıp fonksiyonu olarak Ortalama Mutlak Hata (MAE) kullanılacaktır.

---

## Aşama 5 — Model Karşılaştırması ve Attention Mekanizması

VGG16 ve ResNet50 modellerinin performansı test veri kümesi üzerinde MAE metriği kullanılarak karşılaştırılacaktır.

En başarılı temel model seçildikten sonra modele Attention mekanizması entegre edilecektir.

Attention mekanizmasının görüntü içerisindeki önemli bölgeleri daha etkili şekilde öğrenmesi ve görüş mesafesi tahmin doğruluğunu artırması hedeflenmektedir.

Elde edilen sonuçlar temel model ile karşılaştırılarak raporlanacaktır.

---

## Aşama 6 — Gerçek Dünya Değerlendirmesi

Gerçek dünya veri setlerine erişim sağlanması durumunda model FVEI ve/veya FHVI veri setleri üzerinde Fine-Tuning işlemine tabi tutulacaktır.

Bu aşamada modelin sentetik veriden gerçek yol görüntülerine genelleme başarısı değerlendirilecektir.

---

## Aşama 7 — Web Tabanlı Prototip

En başarılı model Flask tabanlı web uygulamasına entegre edilecektir.

HTML ve CSS kullanılarak geliştirilecek kullanıcı arayüzü üzerinden kullanıcı sisteme görüntü yükleyebilecek ve model ilgili görüntü için görüş mesafesi tahminini gerçekleştirecektir.

Tahmin edilen görüş mesafesi kullanıcı arayüzünde gösterilecek ve böylece proje çıktılarının uygulamalı olarak gösterilebildiği işlevsel bir prototip elde edilecektir.