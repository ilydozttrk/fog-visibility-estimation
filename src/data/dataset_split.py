"""
dataset_split.py

FRIDA veri setini sahne bazlı olarak eğitim, doğrulama ve test
kümelerine ayırır.

Aynı sahneye ait farklı görüntü varyantlarının farklı veri
kümelerine dağılması engellenerek veri sızıntısı önlenir.
"""

from pathlib import Path
import random
import shutil


RANDOM_SEED = 42
TRAIN_SCENE_COUNT = 12
VALIDATION_SCENE_COUNT = 3
TEST_SCENE_COUNT = 3


def extract_scene_id(image_path: Path) -> str:
    """
    FRIDA görüntü dosyasının adından sahne kimliğini çıkarır.

    Örnek
    -----
    K080-000001.png -> 000001
    LIma-000018.png -> 000018

    Parameters
    ----------
    image_path : Path
        Sahne kimliği çıkarılacak görüntü dosyası.

    Returns
    -------
    str
        Altı basamaklı sahne kimliği.

    Raises
    ------
    ValueError
        Dosya adı beklenen FRIDA biçimine uymuyorsa.
    """
    image_path = Path(image_path)
    stem = image_path.stem

    if "-" not in stem:
        raise ValueError(
            f"Dosya adı beklenen FRIDA biçimine uymuyor: {image_path.name}"
        )

    scene_id = stem.rsplit("-", maxsplit=1)[-1]

    if not scene_id.isdigit() or len(scene_id) != 6:
        raise ValueError(
            f"Geçersiz sahne kimliği: {image_path.name}"
        )

    return scene_id


def group_images_by_scene(
    image_paths: list[Path],
) -> dict[str, list[Path]]:
    """
    Görüntüleri sahne kimliklerine göre gruplandırır.

    Parameters
    ----------
    image_paths : list[Path]
        Gruplandırılacak görüntü dosyaları.

    Returns
    -------
    dict[str, list[Path]]
        Anahtarı sahne kimliği, değeri o sahneye ait görüntü
        dosyalarının listesi olan sözlük.
    """
    scene_groups: dict[str, list[Path]] = {}

    for image_path in image_paths:
        scene_id = extract_scene_id(image_path)

        if scene_id not in scene_groups:
            scene_groups[scene_id] = []

        scene_groups[scene_id].append(image_path)

    for scene_id in scene_groups:
        scene_groups[scene_id] = sorted(scene_groups[scene_id])

    return scene_groups


def split_scene_ids(
    scene_ids: list[str],
    random_seed: int = RANDOM_SEED,
) -> tuple[list[str], list[str], list[str]]:
    """
    Sahne kimliklerini eğitim, doğrulama ve test kümelerine ayırır.

    Aynı sahneye ait tüm görüntüler aynı veri kümesinde kalır.

    Parameters
    ----------
    scene_ids : list[str]
        Bölünecek sahne kimlikleri.
    random_seed : int
        Tekrarlanabilir rastgele bölme için kullanılacak seed değeri.

    Returns
    -------
    tuple[list[str], list[str], list[str]]
        Eğitim, doğrulama ve test sahne kimlikleri.

    Raises
    ------
    ValueError
        Sahne sayısı beklenen toplamla uyuşmuyorsa.
    """
    expected_scene_count = (
        TRAIN_SCENE_COUNT
        + VALIDATION_SCENE_COUNT
        + TEST_SCENE_COUNT
    )

    if len(scene_ids) != expected_scene_count:
        raise ValueError(
            f"Beklenen sahne sayısı {expected_scene_count}, "
            f"bulunan sahne sayısı {len(scene_ids)}."
        )

    shuffled_scene_ids = sorted(scene_ids)

    random_generator = random.Random(random_seed)
    random_generator.shuffle(shuffled_scene_ids)

    train_end = TRAIN_SCENE_COUNT
    validation_end = train_end + VALIDATION_SCENE_COUNT

    train_scene_ids = sorted(
        shuffled_scene_ids[:train_end]
    )
    validation_scene_ids = sorted(
        shuffled_scene_ids[train_end:validation_end]
    )
    test_scene_ids = sorted(
        shuffled_scene_ids[validation_end:]
    )

    return (
        train_scene_ids,
        validation_scene_ids,
        test_scene_ids,
    )

def copy_split_images(
    scene_groups: dict[str, list[Path]],
    split_scene_ids: list[str],
    output_dir: Path,
) -> int:
    """
    Seçilen sahnelere ait görüntüleri hedef klasöre kopyalar.

    Parameters
    ----------
    scene_groups : dict[str, list[Path]]
        Sahne kimliklerine göre gruplanmış görüntüler.
    split_scene_ids : list[str]
        Kopyalanacak sahne kimlikleri.
    output_dir : Path
        Görüntülerin kopyalanacağı hedef klasör.

    Returns
    -------
    int
        Başarıyla kopyalanan toplam görüntü sayısı.

    Raises
    ------
    KeyError
        Belirtilen sahne kimliği gruplar içinde bulunmuyorsa.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copied_count = 0

    for scene_id in split_scene_ids:
        if scene_id not in scene_groups:
            raise KeyError(
                f"Sahne kimliği bulunamadı: {scene_id}"
            )

        for image_path in scene_groups[scene_id]:
            destination_path = output_dir / image_path.name

            shutil.copy2(
                image_path,
                destination_path,
            )

            copied_count += 1

    return copied_count


def main():
    """
    FRIDA veri setini sahne bazlı olarak eğitim,
    doğrulama ve test kümelerine ayırır.
    """
    project_root = Path(__file__).resolve().parents[2]

    input_dir = (
        project_root
        / "data"
        / "processed"
        / "frida"
    )

    split_root = (
        project_root
        / "data"
        / "splits"
    )

    train_dir = split_root / "train"
    validation_dir = split_root / "validation"
    test_dir = split_root / "test"

    image_paths = sorted(input_dir.glob("*.png"))

    scene_groups = group_images_by_scene(image_paths)

    scene_ids = sorted(scene_groups.keys())

    (
        train_scene_ids,
        validation_scene_ids,
        test_scene_ids,
    ) = split_scene_ids(scene_ids)

    train_count = copy_split_images(
        scene_groups,
        train_scene_ids,
        train_dir,
    )

    validation_count = copy_split_images(
        scene_groups,
        validation_scene_ids,
        validation_dir,
    )

    test_count = copy_split_images(
        scene_groups,
        test_scene_ids,
        test_dir,
    )

    print("\nVeri seti başarıyla bölündü.\n")

    print(f"Eğitim görüntü sayısı     : {train_count}")
    print(f"Doğrulama görüntü sayısı  : {validation_count}")
    print(f"Test görüntü sayısı       : {test_count}")

    print("\nKlasörler")

    print(f"Train      -> {train_dir}")
    print(f"Validation -> {validation_dir}")
    print(f"Test       -> {test_dir}")

if __name__ == "__main__":
    main()