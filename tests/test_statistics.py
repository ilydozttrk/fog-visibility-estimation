"""Unit tests for the statistical helper functions (no torch needed)."""

import numpy as np
import pytest

from src.evaluation.statistical_analysis import (
    cluster_bootstrap_mean,
    holm_correction,
    mae,
    paired_wilcoxon,
    r2,
    rmse,
    stratified_bootstrap,
)


def test_holm_correction_matches_manual_calculation():
    # Sorted p: 0.01 (x3), 0.03 (x2), 0.04 (x1) -> 0.03, 0.06, 0.06
    adjusted = holm_correction([0.04, 0.01, 0.03])
    assert adjusted == pytest.approx([0.06, 0.03, 0.06])


def test_holm_correction_is_capped_at_one():
    assert holm_correction([0.6, 0.9]) == pytest.approx([1.0, 1.0])


def test_cluster_bootstrap_interval_contains_estimate():
    rng = np.random.default_rng(0)
    clusters = np.repeat(np.arange(10), 8)
    values = rng.normal(50.0, 5.0, size=80)

    interval = cluster_bootstrap_mean(values, clusters, n_bootstrap=2000)

    assert interval.estimate == pytest.approx(values.mean())
    assert interval.lower < interval.estimate < interval.upper


def test_cluster_bootstrap_has_zero_width_for_constant_values():
    clusters = np.repeat(np.arange(5), 4)
    interval = cluster_bootstrap_mean(np.full(20, 3.0), clusters, n_bootstrap=200)

    assert interval.lower == pytest.approx(3.0)
    assert interval.upper == pytest.approx(3.0)


def test_cluster_bootstrap_requires_two_clusters():
    with pytest.raises(ValueError):
        cluster_bootstrap_mean(np.ones(4), np.zeros(4))


def test_stratified_bootstrap_preserves_statistic():
    target = np.array([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
    prediction = target + np.array([1.0, -1.0, 2.0, -2.0, 3.0, -3.0])
    strata = np.array([0, 0, 1, 1, 2, 2])

    interval = stratified_bootstrap(
        mae, (target, prediction), strata, n_bootstrap=500
    )

    assert interval.estimate == pytest.approx(2.0)
    assert 1.0 <= interval.lower <= interval.upper <= 3.0


def test_paired_wilcoxon_identical_samples():
    a = np.arange(10, dtype=float)
    assert paired_wilcoxon(a, a.copy())["p_value"] == 1.0


def test_paired_wilcoxon_detects_consistent_shift():
    a = np.linspace(10, 30, 15)
    b = a + np.linspace(5, 9, 15)
    assert paired_wilcoxon(a, b)["p_value"] < 0.001


def test_regression_metrics():
    target = np.array([1.0, 2.0, 3.0])
    prediction = np.array([1.0, 2.0, 5.0])

    assert mae(target, prediction) == pytest.approx(2.0 / 3.0)
    assert rmse(target, prediction) == pytest.approx(np.sqrt(4.0 / 3.0))
    assert r2(target, prediction) == pytest.approx(1.0 - 4.0 / 2.0)


def test_separate_output_directory_preserves_published_fvei_results(tmp_path, monkeypatch):
    from src.evaluation import statistical_analysis as analysis

    published = tmp_path / "published"
    published.mkdir()
    existing = {
        published / "statistical_analysis.json": '{"fvei": "recorded results"}\n',
        published / "statistical_analysis.md": "Published FVEI report\n",
        published / "statistical_mae_differences.png": "Published plot sentinel\n",
    }
    for path, content in existing.items():
        path.write_text(content, encoding="utf-8")

    monkeypatch.setattr(analysis, "STATISTICS_DIR", published)
    monkeypatch.setattr(analysis, "REPORT_PATH", published / "statistical_analysis.md")
    monkeypatch.setattr(analysis, "FIGURE_PATH", published / "statistical_mae_differences.png")
    monkeypatch.setattr(analysis, "load_synthetic_predictions", lambda: None)
    monkeypatch.setattr(analysis, "load_fvei_predictions", lambda: {})
    monkeypatch.setattr(analysis, "load_multiseed_summaries", lambda: {})
    output = tmp_path / "ci"
    monkeypatch.setattr("sys.argv", ["statistics", "--no-figure", "--output-dir", str(output)])

    analysis.main()

    assert (output / "statistical_analysis.json").read_text(encoding="utf-8").strip() == "{}"
    assert (output / "statistical_analysis.md").exists()
    assert not (output / "statistical_mae_differences.png").exists()
    for path, content in existing.items():
        assert path.read_text(encoding="utf-8") == content
