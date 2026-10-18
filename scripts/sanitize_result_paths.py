"""
sanitize_result_paths.py

Older scripts stored absolute Windows paths such as
C:\\projects\\fog-visibility-estimation\\results\\checkpoints\\x.pth
inside result files. Before results are committed to Git these are
rewritten to repository-relative POSIX paths
(results/checkpoints/x.pth), so that no local directory layout is
published and the files read the same on every machine.

Only .json, .md and .csv files under results/ (or the folders given
on the command line) are touched. Run with --check first to see what
would change.

Usage
-----
python scripts/sanitize_result_paths.py --check
python scripts/sanitize_result_paths.py

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SUFFIXES = {".json", ".md", ".csv"}

# Any absolute path (Windows drive or POSIX) that runs through a folder
# whose name starts with "fog-visibility-estimation" (covers renamed
# copies such as "fog-visibility-estimation - Kopya").
ABSOLUTE_PROJECT_PATH = re.compile(
    r"(?:[A-Za-z]:)?[\\/](?:[^\\/\"'\n|,`]+[\\/])*?"
    r"fog-visibility-estimation[^\\/\"'\n|,`]*[\\/]"
    r"(?P<rest>[^\"'\n|,`]*)"
)


def _relative(match: re.Match) -> str:
    return match.group("rest").replace("\\", "/")


def sanitize_text(text: str) -> str:
    return ABSOLUTE_PROJECT_PATH.sub(_relative, text)


def _sanitize_json_value(value):
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, list):
        return [_sanitize_json_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _sanitize_json_value(v) for k, v in value.items()}
    return value


def sanitize_file(path: Path) -> tuple[str, str]:
    original = path.read_text(encoding="utf-8-sig")

    if path.suffix == ".json":
        data = json.loads(original)
        cleaned = json.dumps(_sanitize_json_value(data), indent=2, ensure_ascii=False)
        cleaned += "\n"
        # Keep the file untouched if nothing but formatting would change.
        if json.loads(cleaned) == data:
            return original, original
        return original, cleaned

    return original, sanitize_text(original)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "folders", nargs="*", type=Path, default=[PROJECT_ROOT / "results"]
    )
    parser.add_argument(
        "--check", action="store_true", help="Only list files that would change."
    )
    args = parser.parse_args()

    changed = 0

    for folder in args.folders:
        for path in sorted(folder.rglob("*")):
            if path.suffix not in SUFFIXES or not path.is_file():
                continue

            original, cleaned = sanitize_file(path)

            if cleaned == original:
                continue

            changed += 1
            print(("would update: " if args.check else "updated: ") + str(path))

            if not args.check:
                path.write_text(cleaned, encoding="utf-8")

    print(f"{changed} file(s) {'need changes' if args.check else 'updated'}.")


if __name__ == "__main__":
    main()
