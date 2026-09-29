"""Audit the author's partial FVEI ZIP and create a reproducible dataset manifest.

No image or derived label is committed to the repository. The last filename
field is the visibility in metres; directory 4 has a 500 m ceiling and is
kept separate from exact-label regression metrics.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
PATTERN = re.compile(r"(?:^|/)([0-4])/([0-4])-([0-9]+)-([0-9]+)\.jpg$")
LIMITS = {0: (0, 50), 1: (50, 100), 2: (100, 200), 3: (200, 500)}


def audit(source: Path, destination: Path) -> dict:
    groups = defaultdict(list)
    rejected = Counter()
    with zipfile.ZipFile(source) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            match = PATTERN.search(info.filename)
            if not match or match.group(1) != match.group(2):
                rejected["unexpected_name"] += 1
                continue
            level, _, _, label = map(int, match.groups())
            try:
                content = archive.read(info)
                with Image.open(io.BytesIO(content)) as image:
                    image.load()
                    if image.size != (1920, 1080) or image.format != "JPEG":
                        raise ValueError("unexpected image format or dimensions")
            except (OSError, ValueError, zipfile.BadZipFile):
                rejected["invalid_image"] += 1
                continue
            if level != 4 and not (LIMITS[level][0] <= label < LIMITS[level][1]):
                rejected["outside_level_range"] += 1
                continue
            if level == 4 and label != 500:
                rejected["unexpected_ceiling_label"] += 1
                continue
            groups[hashlib.sha256(content).hexdigest()].append(
                (info.filename, level, label)
            )

    rows = []
    for digest, copies in sorted(groups.items()):
        labels = {(level, value) for _, level, value in copies}
        if len(labels) != 1:
            rejected["conflicting_duplicate_images"] += len(copies)
            continue
        rejected["redundant_identical_images"] += len(copies) - 1
        name, level, label = min(copies)
        rows.append((name, level, label, "ceiling" if level == 4 else "exact", digest))

    rows.sort()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("zip_member", "level", "visibility_m", "label_kind", "sha256"))
        writer.writerows(rows)

    with source.open("rb") as handle:
        source_sha256 = hashlib.file_digest(handle, "sha256").hexdigest()
    summary = {
        "source_sha256": source_sha256,
        "retained": len(rows),
        "exact": sum(row[3] == "exact" for row in rows),
        "ceiling": sum(row[3] == "ceiling" for row in rows),
        "rejected": dict(sorted(rejected.items())),
        "policy": "Dataset audit complete; 500 m ceiling kept separate from exact-label regression.",
    }
    destination.with_suffix(".json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_path", type=Path, help="Inner 'fog open data.zip' file")
    parser.add_argument(
        "--manifest", type=Path,
        default=ROOT / "data/processed/fvei/manifest.csv",
    )
    args = parser.parse_args()
    print(json.dumps(audit(args.zip_path, args.manifest), indent=2))
