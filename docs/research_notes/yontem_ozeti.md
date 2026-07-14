# Yöntem Özeti

## Aşama 1 — Veri Seti Hazırlığı ve Normalizasyon

FRIDA ve FRIDA2 sentetik veri setleri incelenecek ve veri havuzuna dahil edilecektir.

Veri setlerinin klasör yapısı, görüntü formatları ve derinlik bilgileri analiz edilecektir.

Derinlik haritalarından sürekli görüş mesafesi regresyon etiketlerinin türetilmesi planlanmaktadır.

Görüntüler için gerekli veri ön işleme ve normalizasyon adımları belirlenecektir.

## Aşama 2 — Eğitim, Doğrulama ve Test Veri Ayrımı

Hazırlanan veri seti üç ana bölüme ayrılacaktır.

- Eğitim kümesi: Veri setinin yaklaşık %70–80'i.
- Doğrulama kümesi: Veri setinin yaklaşık %10–15'i.
- Test kümesi: Kalan veri örnekleri.

Eğitim kümesi modellerin öğrenme sürecinde kullanılacaktır.

Doğrulama kümesi model performansının takibi ve hiperparametre ayarlarında kullanılacaktır.

Test kümesi yalnızca eğitim ve optimizasyon tamamlandıktan sonra modellerin genelleme yeteneğinin objektif olarak değerlendirilmesi amacıyla kullanılacaktır.

## Aşama 3 — Transfer Öğrenme ile Model Adaptasyonu

VGG16 ve ResNet50 modelleri ImageNet üzerinde önceden eğitilmiş ağırlıklarla yüklenecektir.

Modellerin evrişimsel özellik çıkarıcı katmanları başlangıç aşamasında dondurulacaktır.

Orijinal sınıflandırma katmanları kaldırılacaktır.

Modellere sürekli bir görüş mesafesi değeri tahmin eden tek çıkışlı regresyon başlığı eklenecektir.

Modeller FRIDA ve FRIDA2 veri setlerinden elde edilen regresyon etiketleri kullanılarak eğitilecektir.

Kayıp fonksiyonu olarak MAE kullanılacaktır.

## Aşama 4 — Model Karşılaştırması ve Dikkat Mekanizması

VGG16 ve ResNet50 modellerinin performansı test veri seti üzerinde MAE metriği kullanılarak karşılaştırılacaktır.

En düşük MAE değerini sağlayan model nihai temel mimari olarak seçilecektir.

Seçilen modele bir Dikkat Mekanizması entegre edilecektir.

Dikkat Mekanizmasının modelin görüntülerdeki kritik uzamsal bölgelere odaklanması ve MAE değerini iyileştirmesi hedeflenmektedir.

Dikkat Mekanizmasının MAE üzerindeki etkisi temel model ile karşılaştırılarak raporlanacaktır.

## Aşama 5 — Web Tabanlı Prototip

Optimize edilen nihai model Flask API kullanılarak bir web sunucusuna entegre edilecektir.

HTML ve CSS kullanılarak basit bir kullanıcı arayüzü geliştirilecektir.

Kullanıcı sisteme bir görüntü yükleyebilecektir.

Model yüklenen görüntü üzerinden görüş mesafesi tahmini gerçekleştirecektir.

Tahmin sonucu kullanıcı arayüzünde gösterilecektir.