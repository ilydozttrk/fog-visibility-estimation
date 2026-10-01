import random
import numpy as np
import torch


def set_seed(seed: int) -> None:
    """
    Sets random seed for reproducible experiments.
    """

    random.seed(seed)

    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # Some CUDA operations used by VGG16, including AdaptiveAvgPool2d backward,
    # do not provide a strictly deterministic implementation. Keep deterministic
    # algorithms enabled where available and warn instead of aborting.
    torch.use_deterministic_algorithms(True, warn_only=True)