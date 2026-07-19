from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATED_ROOT = PROJECT_ROOT / "data" / "generated"
IMAGES_DIR = GENERATED_ROOT / "images"
LABELS_CSV_PATH = GENERATED_ROOT / "labels.csv"

FIGURES_DIR = PROJECT_ROOT / "figures"
OUTPUT_FIGURE_PATH = FIGURES_DIR / "visibility_levels_sample.png"

EXPECTED_VISIBILITY_LEVELS = {
    50.0,
    80.0,
    100.0,
    150.0,
    200.0,
    300.0,
    500.0,
    800.0,
}

EXPECTED_TOTAL_IMAGES = 672
EXPECTED_TOTAL_SCENES = 84


def read_labels() -> list[dict[str, str]]:
    """
    labels.csv dosyasını okur.
    """
    if not LABELS_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Etiket dosyası bulunamadı: {LABELS_CSV_PATH}"
        )

    with LABELS_CSV_PATH.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    if not rows:
        raise ValueError("labels.csv boş.")

    return rows


def validate_dataset(rows: list[dict[str, str]]) -> None:
    """
    Etiketler ile görüntü dosyalarının tutarlılığını kontrol eder.
    """
    errors: list[str] = []

    filenames = [row["filename"] for row in rows]
    visibility_values = [
        float(row["visibility_m"])
        for row in rows
    ]

    scene_keys = {
        (
            row["source_dataset"],
            row["scene_id"],
        )
        for row in rows
    }

    source_counts = Counter(
        row["source_dataset"]
        for row in rows
    )

    visibility_counts = Counter(visibility_values)

    duplicate_filenames = [
        filename
        for filename, count in Counter(filenames).items()
        if count > 1
    ]

    missing_files = []

    for filename in filenames:
        image_path = GENERATED_ROOT / filename

        if not image_path.exists():
            missing_files.append(filename)

    unexpected_visibility_levels = (
        set(visibility_values)
        - EXPECTED_VISIBILITY_LEVELS
    )

    if len(rows) != EXPECTED_TOTAL_IMAGES:
        errors.append(
            f"Beklenen satır sayısı {EXPECTED_TOTAL_IMAGES}, "
            f"bulunan {len(rows)}."
        )

    if len(scene_keys) != EXPECTED_TOTAL_SCENES:
        errors.append(
            f"Beklenen sahne sayısı {EXPECTED_TOTAL_SCENES}, "
            f"bulunan {len(scene_keys)}."
        )

    if duplicate_filenames:
        errors.append(
            f"Tekrarlanan dosya adı sayısı: "
            f"{len(duplicate_filenames)}."
        )

    if missing_files:
        errors.append(
            f"Eksik görüntü dosyası sayısı: "
            f"{len(missing_files)}."
        )

    if unexpected_visibility_levels:
        errors.append(
            "Beklenmeyen görüş mesafeleri bulundu: "
            f"{sorted(unexpected_visibility_levels)}"
        )

    print("\nVERİ SETİ DOĞRULAMA SONUÇLARI")
    print("-" * 40)
    print(f"CSV satır sayısı: {len(rows)}")
    print(f"Bağımsız sahne sayısı: {len(scene_keys)}")
    print(f"Tekrarlanan dosya adı: {len(duplicate_filenames)}")
    print(f"Eksik görüntü dosyası: {len(missing_files)}")

    print("\nKaynak veri seti dağılımı:")

    for source, count in sorted(source_counts.items()):
        print(f"  {source}: {count}")

    print("\nGörüş mesafesi dağılımı:")

    for visibility_m in sorted(visibility_counts):
        print(
            f"  {visibility_m:>6.0f} m: "
            f"{visibility_counts[visibility_m]}"
        )

    if errors:
        print("\nDOĞRULAMA BAŞARISIZ")

        for error in errors:
            print(f"  - {error}")

        raise RuntimeError(
            "Üretilen veri setinde doğrulama hataları bulundu."
        )

    print("\nDOĞRULAMA BAŞARILI")
    print("Veri seti sayısal olarak tutarlı.")


def select_sample_scene(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """
    Sekiz görüş seviyesinin tamamına sahip ilk sahneyi seçer.
    """
    grouped_rows: dict[
        tuple[str, str],
        list[dict[str, str]],
    ] = {}

    for row in rows:
        key = (
            row["source_dataset"],
            row["scene_id"],
        )

        grouped_rows.setdefault(key, []).append(row)

    for key in sorted(grouped_rows):
        scene_rows = grouped_rows[key]

        scene_visibility_levels = {
            float(row["visibility_m"])
            for row in scene_rows
        }

        if scene_visibility_levels == EXPECTED_VISIBILITY_LEVELS:
            return sorted(
                scene_rows,
                key=lambda row: float(row["visibility_m"]),
            )

    raise ValueError(
        "Sekiz görüş seviyesinin tamamına sahip sahne bulunamadı."
    )


def visualize_sample_scene(
    scene_rows: list[dict[str, str]],
) -> None:
    """
    Aynı sahnenin farklı görüş seviyelerini tek figürde gösterir.
    """
    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axes = plt.subplots(
        nrows=2,
        ncols=4,
        figsize=(16, 8),
    )

    for axis, row in zip(axes.flat, scene_rows):
        image_path = GENERATED_ROOT / row["filename"]

        with Image.open(image_path) as image:
            axis.imshow(image.convert("RGB"))

        visibility_m = float(row["visibility_m"])

        axis.set_title(f"{visibility_m:.0f} m")
        axis.axis("off")

    source_dataset = scene_rows[0]["source_dataset"]
    scene_id = scene_rows[0]["scene_id"]

    figure.suptitle(
        f"Sentetik Sis Görüş Seviyeleri\n"
        f"Kaynak: {source_dataset} | Sahne: {scene_id}",
        fontsize=15,
    )

    figure.tight_layout()
    figure.savefig(
        OUTPUT_FIGURE_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    plt.show()

    print(
        f"\nÖrnek görselleştirme kaydedildi: "
        f"{OUTPUT_FIGURE_PATH}"
    )


def main() -> None:
    rows = read_labels()

    validate_dataset(rows)

    sample_scene_rows = select_sample_scene(rows)

    visualize_sample_scene(sample_scene_rows)


if __name__ == "__main__":
    main()