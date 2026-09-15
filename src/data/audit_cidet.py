from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
CIDET_INTERIM = ROOT / "data" / "interim" / "cidet"
IMAGE_DIR = CIDET_INTERIM / "images"


def find_required_file(filename: str) -> Path:
    """Find exactly one required CIDET file recursively."""
    matches = list(CIDET_INTERIM.rglob(filename))

    if not matches:
        raise FileNotFoundError(
            f"Could not find required CIDET file: {filename}"
        )

    if len(matches) > 1:
        locations = "\n".join(str(path) for path in matches)
        raise RuntimeError(
            f"Found multiple files named {filename}:\n{locations}"
        )

    return matches[0]


def find_image_files() -> dict[str, Path]:
    """Find all CIDET image files recursively."""
    image_paths: dict[str, Path] = {}

    for path in IMAGE_DIR.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            if path.name in image_paths:
                raise RuntimeError(
                    f"Duplicate image filename detected: {path.name}"
                )

            image_paths[path.name] = path

    return image_paths


def load_split_csv(path: Path) -> list[str]:
    """Load an official CIDET split CSV without assuming a header."""
    df = pd.read_csv(path, header=None)

    if df.shape[1] != 1:
        raise ValueError(
            f"{path.name} expected 1 column, found {df.shape[1]}"
        )

    return df.iloc[:, 0].astype(str).str.strip().tolist()


def main() -> None:
    annotation_path = find_required_file(
        "tabular_data_and_visibility_annotation.csv"
    )
    train_path = find_required_file("images_train.csv")
    val_path = find_required_file("images_val.csv")
    test_path = find_required_file("images_test.csv")

    print("\n=== CIDET DATA AUDIT ===")

    print("\n--- DISCOVERED FILES ---")
    print(f"Annotation: {annotation_path}")
    print(f"Train:      {train_path}")
    print(f"Validation: {val_path}")
    print(f"Test:       {test_path}")

    image_files = find_image_files()
    annotations = pd.read_csv(annotation_path)

    train_files = load_split_csv(train_path)
    val_files = load_split_csv(val_path)
    test_files = load_split_csv(test_path)

    print("\n--- FILE COUNTS ---")
    print(f"Images found:         {len(image_files)}")
    print(f"Annotation rows:      {len(annotations)}")
    print(f"Train split:          {len(train_files)}")
    print(f"Validation split:     {len(val_files)}")
    print(f"Test split:           {len(test_files)}")
    print(
        "Total official split: "
        f"{len(train_files) + len(val_files) + len(test_files)}"
    )

    print("\n--- ANNOTATION COLUMNS ---")
    for column in annotations.columns:
        print(column)

    image_column = "image_name"
    target_column = "visibility estimation average"

    if image_column not in annotations.columns:
        raise KeyError(
            f"Required annotation column not found: {image_column}"
        )

    if target_column not in annotations.columns:
        raise KeyError(
            f"Required target column not found: {target_column}"
        )

    annotated_names = set(
        annotations[image_column].astype(str).str.strip()
    )
    image_names = set(image_files.keys())

    missing_images = annotated_names - image_names
    images_without_annotation = image_names - annotated_names

    print("\n--- IMAGE / ANNOTATION CONSISTENCY ---")
    print(
        "Annotated files missing from image directory: "
        f"{len(missing_images)}"
    )
    print(
        "Images without annotation:                   "
        f"{len(images_without_annotation)}"
    )

    if missing_images:
        print("\nMissing image examples:")
        for filename in sorted(missing_images)[:10]:
            print(f"  {filename}")

    if images_without_annotation:
        print("\nUnannotated image examples:")
        for filename in sorted(images_without_annotation)[:10]:
            print(f"  {filename}")

    train_set = set(train_files)
    val_set = set(val_files)
    test_set = set(test_files)

    print("\n--- SPLIT OVERLAP CHECK ---")
    print(f"Train ∩ Val:  {len(train_set & val_set)}")
    print(f"Train ∩ Test: {len(train_set & test_set)}")
    print(f"Val ∩ Test:   {len(val_set & test_set)}")

    official_split = train_set | val_set | test_set

    split_missing_images = official_split - image_names
    split_missing_annotations = official_split - annotated_names

    annotated_not_in_split = annotated_names - official_split

    print("\n--- OFFICIAL SPLIT CONSISTENCY ---")
    print(
        "Unique official split entries:             "
        f"{len(official_split)}"
    )
    print(
        "Official split entries missing image:      "
        f"{len(split_missing_images)}"
    )
    print(
        "Official split entries missing annotation: "
        f"{len(split_missing_annotations)}"
    )
    print(
        "Annotated entries not in official split:   "
        f"{len(annotated_not_in_split)}"
    )

    target = pd.to_numeric(
        annotations[target_column],
        errors="coerce",
    )

    print("\n--- VISIBILITY TARGET ---")
    print(f"Valid target values:   {target.notna().sum()}")
    print(f"Missing target values: {target.isna().sum()}")

    print("\nVisibility statistics [m]:")
    print(target.describe())

    observer_columns = [
        column
        for column in annotations.columns
        if "visibility estimation" in column.lower()
        and column != target_column
    ]

    print("\n--- OBSERVER COLUMNS ---")

    if observer_columns:
        for column in observer_columns:
            print(column)
    else:
        print("No additional observer columns detected.")

    print("\n=== AUDIT COMPLETE ===")


if __name__ == "__main__":
    main()