"""Verify stopping metadata without training a backbone or reading real test data."""

from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest
import torch

from src.training import train_synthetic_multiseed as training


@pytest.mark.parametrize(
    "validation,patience,expected_stop,converged",
    [
        ([3.0, 2.0, 1.0], 2, 3, False),
        ([1.0, 2.0, 3.0], 3, 3, False),
        ([1.0, 2.0, 3.0, 4.0], 2, 3, True),
    ],
)
def test_budget_cap_does_not_imply_early_stopping(
    tmp_path, monkeypatch, validation, patience, expected_stop, converged
):
    frame = pd.DataFrame({
        "filename": ["synthetic-test.png"], "scene_id": [1],
        "source_dataset": ["fixture"], "visibility_m": [10.0],
    })
    loader = SimpleNamespace(dataset=SimpleNamespace(data=frame))
    monkeypatch.setattr(training, "DEVICE", torch.device("cpu"))
    monkeypatch.setattr(training, "create_dataloaders", lambda **kwargs: (loader, loader, loader))
    monkeypatch.setattr(training, "DataLoader", lambda *args, **kwargs: loader)
    monkeypatch.setattr(training, "build_regression_model", lambda *args, **kwargs: torch.nn.Linear(1, 1))
    monkeypatch.setattr(training, "freeze_all_but_head", lambda *args: None)
    values = iter(validation)

    def fake_epoch(model, data, loss, optimizer=None, max_batches=None):
        return 0.0 if optimizer is not None else next(values)

    calls = []

    def fake_predict(model, data):
        calls.append(data)
        return np.array([11.0])

    monkeypatch.setattr(training, "run_epoch", fake_epoch)
    monkeypatch.setattr(training, "predict", fake_predict)
    summary = training.train_one_seed(
        "vgg16", 42, 42, len(validation), tmp_path, False, patience=patience
    )

    assert summary["stopped_epoch"] == expected_stop
    assert summary["early_stopped"] is converged
    assert summary["converged_within_budget"] is converged
    assert summary["best_epoch"] == int(np.argmin(validation[:expected_stop])) + 1
    assert len(calls) == 1
