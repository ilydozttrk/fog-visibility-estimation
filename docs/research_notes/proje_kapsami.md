# Proje Kapsamı

## Proje Başlığı

Transfer Öğrenme Temelli CNN Mimarilerinin Görüş Mesafesi Tahmininde Karşılaştırmalı Analizi

## Araştırma Problemi

Kötü hava koşullarına bağlı düşük görüş mesafesi, karayolları trafiğinde önemli bir kaza riski oluşturmaktadır. Mevcut güvenlik sistemlerinde kullanılan sensör tabanlı yöntemler, yüksek maliyetleri ve sınırlı kapsama alanları nedeniyle yaygın entegrasyonda zorluk oluşturabilmektedir.

Bu proje, mevcut yol gözetleme kameralarının kullanıldığı görüntü tabanlı bir yapay zekâ yaklaşımıyla daha düşük maliyetli görüş mesafesi tahmini yapılabilirliğini araştırmaktadır.

## Araştırma Sorusu

Transfer öğrenme yöntemi ile görüntü tabanlı görüş mesafesi tahmini görevine adapte edilen VGG16 ve ResNet50 mimarilerinden hangisi, sentetik ve gerçek dünya veri kümelerinde en düşük MAE değerini sunarak Akıllı Ulaşım Sistemleri entegrasyonu için daha uygun bir temel oluşturur?

## Hipotez

ResNet50 mimarisinin, artık bağlantıları sayesinde transfer öğrenme ile adapte edildiğinde, aynı veri seti ve eğitim parametreleri altında VGG16 mimarisine kıyasla istatistiksel olarak anlamlı düzeyde daha düşük MAE değerleri üretmesi beklenmektedir.

## Projenin Temel Amacı

Sisli hava koşullarında yol güvenliğini artırmak amacıyla, transfer öğrenme yöntemi kullanılarak önceden eğitilmiş VGG16 ve ResNet50 CNN modellerini karşılaştırmalı olarak analiz etmek, görüntü tabanlı görüş mesafesi tahmini gerçekleştirmek ve Flask API ile Akıllı Ulaşım Sistemleri entegrasyonuna uygun fonksiyonel bir prototip geliştirmektir.

## Temel Performans Metriği

Ortalama Mutlak Hata (Mean Absolute Error — MAE).

MAE değeri, metre cinsinden görüş mesafesi tahmin hatasını değerlendirmek için kullanılmaktadır. İlk VGG16 baseline eğitimi sonucunda elde edilen en düşük doğrulama hatası **69.9705 metre** olarak ölçülmüş ve araştırma önerisinde belirlenen performans hedefi başarıyla karşılanmıştır.

## Planlanan Veri Setleri

- FRIDA
- FRIDA2
- FVEI
- FHVI

FRIDA ve FRIDA2 veri setleri kullanılarak derinlik haritaları üzerinden farklı görüş mesafelerini temsil eden sentetik görüntüler oluşturulmuştur.

Oluşturulan veri kümesi toplam **84 sahne** ve **672 sentetik görüntüden** oluşmaktadır. Bu veri kümesi model geliştirme ve başlangıç eğitim sürecinde kullanılmaktadır.

Hazırlanan sentetik veri kümesi sahne bazlı olarak eğitim, doğrulama ve test kümelerine ayrılmıştır. Aynı temel sahneye ait tüm görüş mesafesi varyasyonları aynı alt kümede tutulmuş ve böylece veri sızıntısının önüne geçilmiştir.

Uygulanan veri dağılımı aşağıdaki şekildedir:

- Eğitim kümesi: **464 görüntü**
- Doğrulama kümesi: **96 görüntü**
- Test kümesi: **112 görüntü**

FVEI ve FHVI gibi gerçek dünya veri setlerinin erişilebilirlik ve uygunluk durumları araştırılacaktır. Uygun gerçek dünya verileri, modelin ince ayar ve gerçek dünya koşullarındaki değerlendirme süreçlerinde kullanılacaktır.

