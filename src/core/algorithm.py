import numpy as np
import logging
from typing import Tuple


logger = logging.getLogger(__name__)


def detect_fall(
        data: np.ndarray,
        frequency: int
        ) -> Tuple[float, bool]:
    """
    Detects peaks in the given data that may indicate a fall event.

    Parameters
    ----------
    data : list | np.ndarray
        The input signal data to analyze.
    frequency : int
        The sampling frequency of the data.

    Returns
    -------
    float
        The magnitude of detected falls.
    bool
        True if a fall is detected, False otherwise.
    """
    # calculate acceleration magnitude
    magnitude = np.linalg.norm(data, axis=1)
    # simple peak detection
    threshold = 30.0  # example threshold for fall detection
    peaks = magnitude > threshold
    if np.sum(peaks) > 0:
        logger.debug("Possible fall peak detected.")
        return float(magnitude[-1]), True
    else:

        return float(magnitude[-1]), False
