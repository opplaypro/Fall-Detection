import numpy as np
import logging
from typing import Tuple


logger = logging.getLogger(__name__)


def detect_fall(
        accelerometer_data: np.ndarray,
        gyroscope_data: np.ndarray,
        frequency: int
        ) -> bool:
    """
    Detects peaks in the given data that may indicate a fall event.

    Parameters
    ----------
    accelerometer_data : list | np.ndarray
        The input accelerometer signal data to analyze.
    gyroscope_data : list | np.ndarray
        The input gyroscope signal data to analyze.
    frequency : int
        The sampling frequency of the data.

    Returns
    -------
    bool
        True if a fall is detected, False otherwise.
    """
    # calculate acceleration magnitude
    magnitude = np.linalg.norm(accelerometer_data, axis=1)
    # simple peak detection
    threshold = 30.0  # example threshold for fall detection
    peaks = magnitude > threshold
    if np.sum(peaks) > 0:
        logger.debug("Possible fall peak detected.")
        return True
    else:

        return False