## Karşılaştırılacak Modeller

• VGG16 (Tamamlandı)

- ImageNet ön eğitimli ağırlıklar kullanıldı.
- Transfer öğrenme tabanlı regresyon modeli geliştirildi.
- 20 epoch eğitim gerçekleştirildi.
- En iyi Validation MAE: 69.9705 m (18. epoch)
- Bağımsız test kümesi üzerinde Test MAE: 66.7227 m
- Otomatik değerlendirme pipeline'ı geliştirildi.
- Tahmin CSV dosyaları, JSON özetleri, Markdown raporları ve değerlendirme grafikleri oluşturuldu.
- İlk baseline modeli başarıyla tamamlandı.

• ResNet50

Her iki model de ImageNet üzerinde önceden eğitilmiş ağırlıklarla transfer öğrenme yaklaşımı kullanılarak görüş mesafesi tahmini görevine adapte edilecektir.

Modellerin orijinal sınıflandırma katmanları kaldırılacak ve sürekli bir görüş mesafesi değeri tahmin eden regresyon çıkışı kullanılacaktır.

VGG16 modeli ImageNet üzerinde önceden eğitilmiş ağırlıklarla projeye entegre edilmiştir. Modelin evrişimsel (backbone) katmanları dondurulmuş ve orijinal sınıflandırma başlığı yerine tek çıkışlı bir regresyon başlığı geliştirilmiştir.

Model için eğitim, doğrulama ve checkpoint mekanizmalarını içeren eğitim altyapısı tamamlanmış; Adam optimizasyon algoritması ve Ortalama Mutlak Hata (L1 Loss / MAE) kullanılarak ilk tam eğitim gerçekleştirilmiştir.

Toplam **20 epoch** süren ilk eğitim sonunda model **18. epochta 69.9705 metre Validation MAE** değerine ulaşmış ve araştırma önerisinde belirlenen **MAE < 100 metre** performans hedefini başarıyla karşılamıştır.

Deney sonuçları standart deney kayıt dosyalarında saklanmış, eğitim geçmişi grafiksel olarak raporlanmış ve en başarılı model otomatik olarak checkpoint şeklinde kaydedilmiştir.

Aynı transfer öğrenme, veri bölünmesi ve eğitim yaklaşımı bir sonraki aşamada ResNet50 modeli için uygulanacak; iki model aynı deney koşulları altında karşılaştırılacaktır.

VGG16 için eğitim, doğrulama ve checkpoint kayıt süreçlerini içeren temel eğitim altyapısı geliştirilmiş ve bir epoch'luk başlangıç testi başarıyla tamamlanmıştır.

Aynı transfer öğrenme ve regresyon yaklaşımı ilerleyen aşamada ResNet50 mimarisi için de uygulanacaktır.

## Model Karşılaştırma Yaklaşımı

VGG16 ve ResNet50 modelleri aynı sentetik veri kümesi, aynı sahne bazlı eğitim/doğrulama/test ayrımı ve aynı eğitim parametreleri altında değerlendirilecektir.

Adil ve tekrarlanabilir bir karşılaştırma sağlamak amacıyla modellerde aynı görüntü boyutu, normalizasyon yaklaşımı, batch büyüklüğü, veri ayrımı, rastgelelik tohumu ve temel değerlendirme metriği kullanılacaktır.

Deney parametreleri merkezi bir yapılandırma dosyasında tutulmakta ve deneylerin tekrarlanabilirliği için sabit rastgelelik tohumu kullanılmaktadır.

Modellerin temel performans karşılaştırması test veri seti üzerinde elde edilen MAE değerleri kullanılarak gerçekleştirilecektir.

Bu karşılaştırma sonucunda en düşük test MAE değerini sağlayan model nihai temel mimari olarak seçilecektir.

## Nihai Model Seçimi ve Dikkat Mekanizması

