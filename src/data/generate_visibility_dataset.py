from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from PIL import Image


# Proje ana dizini
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Ham veri dizinleri
RAW_DATASETS = {
    "frida": PROJECT_ROOT / "data" / "raw" / "frida",
    "frida2": PROJECT_ROOT / "data" / "raw" / "frida2",
}

# Üretilecek veri seti
OUTPUT_ROOT = PROJECT_ROOT / "data" / "generated"
OUTPUT_IMAGES_DIR = OUTPUT_ROOT / "images"
LABELS_CSV_PATH = OUTPUT_ROOT / "labels.csv"

# Metre cinsinden hedef görüş mesafeleri
VISIBILITY_LEVELS_M = (50, 80, 100, 150, 200, 300, 500, 800)

# Koschmieder kontrast eşiği
CONTRAST_THRESHOLD = 0.02

# Atmosferik ışık: beyaz/gri gökyüzü varsayımı
ATMOSPHERIC_LIGHT = np.array([1.0, 1.0, 1.0], dtype=np.float32)

# FRIDA ve FRIDA2 görüntü boyutu
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480


def visibility_to_beta(
    visibility_m: float,
    contrast_threshold: float = CONTRAST_THRESHOLD,
) -> float:
    """
    Görüş mesafesini atmosferik sönüm katsayısına dönüştürür.

    Koschmieder ilişkisi:
        beta = -ln(C_t) / V

    Args:
        visibility_m: Metre cinsinden görüş mesafesi.
        contrast_threshold: Görsel kontrast eşiği.

    Returns:
        Atmosferik sönüm katsayısı beta.
    """
    if visibility_m <= 0:
        raise ValueError("Görüş mesafesi sıfırdan büyük olmalıdır.")

    if not 0 < contrast_threshold < 1:
        raise ValueError("Kontrast eşiği 0 ile 1 arasında olmalıdır.")

    return -math.log(contrast_threshold) / visibility_m


def load_rgb_image(image_path: Path) -> np.ndarray:
    """
    RGB görüntüyü [0, 1] aralığında NumPy dizisi olarak yükler.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Görüntü bulunamadı: {image_path}")

    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image_array = np.asarray(image, dtype=np.float32) / 255.0

    expected_shape = (IMAGE_HEIGHT, IMAGE_WIDTH, 3)

    if image_array.shape != expected_shape:
        raise ValueError(
            f"Beklenmeyen görüntü boyutu: {image_array.shape}. "
            f"Beklenen: {expected_shape}"
        )

    return image_array


def load_depth_map(depth_path: Path) -> np.ndarray:
    """
    FRIDA .fdd derinlik haritasını okur ve milimetreden metreye çevirir.

    FRIDA'nın displayall.m dosyasında derinlik haritaları:
        depth_map_m = load(file) / 1000.0
    biçiminde kullanılmaktadır.
    """
    if not depth_path.exists():
        raise FileNotFoundError(f"Derinlik haritası bulunamadı: {depth_path}")

    depth_map_mm = np.loadtxt(
    depth_path,
    dtype=np.float32,
    comments="%",
    )

    expected_shape = (IMAGE_HEIGHT, IMAGE_WIDTH)

    if depth_map_mm.shape != expected_shape:
        raise ValueError(
            f"Beklenmeyen derinlik haritası boyutu: {depth_map_mm.shape}. "
            f"Beklenen: {expected_shape}"
        )

    depth_map_m = depth_map_mm / 1000.0

    if not np.isfinite(depth_map_m).all():
        raise ValueError(f"Geçersiz derinlik değeri bulundu: {depth_path}")

    if np.any(depth_map_m < 0):
        raise ValueError(f"Negatif derinlik değeri bulundu: {depth_path}")

    return depth_map_m


def generate_homogeneous_fog(
    clear_image: np.ndarray,
    depth_map_m: np.ndarray,
    visibility_m: float,
    atmospheric_light: np.ndarray = ATMOSPHERIC_LIGHT,
) -> tuple[np.ndarray, float]:
    """
    Atmosferik saçılım modeliyle homojen sisli görüntü üretir.

    I(x) = J(x)t(x) + A(1 - t(x))
    t(x) = exp(-beta * d(x))
    """
    beta = visibility_to_beta(visibility_m)

    transmission = np.exp(-beta * depth_map_m)
    transmission = np.clip(transmission, 0.0, 1.0)
    transmission = transmission[..., np.newaxis]

    foggy_image = (
        clear_image * transmission
        + atmospheric_light * (1.0 - transmission)
    )

    foggy_image = np.clip(foggy_image, 0.0, 1.0)

    return foggy_image, beta


def save_image(image_array: np.ndarray, output_path: Path) -> None:
    """
    [0, 1] aralığındaki görüntüyü PNG olarak kaydeder.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image_uint8 = np.round(image_array * 255.0).astype(np.uint8)
    Image.fromarray(image_uint8, mode="RGB").save(output_path)


