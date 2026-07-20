from pathlib import Path

import torch


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
GENERATED_DATA_DIR = DATA_DIR / "generated"
IMAGES_DIR = GENERATED_DATA_DIR / "images"
LABELS_CSV = GENERATED_DATA_DIR / "labels.csv"

RESULTS_DIR = PROJECT_ROOT / "results"
CHECKPOINTS_DIR = RESULTS_DIR / "checkpoints"
LOGS_DIR = RESULTS_DIR / "logs"

VGG16_CHECKPOINT_PATH = CHECKPOINTS_DIR / "vgg16_baseline_best.pth"


# =========================================================
# DATA SETTINGS
# =========================================================

IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_WORKERS = 0

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15


# =========================================================
# MODEL SETTINGS
# =========================================================

MODEL_NAME = "vgg16"
PRETRAINED = True
FREEZE_BACKBONE = True

REGRESSION_HIDDEN_DIM_1 = 512
REGRESSION_HIDDEN_DIM_2 = 128
DROPOUT_RATE = 0.30
OUTPUT_DIM = 1


# =========================================================
# TRAINING SETTINGS
# =========================================================

LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-5
NUM_EPOCHS = 20

LOSS_FUNCTION = "L1Loss"
OPTIMIZER_NAME = "Adam"


# =========================================================
# REPRODUCIBILITY SETTINGS
# =========================================================

RANDOM_SEED = 42
DETERMINISTIC_ALGORITHMS = True
CUDNN_BENCHMARK = False


# =========================================================
# DEVICE SETTINGS
# =========================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_output_directories() -> None:
    """
    Eğitim çıktılarının kaydedileceği klasörleri oluşturur.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)