from io import BytesIO

import pytest

from src.api.app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)

    with app.test_client() as client:
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
    assert "model" in data
    assert "checkpoint_epoch" in data
    assert "validation_mae_m" in data


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
