"""
evaluate_fvei.py

One-shot locked-test evaluation for a run produced by
src.training.finetune_fvei.

The run is evaluated with exactly the same metric code as the final
VGG16 model (src.evaluation.evaluate_vgg16_fvei_final), so all FVEI
numbers are directly comparable:

- exact-label test split (levels 0-3): MAE, RMSE, R2, bias, per level
- 500 m ceiling group analysed separately, never as exact targets

Single-shot protection
----------------------
The locked test split must not drive any further decision. Once a
run has been evaluated, its evaluation.json exists and the script
refuses to evaluate the same run again unless --force is given.

Usage
-----
python -m src.evaluation.evaluate_fvei \
    --run-name resnet50_fvei_synthetic_lastblock_s42 \
    --zip-path <FVEI.zip>

Outputs
-------
results/fvei/runs/<run_name>/test_predictions.csv
results/fvei/runs/<run_name>/ceiling_predictions.csv
results/fvei/runs/<run_name>/evaluation.json

Then refresh the statistics:
python -m src.evaluation.statistical_analysis

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import torch

from src.evaluation.evaluate_vgg16_fvei_final import (
    analyse_ceiling,
    build_loader,
    level_metrics,
    predict,
    regression_metrics,
    save_ceiling_predictions,
    save_exact_predictions,
)
from src.models.regression_models import DISPLAY_NAMES, build_regression_model
from src.training.config import BATCH_SIZE, DEVICE
from src.training.finetune_fvei import CHECKPOINT_DIR, RUNS_DIR, relative_path
from src.training.fvei_dataloader import DEFAULT_MANIFEST


def load_run_model(checkpoint_path: Path) -> tuple[torch.nn.Module, dict]:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location="cpu")

    if checkpoint.get("test_used_for_selection", True):
        raise RuntimeError(
            "Checkpoint metadata does not confirm that the test split was "
            "excluded from model selection."
        )

    model = build_regression_model(checkpoint["arch"], pretrained=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(DEVICE)
    model.eval()

    return model, checkpoint


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--zip-path", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-evaluate a run that already has an evaluation.json.",
    )
    args = parser.parse_args()

    run_dir = RUNS_DIR / args.run_name
    checkpoint_path = CHECKPOINT_DIR / f"{args.run_name}_best.pth"
    summary_path = run_dir / "evaluation.json"

    if summary_path.exists() and not args.force:
        raise FileExistsError(
            f"Run '{args.run_name}' has already been evaluated on the locked "
            "test split. Re-evaluation is blocked to keep the test single-shot."
        )

    model, checkpoint = load_run_model(checkpoint_path)
    arch = checkpoint["arch"]

    print("=" * 64)
    print(f"Locked FVEI test evaluation : {args.run_name}")
    print("=" * 64)
    print(f"Architecture   : {DISPLAY_NAMES[arch]}")
    print(f"Initialisation : {checkpoint.get('init')}")
    print(f"Selected epoch : {checkpoint.get('epoch')}")
    print(f"Validation MAE : {checkpoint.get('validation_mae'):.4f} m")

    test_dataset, test_loader = build_loader(
        args.zip_path, args.manifest, "test", args.batch_size
    )
    targets, predictions = predict(model, test_loader)

    overall = regression_metrics(targets, predictions)
    by_level = level_metrics(test_dataset, targets, predictions)

    run_dir.mkdir(parents=True, exist_ok=True)
    save_exact_predictions(
        test_dataset, targets, predictions, run_dir / "test_predictions.csv"
    )

    ceiling_dataset, ceiling_loader = build_loader(
        args.zip_path, args.manifest, "ceiling_eval", args.batch_size
    )
    _, ceiling_predictions = predict(model, ceiling_loader)
    ceiling = analyse_ceiling(ceiling_dataset, ceiling_predictions)
    save_ceiling_predictions(
        ceiling_dataset, ceiling_predictions, run_dir / "ceiling_predictions.csv"
    )

    summary = {
        "run_name": args.run_name,
        "dataset": "FVEI",
        "arch": arch,
        "init": checkpoint.get("init"),
        "checkpoint": relative_path(checkpoint_path),
        "selected_epoch": checkpoint.get("epoch"),
        "selection_validation_mae_m": checkpoint.get("validation_mae"),
        "evaluated_at": datetime.now().isoformat(timespec="seconds"),
        "held_out_test": {
            "used_for_model_selection": False,
            "metrics": overall,
            "level_metrics": by_level,
        },
        "ceiling_eval": ceiling,
        "notes": [
            "Exact-label test metrics use only FVEI levels 0-3.",
            "Level-4 500 m samples are analysed separately as ceiling labels.",
            "Same metric code as evaluate_vgg16_fvei_final.py.",
        ],
    }

    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print("\n=== LOCKED EXACT-LABEL TEST RESULTS ===")
    print(f"N    : {overall['n']}")
    print(f"MAE  : {overall['mae_m']:.4f} m")
    print(f"RMSE : {overall['rmse_m']:.4f} m")
    print(f"R2   : {overall['r2']:.6f}")
    print(f"Bias : {overall['bias_m']:.4f} m")

    for level, metrics in by_level.items():
        print(
            f"Level {level} | N={metrics['n']} | MAE={metrics['mae_m']:.4f} m "
            f"| RMSE={metrics['rmse_m']:.4f} m | Bias={metrics['bias_m']:.4f} m"
        )

    print(
        f"\n500 m group: {ceiling['predictions_at_or_above_500']}/{ceiling['n']} "
        f"predictions >= 500 m"
    )
    print(f"\nSaved to {relative_path(run_dir)}")
    print("Refresh statistics: python -m src.evaluation.statistical_analysis")


if __name__ == "__main__":
    main()
