# Sisli Hava Koşullarında Görüş Mesafesi Tahmini

Bu proje, sisli hava koşullarında görüntü tabanlı görüş mesafesi tahmini için transfer öğrenme temelli VGG16 ve ResNet50 CNN mimarilerinin karşılaştırmalı analizini gerçekleştirmeyi amaçlamaktadır.

## Araştırmanın Amacı

VGG16 ve ResNet50 modellerinin sürekli görüş mesafesi regresyonu görevindeki performansları Ortalama Mutlak Hata (MAE) metriği kullanılarak karşılaştırılacaktır.

Test veri seti üzerinde en düşük MAE değerini sağlayan model seçilecek ve seçilen modele bir Dikkat Mekanizması entegre edilecektir.

## Araştırma Sorusu

Transfer öğrenme yöntemi ile görüntü tabanlı görüş mesafesi tahmini görevine adapte edilen VGG16 ve ResNet50 mimarilerinden hangisi daha düşük MAE değeri sağlayarak Akıllı Ulaşım Sistemleri entegrasyonu için daha uygun bir temel oluşturur?

## Planlanan Proje Süreci

1. FRIDA ve FRIDA2 veri setlerinin hazırlanması.
2. Sürekli görüş mesafesi regresyon etiketlerinin hazırlanması.
3. Veri ön işleme ve normalizasyon sürecinin geliştirilmesi.
4. Eğitim, doğrulama ve test veri ayrımının gerçekleştirilmesi.
5. VGG16 modelinin transfer öğrenme ile adapte edilmesi.
6. ResNet50 modelinin transfer öğrenme ile adapte edilmesi.
7. Modellerin MAE metriği ile karşılaştırılması.
8. En iyi modele Dikkat Mekanizması entegrasyonu.
9. Gerçek dünya veri setleri ile ince ayar.
10. Flask API ve HTML/CSS tabanlı web prototipinin geliştirilmesi.

## Proje Durumu

Proje kurulumu ve veri seti araştırma aşaması.