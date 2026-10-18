"""Tests for the shared VGG16 / ResNet50 fine-tuning helpers.

pretrained=False is used everywhere, so no weights are downloaded.
"""

import pytest
import torch
import torch.nn as nn

from src.models.regression_models import (
    build_regression_model,
    configure_last_block_finetuning,
    freeze_all_but_head,
    last_block_parameter_groups,
    set_train_mode,
    verify_last_block_finetuning,
)


@pytest.fixture(scope="module")
def vgg16():
    return build_regression_model("vgg16", pretrained=False)


@pytest.fixture(scope="module")
def resnet50():
    return build_regression_model("resnet50", pretrained=False)


def test_unknown_architecture_is_rejected():
    with pytest.raises(ValueError):
        build_regression_model("alexnet", pretrained=False)


def test_vgg16_last_block_counts_match_final_fvei_model(vgg16):
    configure_last_block_finetuning(vgg16, "vgg16")
    counts = verify_last_block_finetuning(vgg16, "vgg16")

    # Values reported for the final VGG16 FVEI model in README.md.
    assert counts["last_block"] == 7_079_424
    assert counts["head"] == 12_911_361


def test_resnet50_only_layer4_and_head_are_trainable(resnet50):
    configure_last_block_finetuning(resnet50, "resnet50")
    verify_last_block_finetuning(resnet50, "resnet50")

    trainable_prefixes = {
        name.split(".")[0]
        for name, parameter in resnet50.named_parameters()
        if parameter.requires_grad
    }

    assert trainable_prefixes == {"layer4", "fc"}


def test_resnet50_head_matches_original_checkpoint_layout(resnet50):
    head_keys = sorted(k for k in resnet50.state_dict() if k.startswith("fc."))

    assert head_keys == [
        "fc.0.bias",
        "fc.0.weight",
        "fc.3.bias",
        "fc.3.weight",
        "fc.6.bias",
        "fc.6.weight",
    ]


def test_freeze_all_but_head(resnet50):
    freeze_all_but_head(resnet50, "resnet50")

    for name, parameter in resnet50.named_parameters():
        assert parameter.requires_grad == name.startswith("fc.")


def test_parameter_groups_use_two_learning_rates(vgg16):
    configure_last_block_finetuning(vgg16, "vgg16")
    groups = last_block_parameter_groups(vgg16, "vgg16", 1e-5, 1e-4)

    assert [g["lr"] for g in groups] == [1e-5, 1e-4]
    assert all(g["params"] for g in groups)


def test_set_train_mode_keeps_batchnorm_frozen(resnet50):
    set_train_mode(resnet50)

    assert resnet50.training
    assert all(
        not m.training
        for m in resnet50.modules()
        if isinstance(m, nn.BatchNorm2d)
    )
    assert any(m.training for m in resnet50.modules() if isinstance(m, nn.Dropout))


@pytest.mark.parametrize("arch", ["vgg16", "resnet50"])
def test_forward_returns_one_value_per_image(arch):
    model = build_regression_model(arch, pretrained=False).eval()

    with torch.no_grad():
        output = model(torch.zeros(2, 3, 224, 224))

    assert output.shape == (2, 1)


@pytest.mark.parametrize("arch", ["resnet50_cbam", "resnet50_se"])
def test_resnet50_attention_variant_trains_only_attention_and_head(arch):
    model = build_regression_model(arch, pretrained=False)
    freeze_all_but_head(model, arch)

    trainable = {
        name.split(".")[0] + "." + name.split(".")[1]
        if name.startswith("layer4.") else name.split(".")[0]
        for name, parameter in model.named_parameters()
        if parameter.requires_grad
    }

    assert trainable == {"layer4.attention", "fc"}

    with torch.no_grad():
        assert model.eval()(torch.zeros(1, 3, 224, 224)).shape == (1, 1)


def test_attention_variants_cannot_use_fvei_last_block_finetuning():
    model = build_regression_model("resnet50_se", pretrained=False)
    with pytest.raises(ValueError):
        configure_last_block_finetuning(model, "resnet50_se")