def find_scene_pairs(dataset_dir: Path) -> list[tuple[str, Path, Path]]:
    """
    Her sahne için açık görüntüyü ve derinlik haritasını eşleştirir.

    Açık görüntü örneği:
        LIma-000001.png

    Derinlik haritası adları veri setine göre şu biçimlerde olabilir:
        Dmap-000001.fdd
        LDep-000001.fdd
    """
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Veri seti klasörü bulunamadı: {dataset_dir}")

    clear_images = sorted(dataset_dir.glob("LIma-*.png"))
    scene_pairs: list[tuple[str, Path, Path]] = []

    for clear_image_path in clear_images:
        scene_id = clear_image_path.stem.split("-")[-1]

        depth_candidates = [
            dataset_dir / f"Dmap-{scene_id}.fdd",
            dataset_dir / f"LDep-{scene_id}.fdd",
        ]

        depth_path = next(
            (candidate for candidate in depth_candidates if candidate.exists()),
            None,
        )

        if depth_path is None:
            print(
                f"UYARI: Sahne {scene_id} için derinlik haritası bulunamadı. "
                "Sahne atlandı."
            )
            continue

        scene_pairs.append((scene_id, clear_image_path, depth_path))

    return scene_pairs


def generate_dataset() -> None:
    """
    FRIDA ve FRIDA2 açık görüntülerinden çok seviyeli sentetik sis
    veri seti ve labels.csv üretir.
    """
    OUTPUT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    LABELS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | float]] = []
    total_generated = 0
    total_failed = 0

    for dataset_name, dataset_dir in RAW_DATASETS.items():
        print(f"\nVeri seti işleniyor: {dataset_name}")
        print(f"Kaynak: {dataset_dir}")

        try:
            scene_pairs = find_scene_pairs(dataset_dir)
        except FileNotFoundError as error:
            print(f"HATA: {error}")
            continue

        print(f"Eşleştirilen sahne sayısı: {len(scene_pairs)}")

        for scene_id, clear_image_path, depth_path in scene_pairs:
            try:
                clear_image = load_rgb_image(clear_image_path)
                depth_map_m = load_depth_map(depth_path)

                for visibility_m in VISIBILITY_LEVELS_M:
                    foggy_image, beta = generate_homogeneous_fog(
                        clear_image=clear_image,
                        depth_map_m=depth_map_m,
                        visibility_m=visibility_m,
                    )

                    filename = (
                        f"{dataset_name}_scene{scene_id}_"
                        f"v{visibility_m:04d}.png"
                    )

                    relative_image_path = Path("images") / filename
                    output_image_path = OUTPUT_ROOT / relative_image_path

                    save_image(foggy_image, output_image_path)

                    rows.append(
                        {
                            "filename": relative_image_path.as_posix(),
                            "visibility_m": float(visibility_m),
                            "scene_id": scene_id,
                            "source_dataset": dataset_name,
                            "beta": beta,
                            "clear_image": clear_image_path.name,
                            "depth_map": depth_path.name,
                        }
                    )

                    total_generated += 1

            except (
                FileNotFoundError,
                ValueError,
                OSError,
            ) as error:
                total_failed += 1
                print(
                    f"HATA: {dataset_name} sahne {scene_id} işlenemedi: "
                    f"{error}"
                )

    fieldnames = [
        "filename",
        "visibility_m",
        "scene_id",
        "source_dataset",
        "beta",
        "clear_image",
        "depth_map",
    ]

    with LABELS_CSV_PATH.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\nVeri üretimi tamamlandı.")
    print(f"Üretilen görüntü sayısı: {total_generated}")
    print(f"Başarısız sahne sayısı: {total_failed}")
    print(f"Görüntü klasörü: {OUTPUT_IMAGES_DIR}")
    print(f"Etiket dosyası: {LABELS_CSV_PATH}")


def main() -> None:
    generate_dataset()


if __name__ == "__main__":
    main()