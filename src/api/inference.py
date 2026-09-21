from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import torch
from PIL import Image
from torch import nn

from src.training.train_vgg16 import build_vgg16_regression_model
from src.training.cidet_dataloader import get_cidet_transforms


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

DEFAULT_CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "results"
    / "checkpoints"
    / "vgg16_cidet_block5_huber_best.pth"
)


@dataclass(frozen=True)
class VisibilityPrediction:
    visibility_m: float
    checkpoint_epoch: int | None
    validation_mae_m: float | None


class VisibilityPredictor:
    """Inference wrapper for the selected CIDET development checkpoint."""

    def __init__(
        self,
        checkpoint_path: Path = DEFAULT_CHECKPOINT_PATH,
        device: torch.device | str = DEVICE,
    ) -> None:
        self.checkpoint_path = Path(checkpoint_path)
        self.device = torch.device(device)

        if not self.checkpoint_path.is_file():
            raise FileNotFoundError(
                f"Checkpoint not found: {self.checkpoint_path}"
            )

        self.transform = get_cidet_transforms()

        self.model: nn.Module = build_vgg16_regression_model()

        checkpoint = torch.load(
            self.checkpoint_path,
            map_location=self.device,
            weights_only=False,
        )

        if "model_state_dict" not in checkpoint:
            raise KeyError(
                "Checkpoint does not contain 'model_state_dict'."
            )

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.to(self.device)
        self.model.eval()

        self.checkpoint_epoch = self._optional_int(
            checkpoint.get("epoch")
        )

        self.validation_mae_m = self._optional_float(
            checkpoint.get("validation_mae")
        )

    @staticmethod
    def _optional_int(value: object) -> int | None:
        if value is None:
            return None
        return int(value)

    @staticmethod
    def _optional_float(value: object) -> float | None:
        if value is None:
            return None
        return float(value)

    def predict(self, image: Image.Image) -> VisibilityPrediction:
        """Estimate visibility in metres for one RGB image."""

        rgb_image = image.convert("RGB")
        image_tensor = self.transform(rgb_image).unsqueeze(0)
        image_tensor = image_tensor.to(self.device)

        with torch.inference_mode():
            output = self.model(image_tensor)

        visibility_m = float(output.reshape(-1)[0].item())

        return VisibilityPrediction(
            visibility_m=visibility_m,
            checkpoint_epoch=self.checkpoint_epoch,
            validation_mae_m=self.validation_mae_m,
        )


def load_image(image_path: Path | str) -> Image.Image:
    """Load an image from disk while ensuring the file is decoded."""

    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    with Image.open(path) as image:
        image.load()
        return image.convert("RGB")




