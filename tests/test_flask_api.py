from io import BytesIO

import pytest
from PIL import Image

import src.api.app as app_module
from src.api.inference import VisibilityPrediction


class FakePredictor:
    """Small deterministic predictor used only by API unit tests."""

    checkpoint_epoch = 12
    validation_mae_m = 26.442758973439535

    def predict(self, image: Image.Image) -> VisibilityPrediction:
        return VisibilityPrediction(
            visibility_m=123.456,
            checkpoint_epoch=self.checkpoint_epoch,
            validation_mae_m=self.validation_mae_m,
        )


@pytest.fixture(autouse=True)
def fake_predictor(monkeypatch):
    predictor = FakePredictor()

    monkeypatch.setattr(
        app_module,
        "get_predictor",
        lambda: predictor,
    )

    return predictor


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as client:
        yield client


def test_home_page_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"FOG VIEW" in response.data


def test_health_endpoint_returns_model_status(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert data["model"] == "VGG16 FVEI Block5 Fine-Tuned"
    assert data["checkpoint_epoch"] == 12
    assert data["validation_mae_m"] == pytest.approx(
        26.442758973439535
    )


def test_predict_requires_image(client):
    response = client.post(
        "/predict",
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data


def test_predict_rejects_unsupported_extension(client):
    response = client.post(
        "/predict",
        data={
            "image": (
                BytesIO(b"not-an-image"),
                "sample.txt",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data


def test_predict_returns_visibility_for_valid_image(client):
    image = Image.new(
        "RGB",
        (64, 64),
        (180, 180, 180),
    )

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    response = client.post(
        "/predict",
        data={
            "image": (
                buffer,
                "sample.jpg",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["visibility_m"] == 123.46
    assert data["unit"] == "m"
    assert data["model"] == "VGG16 FVEI Block5 Fine-Tuned"
    assert data["checkpoint_epoch"] == 12


def test_health_returns_503_when_checkpoint_is_unavailable(
    client,
    monkeypatch,
):
    def unavailable_predictor():
        raise FileNotFoundError("Checkpoint not found.")

    monkeypatch.setattr(
        app_module,
        "get_predictor",
        unavailable_predictor,
    )

    response = client.get("/health")

    assert response.status_code == 503

    data = response.get_json()

    assert data["status"] == "unavailable"
    assert data["model"] == "VGG16 FVEI Block5 Fine-Tuned"
    assert "error" in data
