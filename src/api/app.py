from __future__ import annotations

import io

from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError

from src.api.inference import VisibilityPredictor


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(__name__)

predictor = VisibilityPredictor()


def allowed_file(filename: str) -> bool:
    """Return True when the uploaded file has a supported extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )



@app.get("/")
def index():
    """Render the visibility estimation web interface."""
    return render_template("index.html")

@app.get("/health")
def health():
    """Simple service health endpoint."""
    return jsonify(
        {
            "status": "ok",
            "model": "VGG16 CIDET Block5 Huber",
            "checkpoint_epoch": predictor.checkpoint_epoch,
            "validation_mae_m": predictor.validation_mae_m,
        }
    )


@app.post("/predict")
def predict():
    """Estimate visibility in metres from an uploaded image."""

    if "image" not in request.files:
        return jsonify(
            {"error": "No image file was provided."}
        ), 400

    uploaded_file = request.files["image"]

    if not uploaded_file.filename:
        return jsonify(
            {"error": "No image file was selected."}
        ), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify(
            {
                "error": (
                    "Unsupported file type. "
                    "Use JPG, JPEG, or PNG."
                )
            }
        ), 400

    try:
        image_bytes = uploaded_file.read()

        with Image.open(io.BytesIO(image_bytes)) as image:
            image.load()
            prediction = predictor.predict(image)

    except (UnidentifiedImageError, OSError):
        return jsonify(
            {"error": "The uploaded file is not a valid image."}
        ), 400

    return jsonify(
        {
            "visibility_m": round(prediction.visibility_m, 2),
            "unit": "m",
            "model": "VGG16 CIDET Block5 Huber",
            "checkpoint_epoch": prediction.checkpoint_epoch,
        }
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )

