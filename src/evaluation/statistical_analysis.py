"""
statistical_analysis.py

Statistical comparison of the saved model predictions.

The research proposal states the hypothesis in terms of a
*statistically significant* MAE difference between ResNet50 and
VGG16. This script tests that claim, and the related attention
and FVEI comparisons, using only prediction files that are
already produced by the evaluation scripts. No model is retrained
and no test split is used for any selection decision.

Methods
-------
Synthetic FRIDA/FRIDA2 test set (112 images, 14 scenes):
    The 8 fog variants of one scene are not independent samples,
    so the scene is the unit of analysis.
    - Per-model MAE with a scene-level cluster bootstrap 95% CI.
    - Paired comparison against the VGG16 baseline:
        * Wilcoxon signed-rank test on per-scene MAE (primary),
        * paired cluster-bootstrap CI of the MAE difference,
        * image-level Wilcoxon test (reported as supplementary).
    - Holm correction over the family of baseline comparisons.

FVEI locked test set (482 images, exact labels):
    Reliable scene/camera identifiers are not available, so an
    image-level, level-stratified bootstrap is used. This is
    reported as a limitation: residual dependence between images
    can make the intervals somewhat too narrow.
    - MAE / RMSE / R2 with 95% bootstrap CI.
    - Optional paired comparison with other FVEI runs found under
      results/fvei/runs/<run_name>/test_predictions.csv.

Multi-seed runs (optional):
    If results/multiseed/<arch>_e<epochs>/seed_<n>/summary.json
    files exist, the per-seed test MAE values are aggregated as
    mean, standard deviation and range.

Outputs
-------
results/statistics/statistical_analysis.json
docs/reports/statistical_analysis.md
figures/statistical_mae_differences.png

Usage
-----
python -m src.evaluation.statistical_analysis

Author: Ilayda Ozturk
Project: TUBITAK 2209-A
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = PROJECT_ROOT / "results"
EVALUATION_DIR = RESULTS_DIR / "evaluation"
FVEI_DIR = RESULTS_DIR / "fvei"
FVEI_RUNS_DIR = FVEI_DIR / "runs"
MULTISEED_DIR = RESULTS_DIR / "multiseed"
STATISTICS_DIR = RESULTS_DIR / "statistics"

REPORT_PATH = (
    PROJECT_ROOT / "docs" / "reports" / "statistical_analysis.md"
)
FIGURE_PATH = (
    PROJECT_ROOT / "figures" / "statistical_mae_differences.png"
)

N_BOOTSTRAP = 10_000
BOOTSTRAP_SEED = 42
ALPHA = 0.05

REFERENCE_SYNTHETIC_MODEL = "VGG16 Baseline"

# Name -> prediction file. The first file defines the reference
# order and the scene keys; files without scene columns are
# aligned by row order and verified against the ground truth.
SYNTHETIC_PREDICTION_FILES = {
    "VGG16 Baseline": "vgg16_test_predictions.csv",
    "ResNet50 Baseline": "resnet50_test_predictions.csv",
    "VGG16 + CBAM": "vgg16_attention_test_predictions.csv",
    "VGG16 + SE": "vgg16_se_test_predictions.csv",
}

REFERENCE_FVEI_RUN = "VGG16 FVEI Block5 (final)"
REFERENCE_FVEI_FILE = FVEI_DIR / "vgg16_fvei_final_test_predictions.csv"


# =============================================================================
# Statistical helpers (pure functions, unit tested)
# =============================================================================

@dataclass
class Interval:
    estimate: float
    lower: float
    upper: float

    def as_dict(self) -> dict:
        return {
            "estimate": self.estimate,
            "ci95_lower": self.lower,
            "ci95_upper": self.upper,
        }


def _percentile_interval(
    estimate: float,
    samples: np.ndarray,
) -> Interval:
    lower, upper = np.percentile(samples, [2.5, 97.5])
    return Interval(float(estimate), float(lower), float(upper))


def cluster_bootstrap_mean(
    values: np.ndarray,
    clusters: np.ndarray,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = BOOTSTRAP_SEED,
) -> Interval:
    """
    Bootstrap CI of a mean when observations are grouped in clusters.

    Whole clusters are resampled with replacement, which keeps the
    within-cluster dependence intact.
    """

    values = np.asarray(values, dtype=float)
    clusters = np.asarray(clusters)

    if values.shape != clusters.shape:
        raise ValueError("values and clusters must have the same shape.")

    unique_clusters, inverse = np.unique(clusters, return_inverse=True)
    n_clusters = len(unique_clusters)

    if n_clusters < 2:
        raise ValueError("At least two clusters are required.")

    cluster_sums = np.bincount(inverse, weights=values)
    cluster_counts = np.bincount(inverse).astype(float)

    rng = np.random.default_rng(seed)
    draws = rng.integers(0, n_clusters, size=(n_bootstrap, n_clusters))

    boot = cluster_sums[draws].sum(axis=1) / cluster_counts[draws].sum(axis=1)

    return _percentile_interval(values.mean(), boot)


def stratified_bootstrap(
    statistic,
    arrays: tuple[np.ndarray, ...],
    strata: np.ndarray,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = BOOTSTRAP_SEED,
) -> Interval:
    """
    Image-level bootstrap that resamples within each stratum, so the
    level distribution of every bootstrap sample equals the original.

    `statistic` receives the resampled arrays and returns a float.
    """

    strata = np.asarray(strata)
    arrays = tuple(np.asarray(a, dtype=float) for a in arrays)

    groups = [np.flatnonzero(strata == s) for s in np.unique(strata)]

    rng = np.random.default_rng(seed)
    boot = np.empty(n_bootstrap)

    for b in range(n_bootstrap):
        index = np.concatenate(
            [rng.choice(g, size=len(g), replace=True) for g in groups]
        )
        boot[b] = statistic(*(a[index] for a in arrays))

    return _percentile_interval(statistic(*arrays), boot)


def paired_wilcoxon(
    a: np.ndarray,
    b: np.ndarray,
) -> dict:
    """
    Two-sided Wilcoxon signed-rank test on paired samples.
    """

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if a.shape != b.shape:
        raise ValueError("Paired samples must have the same shape.")

    differences = b - a

    if np.allclose(differences, 0.0):
        return {"statistic": 0.0, "p_value": 1.0, "n": int(len(a))}

    result = wilcoxon(a, b, zero_method="wilcox", alternative="two-sided")

    return {
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "n": int(len(a)),
    }


def holm_correction(p_values: list[float]) -> list[float]:
    """
    Holm-Bonferroni adjusted p-values (monotone, capped at 1).
    """

    p = np.asarray(p_values, dtype=float)
    m = len(p)

    if m == 0:
        return []

    order = np.argsort(p)
    adjusted = np.empty(m)
    running_max = 0.0

    for rank, index in enumerate(order):
        value = min(1.0, (m - rank) * p[index])
        running_max = max(running_max, value)
        adjusted[index] = running_max

    return adjusted.tolist()


def mae(target: np.ndarray, prediction: np.ndarray) -> float:
    return float(np.mean(np.abs(prediction - target)))


def rmse(target: np.ndarray, prediction: np.ndarray) -> float:
    return float(np.sqrt(np.mean((prediction - target) ** 2)))


def r2(target: np.ndarray, prediction: np.ndarray) -> float:
    ss_res = np.sum((target - prediction) ** 2)
    ss_tot = np.sum((target - target.mean()) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan")


# =============================================================================
# Loading
# =============================================================================

def load_synthetic_predictions() -> pd.DataFrame | None:
    """
    Return one row per test image with columns:
    scene_key, target, and one absolute-error column per model.
    """

    reference_name = REFERENCE_SYNTHETIC_MODEL
    reference_path = (
        EVALUATION_DIR / SYNTHETIC_PREDICTION_FILES[reference_name]
    )

    if not reference_path.exists():
        print(f"[skip] Synthetic reference not found: {reference_path}")
        return None

    reference = pd.read_csv(reference_path)

    table = pd.DataFrame(
        {
            "filename": reference["filename"],
            "scene_key": (
                reference["source_dataset"].astype(str)
                + "_"
                + reference["scene_id"].astype(str)
            ),
            "target": reference["ground_truth_m"].astype(float),
        }
    )

    for name, file_name in SYNTHETIC_PREDICTION_FILES.items():
        path = EVALUATION_DIR / file_name

        if not path.exists():
            print(f"[skip] {name}: {path} not found")
            continue

        frame = pd.read_csv(path)

        if "filename" in frame.columns:
            frame = frame.set_index("filename").loc[table["filename"]]
            target = frame["ground_truth_m"].to_numpy(float)
            prediction = frame["prediction_m"].to_numpy(float)
        else:
            # Older evaluation scripts saved predictions without file
            # names, in the deterministic (shuffle=False) test order.
            if len(frame) != len(table):
                raise ValueError(f"{name}: unexpected row count.")
            target = frame["actual_visibility_m"].to_numpy(float)
            prediction = frame["predicted_visibility_m"].to_numpy(float)

        if not np.allclose(target, table["target"].to_numpy()):
            raise ValueError(
                f"{name}: ground-truth order does not match the "
                "reference prediction file; rows cannot be paired."
            )

        table[name] = np.abs(prediction - target)

    return table


def load_fvei_predictions() -> dict[str, pd.DataFrame]:
    """
    Return FVEI exact-label test predictions keyed by run name.
    Every frame has columns: zip_member, level, target, prediction.
    """

    runs: dict[str, pd.DataFrame] = {}

    def _read(path: Path) -> pd.DataFrame:
        frame = pd.read_csv(path)
        return pd.DataFrame(
            {
                "zip_member": frame["zip_member"],
                "level": frame["level"].astype(int),
                "target": frame["target_visibility_m"].astype(float),
                "prediction": frame["prediction_m"].astype(float),
            }
        )

    if REFERENCE_FVEI_FILE.exists():
        runs[REFERENCE_FVEI_RUN] = _read(REFERENCE_FVEI_FILE)
    else:
        print(f"[skip] FVEI reference not found: {REFERENCE_FVEI_FILE}")

    if FVEI_RUNS_DIR.exists():
        for path in sorted(FVEI_RUNS_DIR.glob("*/test_predictions.csv")):
            runs[path.parent.name] = _read(path)

    return runs


def load_multiseed_summaries() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}

    if not MULTISEED_DIR.exists():
        return groups

    for path in sorted(MULTISEED_DIR.glob("*/seed_*/summary.json")):
        group = path.parent.parent.name

        if group.startswith("_"):
            continue

        summary = json.loads(path.read_text(encoding="utf-8"))

        if summary.get("dry_run"):
            continue

        predictions = path.parent / "test_predictions.csv"
        summary["_predictions_path"] = str(predictions) if predictions.exists() else None

        groups.setdefault(group, []).append(summary)

    return groups


# =============================================================================
# Analyses
# =============================================================================

def analyse_synthetic(table: pd.DataFrame) -> dict:
    models = [
        name for name in SYNTHETIC_PREDICTION_FILES if name in table.columns
    ]
    clusters = table["scene_key"].to_numpy()

    per_model = {}

    for name in models:
        interval = cluster_bootstrap_mean(table[name].to_numpy(), clusters)
        per_model[name] = interval.as_dict()

    scene_mae = table.groupby("scene_key")[models].mean()

    comparisons = []
    reference = REFERENCE_SYNTHETIC_MODEL

    for name in models:
        if name == reference:
            continue

        difference = table[name].to_numpy() - table[reference].to_numpy()
        diff_interval = cluster_bootstrap_mean(difference, clusters)

        scene_test = paired_wilcoxon(
            scene_mae[reference].to_numpy(),
            scene_mae[name].to_numpy(),
        )
        image_test = paired_wilcoxon(
            table[reference].to_numpy(),
            table[name].to_numpy(),
        )

        reference_better = int((scene_mae[name] > scene_mae[reference]).sum())

        comparisons.append(
            {
                "reference": reference,
                "model": name,
                "mae_difference_m": diff_interval.as_dict(),
                "difference_definition": f"MAE({name}) - MAE({reference})",
                "n_images": int(len(table)),
                "n_scenes": int(len(scene_mae)),
                "scenes_where_reference_is_better": reference_better,
                "scene_level_wilcoxon": scene_test,
                "image_level_wilcoxon": image_test,
            }
        )

    adjusted = holm_correction(
        [c["scene_level_wilcoxon"]["p_value"] for c in comparisons]
    )

    for comparison, p_adjusted in zip(comparisons, adjusted):
        comparison["scene_level_wilcoxon"]["p_value_holm"] = p_adjusted
        comparison["significant_at_0_05_holm"] = bool(p_adjusted < ALPHA)

    return {
        "unit_of_analysis": "scene (source_dataset + scene_id)",
        "n_images": int(len(table)),
        "n_scenes": int(table["scene_key"].nunique()),
        "bootstrap": {
            "type": "scene-level cluster bootstrap",
            "n_resamples": N_BOOTSTRAP,
            "seed": BOOTSTRAP_SEED,
        },
        "per_model_test_mae_m": per_model,
        "comparisons_vs_reference": comparisons,
        "multiple_comparison_correction": "Holm-Bonferroni",
    }


def analyse_fvei(runs: dict[str, pd.DataFrame]) -> dict:
    per_run = {}

    for name, frame in runs.items():
        target = frame["target"].to_numpy()
        prediction = frame["prediction"].to_numpy()
        level = frame["level"].to_numpy()

        per_run[name] = {
            "n": int(len(frame)),
            "mae_m": stratified_bootstrap(
                mae, (target, prediction), level
            ).as_dict(),
            "rmse_m": stratified_bootstrap(
                rmse, (target, prediction), level
            ).as_dict(),
            "r2": stratified_bootstrap(
                r2, (target, prediction), level
            ).as_dict(),
        }

    comparisons = []

    if REFERENCE_FVEI_RUN in runs:
        reference = runs[REFERENCE_FVEI_RUN].set_index("zip_member")

        for name, frame in runs.items():
            if name == REFERENCE_FVEI_RUN:
                continue

            other = frame.set_index("zip_member")

            if set(other.index) != set(reference.index):
                raise ValueError(
                    f"FVEI run '{name}' was not evaluated on the same "
                    "locked test images as the reference run."
                )

            other = other.loc[reference.index]
            reference_error = np.abs(
                reference["prediction"] - reference["target"]
            ).to_numpy()
            other_error = np.abs(other["prediction"] - other["target"]).to_numpy()
            level = reference["level"].to_numpy()

            difference = stratified_bootstrap(
                lambda a, b: float(np.mean(b - a)),
                (reference_error, other_error),
                level,
            )

            comparisons.append(
                {
                    "reference": REFERENCE_FVEI_RUN,
                    "model": name,
                    "mae_difference_m": difference.as_dict(),
                    "difference_definition": (
                        f"MAE({name}) - MAE({REFERENCE_FVEI_RUN})"
                    ),
                    "image_level_wilcoxon": paired_wilcoxon(
                        reference_error, other_error
                    ),
                }
            )

        adjusted = holm_correction(
            [c["image_level_wilcoxon"]["p_value"] for c in comparisons]
        )

        for comparison, p_adjusted in zip(comparisons, adjusted):
            comparison["image_level_wilcoxon"]["p_value_holm"] = p_adjusted
            comparison["significant_at_0_05_holm"] = bool(p_adjusted < ALPHA)

    return {
        "unit_of_analysis": "image (scene/camera identifiers unavailable)",
        "bootstrap": {
            "type": "image-level bootstrap stratified by visibility level",
            "n_resamples": N_BOOTSTRAP,
            "seed": BOOTSTRAP_SEED,
        },
        "per_run": per_run,
        "comparisons_vs_reference": comparisons,
        "limitation": (
            "Images may share cameras or scenes; image-level intervals "
            "can therefore be narrower than the true uncertainty."
        ),
    }


def seed_averaged_errors(
    summaries: list[dict],
    seeds: list[int],
) -> pd.DataFrame | None:
    """
    Per-image absolute error averaged over the given training seeds.

    Returns a frame indexed by filename with columns scene_key and
    error, or None when a seed has no saved prediction file.
    """

    by_seed = {s["training_seed"]: s.get("_predictions_path") for s in summaries}
    frames = []

    for seed in seeds:
        path = by_seed.get(seed)
        if not path:
            return None
        frame = pd.read_csv(path).set_index("filename").sort_index()
        frames.append(frame)

    reference = frames[0]
    for frame in frames[1:]:
        if not frame.index.equals(reference.index):
            raise ValueError("Multi-seed runs were not evaluated on the same test images.")

    errors = np.mean([f["absolute_error_m"].to_numpy(float) for f in frames], axis=0)

    return pd.DataFrame(
        {
            "scene_key": (
                reference["source_dataset"].astype(str)
                + "_"
                + reference["scene_id"].astype(str)
            ).to_numpy(),
            "error": errors,
        },
        index=reference.index,
    )


def protocol_decision(
    seed_differences: list[float],
    ci_lower: float,
    ci_upper: float,
    p_holm: float,
    all_converged: bool,
) -> str:
    """
    Pre-registered decision rule (docs/MODEL_SELECTION_PROTOCOL.md).

    Differences are MAE(ResNet50) - MAE(VGG16): positive favours VGG16.
    """

    differences = np.asarray(seed_differences, dtype=float)
    five_seeds = differences.size == 5 and bool(np.all(np.isfinite(differences)))
    vgg_all = five_seeds and bool(np.all(differences > 0))
    resnet_all = five_seeds and bool(np.all(differences < 0))
    excludes_zero = ci_lower > 0 or ci_upper < 0

    if vgg_all and ci_lower > 0 and p_holm < ALPHA:
        verdict = "VGG16 anlamlı düzeyde daha iyi"
    elif resnet_all and ci_upper < 0 and p_holm < ALPHA:
        verdict = "ResNet50 anlamlı düzeyde daha iyi"
    elif excludes_zero or p_holm < ALPHA:
        verdict = "Kısmi kanıt (tüm ölçütler sağlanmadı); anlamlı fark iddia edilmez"
    else:
        verdict = "Anlamlı fark yok"

    if not all_converged:
        verdict += " (uyarı: tüm seed'ler bütçe içinde yakınsamadı)"

    return verdict


def analyse_multiseed(groups: dict[str, list[dict]]) -> dict:
    output = {}

    for group, summaries in groups.items():
        values = np.array([s["test_mae_m"] for s in summaries], dtype=float)
        seeds = [s["training_seed"] for s in summaries]
        epochs = [s["best_epoch"] for s in summaries]
        converged = [
            s.get("converged_within_budget", s["best_epoch"] < s["epochs"])
            for s in summaries
        ]

        output[group] = {
            "n_seeds": int(len(values)),
            "seeds": seeds,
            "test_mae_m_per_seed": values.tolist(),
            "best_epoch_per_seed": epochs,
            "stopped_epoch_per_seed": [
                s.get("stopped_epoch", s["epochs"]) for s in summaries
            ],
            "seeds_converged_within_budget": int(sum(converged)),
            "test_mae_mean_m": float(values.mean()),
            "test_mae_std_m": (
                float(values.std(ddof=1)) if len(values) > 1 else 0.0
            ),
            "test_mae_min_m": float(values.min()),
            "test_mae_max_m": float(values.max()),
        }

    comparisons = []

    vgg_groups = [g for g in groups if g.startswith("vgg16_")]
    resnet_groups = [g for g in groups if g.startswith("resnet50_")]

    def _patience_suffix(group: str) -> str:
        return group.rsplit("_p", 1)[1] if "_p" in group else ""

    for vgg_group in vgg_groups:
        for resnet_group in resnet_groups:
            # Compare early-stopping groups only with the same patience,
            # and fixed-budget groups only with fixed-budget groups.
            if _patience_suffix(vgg_group) != _patience_suffix(resnet_group):
                continue

            vgg = {s["training_seed"]: s["test_mae_m"] for s in groups[vgg_group]}
            resnet = {
                s["training_seed"]: s["test_mae_m"] for s in groups[resnet_group]
            }
            seeds = sorted(set(vgg) & set(resnet))

            if not seeds:
                continue

            differences = np.array([resnet[s] - vgg[s] for s in seeds])

            pooled = None
            vgg_errors = seed_averaged_errors(groups[vgg_group], seeds)
            resnet_errors = seed_averaged_errors(groups[resnet_group], seeds)

            if vgg_errors is not None and resnet_errors is not None:
                resnet_errors = resnet_errors.loc[vgg_errors.index]
                clusters = vgg_errors["scene_key"].to_numpy()
                image_difference = (
                    resnet_errors["error"].to_numpy() - vgg_errors["error"].to_numpy()
                )
                scene = pd.DataFrame(
                    {
                        "scene_key": clusters,
                        "vgg": vgg_errors["error"].to_numpy(),
                        "resnet": resnet_errors["error"].to_numpy(),
                    }
                ).groupby("scene_key").mean()

                pooled = {
                    "description": (
                        "per-image errors averaged over paired seeds; "
                        "scene is the unit of analysis"
                    ),
                    "n_scenes": int(len(scene)),
                    "mae_difference_m": cluster_bootstrap_mean(
                        image_difference, clusters
                    ).as_dict(),
                    "scenes_where_vgg16_is_better": int(
                        (scene["resnet"] > scene["vgg"]).sum()
                    ),
                    "scene_level_wilcoxon": paired_wilcoxon(
                        scene["vgg"].to_numpy(), scene["resnet"].to_numpy()
                    ),
                }

            converged = all(
                s.get("converged_within_budget", s["best_epoch"] < s["epochs"])
                for s in groups[vgg_group] + groups[resnet_group]
                if s["training_seed"] in seeds
            )

            comparisons.append(
                {
                    "all_seeds_converged_within_budget": converged,
                    "pooled_scene_level": pooled,
                    "reference": vgg_group,
                    "model": resnet_group,
                    "paired_seeds": seeds,
                    "difference_definition": (
                        f"test MAE({resnet_group}) - test MAE({vgg_group}), "
                        "per training seed"
                    ),
                    "mae_difference_per_seed_m": differences.tolist(),
                    "mae_difference_mean_m": float(differences.mean()),
                    "seeds_where_vgg16_is_better": int((differences > 0).sum()),
                }
            )

    tested = [c for c in comparisons if c["pooled_scene_level"] is not None]
    adjusted = holm_correction(
        [c["pooled_scene_level"]["scene_level_wilcoxon"]["p_value"] for c in tested]
    )

    for comparison, p_adjusted in zip(tested, adjusted):
        pooled = comparison["pooled_scene_level"]
        pooled["scene_level_wilcoxon"]["p_value_holm"] = p_adjusted
        comparison["protocol_decision"] = protocol_decision(
            comparison["mae_difference_per_seed_m"],
            pooled["mae_difference_m"]["ci95_lower"],
            pooled["mae_difference_m"]["ci95_upper"],
            p_adjusted,
            comparison["all_seeds_converged_within_budget"],
        )

    return {"groups": output, "paired_by_seed": comparisons}


# =============================================================================
# Reporting
# =============================================================================

def _fmt_p(p: float) -> str:
    return f"{p:.2e}" if p < 0.001 else f"{p:.4f}"


def _ci(interval: dict, digits: int = 2) -> str:
    return (
        f"{interval['estimate']:.{digits}f} "
        f"[{interval['ci95_lower']:.{digits}f}, "
        f"{interval['ci95_upper']:.{digits}f}]"
    )


def write_markdown(results: dict, path: Path) -> None:
    lines = [
        "# İstatistiksel Analiz",
        "",
        "Bu rapor `src/evaluation/statistical_analysis.py` tarafından "
        "otomatik olarak üretilir; elle düzenlenmemelidir.",
        "",
        "Analiz yalnızca kaydedilmiş tahmin dosyalarını kullanır. Hiçbir "
        "model yeniden eğitilmemiş ve test kümeleri hiçbir seçim kararında "
        "kullanılmamıştır.",
        "",
    ]

    synthetic = results.get("synthetic")

    if synthetic:
        lines += [
            "## 1. Sentetik FRIDA/FRIDA2 Test Kümesi",
            "",
            f"- Test görüntüsü: **{synthetic['n_images']}**, sahne: "
            f"**{synthetic['n_scenes']}**",
            "- Aynı sahnenin 8 sis seviyesi bağımsız olmadığından analiz "
            "birimi **sahne**dir.",
            "- Güven aralıkları sahne düzeyinde küme bootstrap ile "
            f"({synthetic['bootstrap']['n_resamples']} yeniden örnekleme) "
            "hesaplanmıştır.",
            "",
            "### 1.1 Model Bazında Test MAE (95% GA)",
            "",
            "| Model | Test MAE (m) [95% GA] |",
            "|---|---:|",
        ]

        for name, interval in synthetic["per_model_test_mae_m"].items():
            lines.append(f"| {name} | {_ci(interval)} |")

        lines += [
            "",
            f"### 1.2 {REFERENCE_SYNTHETIC_MODEL} ile Eşleştirilmiş "
            "Karşılaştırmalar",
            "",
            "Fark = MAE(model) − MAE(VGG16 Baseline). Pozitif değer VGG16 "
            "Baseline'ın daha düşük hata ürettiğini gösterir.",
            "",
            "| Model | MAE Farkı (m) [95% GA] | VGG16'nın daha iyi olduğu "
            "sahne | Wilcoxon p (sahne) | Holm p | Wilcoxon p (görüntü, ek) "
            "| Anlamlı (α=0.05, Holm) |",
            "|---|---:|---:|---:|---:|---:|:---:|",
        ]

        for c in synthetic["comparisons_vs_reference"]:
            lines.append(
                f"| {c['model']} | {_ci(c['mae_difference_m'])} | "
                f"{c['scenes_where_reference_is_better']}/{c['n_scenes']} | "
                f"{_fmt_p(c['scene_level_wilcoxon']['p_value'])} | "
                f"{_fmt_p(c['scene_level_wilcoxon']['p_value_holm'])} | "
                f"{_fmt_p(c['image_level_wilcoxon']['p_value'])} | "
                f"{'Evet' if c['significant_at_0_05_holm'] else 'Hayır'} |"
            )

        resnet = next(
            (
                c
                for c in synthetic["comparisons_vs_reference"]
                if c["model"].startswith("ResNet50")
            ),
            None,
        )

        lines += ["", "### 1.3 Hipotezin Değerlendirilmesi", ""]

        if resnet is not None:
            diff = resnet["mae_difference_m"]
            direction = (
                "VGG16 lehine" if diff["estimate"] > 0 else "ResNet50 lehine"
            )
            lines += [
                "Öneride ResNet50'nin VGG16'ya göre istatistiksel olarak "
                "anlamlı düzeyde daha düşük MAE üreteceği öngörülmüştü.",
                "",
                f"Gözlenen fark **{direction}**: ResNet50'nin MAE değeri "
                f"VGG16'dan {diff['estimate']:.2f} m (95% GA "
                f"{diff['ci95_lower']:.2f}–{diff['ci95_upper']:.2f} m) "
                "daha yüksektir. Sahne düzeyinde Wilcoxon testi için Holm "
                "düzeltmeli p = "
                f"{_fmt_p(resnet['scene_level_wilcoxon']['p_value_holm'])}.",
                "",
                "Bu sonuç tek bir sahne ayrımı ve tek eğitim tohumu (seed 42) "
                "için geçerlidir. Tohum değişkenliği için bkz. Bölüm 3.",
                "",
            ]

    fvei = results.get("fvei")

    if fvei and fvei["per_run"]:
        lines += [
            "## 2. FVEI Kilitli Test Kümesi",
            "",
            "- Güvenilir sahne/kamera kimliği bulunmadığından bootstrap "
            "görüntü düzeyinde, görüş seviyesine göre tabakalı yapılmıştır.",
            "- Sınırlılık: Görüntüler aynı kamera veya sahneyi paylaşabilir; "
            "bu nedenle görüntü düzeyindeki güven aralıkları gerçek "
            "belirsizlikten bir miktar dar olabilir.",
            "",
            "| Çalıştırma | N | MAE (m) [95% GA] | RMSE (m) [95% GA] | "
            "R² [95% GA] |",
            "|---|---:|---:|---:|---:|",
        ]

        for name, run in fvei["per_run"].items():
            lines.append(
                f"| {name} | {run['n']} | {_ci(run['mae_m'])} | "
                f"{_ci(run['rmse_m'])} | {_ci(run['r2'], 4)} |"
            )

        if fvei["comparisons_vs_reference"]:
            lines += [
                "",
                f"Fark = MAE(çalıştırma) − MAE({REFERENCE_FVEI_RUN}).",
                "",
                "| Çalıştırma | MAE Farkı (m) [95% GA] | Wilcoxon p | Holm p "
                "| Anlamlı |",
                "|---|---:|---:|---:|:---:|",
            ]

            for c in fvei["comparisons_vs_reference"]:
                lines.append(
                    f"| {c['model']} | {_ci(c['mae_difference_m'])} | "
                    f"{_fmt_p(c['image_level_wilcoxon']['p_value'])} | "
                    f"{_fmt_p(c['image_level_wilcoxon']['p_value_holm'])} | "
                    f"{'Evet' if c['significant_at_0_05_holm'] else 'Hayır'} |"
                )

        lines.append("")

    multiseed = results.get("multiseed")

    lines += ["## 3. Çoklu Tohum (Seed) Deneyleri", ""]

    if multiseed:
        lines += [
            "Sahne ayrımı sabit (seed 42) tutulmuş, yalnızca eğitim tohumu "
            "değiştirilmiştir.",
            "",
            "| Deney Grubu | Seed Sayısı | Test MAE Ort. ± SS (m) | Min–Maks "
            "(m) | En İyi Epoch'lar | Bütçe içinde yakınsayan seed |",
            "|---|---:|---:|---:|---|---:|",
        ]

        for group, row in multiseed["groups"].items():
            lines.append(
                f"| {group} | {row['n_seeds']} | "
                f"{row['test_mae_mean_m']:.2f} ± {row['test_mae_std_m']:.2f} | "
                f"{row['test_mae_min_m']:.2f}–{row['test_mae_max_m']:.2f} | "
                f"{', '.join(str(e) for e in row['best_epoch_per_seed'])} | "
                f"{row['seeds_converged_within_budget']}/{row['n_seeds']} |"
            )

        if multiseed["paired_by_seed"]:
            lines += [
                "",
                "Seed bazında eşleştirilmiş karşılaştırma "
                "(fark = ResNet50 − VGG16):",
                "",
                "| VGG16 grubu | ResNet50 grubu | Ortak seed | Ortalama fark "
                "(m) | VGG16'nın daha iyi olduğu seed | Fark [95% GA] (sahne, "
                "seed ortalaması) | VGG16'nın daha iyi olduğu sahne | Holm p "
                "| Protokol kararı |",
                "|---|---|---:|---:|---:|---:|---:|---:|---|",
            ]

            for c in multiseed["paired_by_seed"]:
                pooled = c.get("pooled_scene_level")
                if pooled:
                    extra = (
                        f"{_ci(pooled['mae_difference_m'])} | "
                        f"{pooled['scenes_where_vgg16_is_better']}/"
                        f"{pooled['n_scenes']} | "
                        f"{_fmt_p(pooled['scene_level_wilcoxon']['p_value_holm'])} | "
                        f"{c['protocol_decision']}"
                    )
                else:
                    extra = "– | – | – | tahmin dosyası yok"
                lines.append(
                    f"| {c['reference']} | {c['model']} | "
                    f"{len(c['paired_seeds'])} | "
                    f"{c['mae_difference_mean_m']:.2f} | "
                    f"{c['seeds_where_vgg16_is_better']}/"
                    f"{len(c['paired_seeds'])} | {extra} |"
                )

            lines += [
                "",
                "Gruplar yalnızca aynı durdurma kuralına sahip gruplarla "
                "eşleştirilir (sabit bütçe ↔ sabit bütçe, aynı patience ↔ "
                "aynı patience).",
                "",
                "\"Bütçe içinde yakınsayan seed\": erken durdurmalı koşularda "
                "epoch bütçesine ulaşmadan patience kuralıyla duran seed sayısı. "
                "Eski sabit bütçeli koşularda en iyi validation epoch'unun son "
                "epoch'tan önce olması yalnızca bir yakınsama göstergesi olarak kullanılır.",
                "",
                "Anlamlılık testi: her görüntünün hatası eşleştirilmiş seed'ler "
                "üzerinden ortalanır, ardından 14 test sahnesinde eşleştirilmiş "
                "Wilcoxon testi uygulanır (Holm düzeltmeli); güven aralığı sahne "
                "düzeyinde küme bootstrap ile hesaplanır. Seed düzeyinde doğrudan "
                "test yapılmaz, çünkü 5 seed ile ulaşılabilecek en küçük iki yönlü "
                "p değeri 0.0625'tir.",
                "",
                "Karar kuralı: [`docs/MODEL_SELECTION_PROTOCOL.md`]"
                "(../MODEL_SELECTION_PROTOCOL.md).",
            ]

        lines.append("")
    else:
        lines += [
            "Henüz çoklu tohum sonucu bulunmamaktadır. Çalıştırmak için:",
            "",
            "```bash",
            "python -m src.training.train_synthetic_multiseed --arch vgg16",
            "python -m src.training.train_synthetic_multiseed --arch resnet50",
            "python -m src.training.train_synthetic_multiseed --arch resnet50 "
            "--epochs 50",
            "```",
            "",
        ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def plot_differences(results: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = []

    synthetic = results.get("synthetic") or {}
    for c in synthetic.get("comparisons_vs_reference", []):
        rows.append((f"Sentetik: {c['model']}", c["mae_difference_m"]))

    fvei = results.get("fvei") or {}
    for c in fvei.get("comparisons_vs_reference", []):
        rows.append((f"FVEI: {c['model']}", c["mae_difference_m"]))

    multiseed = results.get("multiseed") or {}
    for c in multiseed.get("paired_by_seed", []):
        if c.get("pooled_scene_level"):
            rows.append(
                (
                    f"Çoklu seed: {c['model']} vs {c['reference']}",
                    c["pooled_scene_level"]["mae_difference_m"],
                )
            )

    if not rows:
        return

    fig, ax = plt.subplots(figsize=(8, 0.7 * len(rows) + 1.6))

    for y, (_, interval) in enumerate(rows):
        ax.errorbar(
            interval["estimate"],
            y,
            xerr=[
                [interval["estimate"] - interval["ci95_lower"]],
                [interval["ci95_upper"] - interval["estimate"]],
            ],
            fmt="o",
            color="#2f5d8a",
            capsize=4,
        )

    ax.axvline(0.0, color="#888888", linewidth=1, linestyle="--")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([label for label, _ in rows])
    ax.invert_yaxis()
    ax.set_xlabel("MAE farkı (m), referans modele göre  [95% GA]")
    ax.set_title("Referans modele göre MAE farkları")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200)
    plt.close(fig)


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-figure", action="store_true")
    parser.add_argument(
        "--output-dir", type=Path,
        help="Write analysis outputs to this directory, preserving the published report.",
    )
    args = parser.parse_args()

    results: dict = {}

    synthetic_table = load_synthetic_predictions()
    if synthetic_table is not None:
        results["synthetic"] = analyse_synthetic(synthetic_table)

    fvei_runs = load_fvei_predictions()
    if fvei_runs:
        results["fvei"] = analyse_fvei(fvei_runs)

    multiseed = load_multiseed_summaries()
    if multiseed:
        results["multiseed"] = analyse_multiseed(multiseed)

    output_dir = args.output_dir.resolve() if args.output_dir is not None else None
    json_path = (output_dir or STATISTICS_DIR) / "statistical_analysis.json"
    report_path = output_dir / "statistical_analysis.md" if output_dir else REPORT_PATH
    figure_path = output_dir / "statistical_mae_differences.png" if output_dir else FIGURE_PATH
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    write_markdown(results, report_path)

    if not args.no_figure:
        plot_differences(results, figure_path)

    outputs = [json_path, report_path] + ([] if args.no_figure else [figure_path])
    for path in outputs:
        display_path = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path
        print(f"Saved: {display_path}")


if __name__ == "__main__":
    main()
