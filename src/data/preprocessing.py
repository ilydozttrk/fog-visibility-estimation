"""
preprocessing.py

FRIDA veri seti için görüntü ön işleme işlemlerini gerçekleştirir.

Görevler:
- Görüntüleri yükleme
- Yeniden boyutlandırma (224x224)
- Normalizasyon
- İşlenmiş görüntüleri kaydetme
"""

from pathlib import Path
from PIL import Image


def load_image(image_path: Path) -> Image.Image:
    """
    Verilen dosya yolundaki görüntüyü yükler ve RGB formatına dönüştürür.

    Parameters
    ----------
    image_path : Path
        Yüklenecek görüntünün dosya yolu.

    Returns
    -------
    Image.Image
        RGB renk modunda yüklenmiş Pillow görüntüsü.

    Raises
    ------
    FileNotFoundError
        Görüntü dosyası bulunamazsa.
    ValueError
        Dosya geçerli bir görüntü olarak açılamazsa.
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Görüntü dosyası bulunamadı: {image_path}")

    if not image_path.is_file():
        raise ValueError(f"Belirtilen yol bir dosya değil: {image_path}")

    try:
        with Image.open(image_path) as image:
            return image.convert("RGB").copy()
    except OSError as error:
        raise ValueError(
            f"Görüntü dosyası açılamadı veya bozuk: {image_path}"
        ) from error


from PIL import Image, ImageOps

def resize_image(image: Image.Image,
                 target_size: tuple[int, int] = (224, 224)) -> Image.Image:
    """
    Görüntüyü en-boy oranını koruyarak hedef boyuta getirir.
    """

    return ImageOps.pad(
        image,
        target_size,
        method=Image.Resampling.LANCZOS,
        color=(0, 0, 0)
    )

def normalize_image(image: Image.Image) -> Image.Image:
    """
    Görüntüyü değiştirmeden döndürür.

    Not:
    Gerçek model normalizasyonu eğitim aşamasında VGG16 ve ResNet50
    modellerine ait resmi preprocess_input fonksiyonlarıyla uygulanacaktır.
    """
    return image

def save_image(image: Image.Image, output_path: Path) -> None:
    """
    İşlenmiş görüntüyü belirtilen dosya yoluna kaydeder.

    Parameters
    ----------
    image : Image.Image
        Kaydedilecek Pillow görüntüsü.
    output_path : Path
        Görüntünün kaydedileceği dosya yolu.
    """
    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        image.save(output_path)
    except OSError as error:
        raise ValueError(
            f"Görüntü kaydedilemedi: {output_path}"
        ) from error

def preprocess_dataset(
    input_dir: Path,
    output_dir: Path,
    target_size: tuple[int, int] = (224, 224),
) -> tuple[int, list[tuple[str, str]]]:
    """
    Belirtilen klasördeki tüm PNG görüntülerine ön işleme uygular.

    Parameters
    ----------
    input_dir : Path
        Ham görüntülerin bulunduğu klasör.
    output_dir : Path
        İşlenmiş görüntülerin kaydedileceği klasör.
    target_size : tuple[int, int]
        Görüntülerin dönüştürüleceği hedef boyut.

    Returns
    -------
    tuple[int, list[tuple[str, str]]]
        Başarıyla işlenen görüntü sayısı ve başarısız dosyaların listesi.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        raise FileNotFoundError(
            f"Girdi klasörü bulunamadı: {input_dir}"
        )

    if not input_dir.is_dir():
        raise ValueError(
            f"Belirtilen girdi yolu bir klasör değil: {input_dir}"
        )

    image_paths = sorted(input_dir.glob("*.png"))

    if not image_paths:
        raise FileNotFoundError(
            f"İşlenecek PNG görüntüsü bulunamadı: {input_dir}"
        )

    processed_count = 0
    failed_files: list[tuple[str, str]] = []

    print(f"Toplam görüntü sayısı: {len(image_paths)}")
    print("Ön işleme başlatılıyor...")

    for image_path in image_paths:
        try:
            image = load_image(image_path)
            resized_image = resize_image(image, target_size)
            normalized_image = normalize_image(resized_image)

            output_path = output_dir / image_path.name
            save_image(normalized_image, output_path)

            processed_count += 1

        except (FileNotFoundError, ValueError) as error:
            failed_files.append((image_path.name, str(error)))

    return processed_count, failed_files

def main():
    """FRIDA veri seti ön işleme pipeline'ını çalıştırır."""
    project_root = Path(__file__).resolve().parents[2]

    input_dir = project_root / "data" / "raw" / "frida"
    output_dir = project_root / "data" / "processed" / "frida"

    processed_count, failed_files = preprocess_dataset(
        input_dir=input_dir,
        output_dir=output_dir,
        target_size=(224, 224),
    )

    print("\nÖn işleme tamamlandı.")
    print(f"Başarıyla işlenen görüntü: {processed_count}")
    print(f"Başarısız görüntü: {len(failed_files)}")
    print(f"Çıktı klasörü: {output_dir}")

    if failed_files:
        print("\nİşlenemeyen dosyalar:")

        for filename, error_message in failed_files:
            print(f"- {filename}: {error_message}")

if __name__ == "__main__":
    main()