Test veri seti üzerinde en düşük MAE değerini sağlayan model nihai temel mimari olarak seçilecektir.

Seçilen modele bir Dikkat Mekanizması entegre edilecektir.

Dikkat Mekanizmasının modelin görüntülerdeki kritik uzamsal bölgelere daha fazla odaklanmasını sağlaması hedeflenmektedir.

Dikkat Mekanizması entegrasyonunun ardından model yeniden değerlendirilecek ve elde edilen MAE değeri temel modelin MAE değeri ile karşılaştırılacaktır.

Dikkat Mekanizmasının model performansına etkisi bu karşılaştırma üzerinden raporlanacaktır.

## Nihai Prototip

Optimize edilen nihai model Flask API kullanılarak hafif bir web sunucusuna entegre edilecektir.

HTML ve CSS kullanılarak basit ve fonksiyonel bir kullanıcı arayüzü geliştirilecektir.

Kullanıcı sisteme bir görüntü yükleyebilecek ve model yüklenen görüntü üzerinden görüş mesafesi tahmini gerçekleştirecektir.

Tahmin edilen görüş mesafesi sonucu kullanıcı arayüzünde gösterilecektir.

## Proje Sınırları

- Temel araştırma problemi sürekli görüş mesafesi regresyonudur.
- Projenin ana amacı sis sınıflandırması yapmak değildir.
- Ana model karşılaştırması VGG16 ve ResNet50 mimarileri arasında gerçekleştirilecektir.
- Temel performans metriği MAE olacaktır.
- Dikkat Mekanizması, temel VGG16 ve ResNet50 karşılaştırması tamamlandıktan sonra yalnızca seçilen en iyi modele uygulanacaktır.
- Gerçek dünya verilerinin kullanımı erişilebilirlik ve veri uygunluğu doğrultusunda araştırma önerisinde tanımlanan yaklaşım çerçevesinde gerçekleştirilecektir.
- Web prototipi basit ve fonksiyonel tutulacaktır.
- Flask API, model tahmininin web tabanlı kullanımını göstermek amacıyla kullanılacaktır.
- Proje uygulaması onaylanan TÜBİTAK 2209-A araştırma önerisinin bilimsel kapsamı dışına çıkmayacaktır.
- Eğitim sürecinde veri sızıntısını önlemek amacıyla eğitim, doğrulama ve test ayrımı sahne bazlı gerçekleştirilecektir.
- Aynı temel sahneye ait tüm görüntüler tek bir veri alt kümesinde tutulacaktır.
- VGG16 ve ResNet50 modelleri mümkün olduğunca aynı eğitim ve değerlendirme koşullarında karşılaştırılacaktır.
- Model seçimi doğrulama performansına göre yapılacak, nihai karşılaştırma ise bağımsız test kümesi üzerinde gerçekleştirilecektir.
- Test veri kümesi model geliştirme ve hiperparametre ayarlama süreçlerinde kullanılmayacaktır.

## Proje Uygulama İlkesi

Projenin bütün teknik ve bilimsel kararlarında onaylanan TÜBİTAK 2209-A Araştırma Önerisi Formu temel kaynak olarak kabul edilecektir.

Roadmap, araştırma önerisinde tanımlanan çalışmanın günlük uygulama sırasını belirlemek amacıyla kullanılacaktır.

Araştırma önerisinin kapsamını değiştiren yeni bir araştırma problemi, temel model mimarisi veya proje amacı eklenmeyecektir.

Teknik uygulama sırasında alınması gereken kararlar, araştırma sorusu, hipotez, yöntem ve proje hedefleri ile uyumlu olacak şekilde değerlendirilecektir.

Geliştirilen kod, veri hazırlama adımları, deney parametreleri ve model sonuçları düzenli olarak dokümante edilecek; proje sürecinin tekrarlanabilir ve denetlenebilir olması sağlanacaktır.