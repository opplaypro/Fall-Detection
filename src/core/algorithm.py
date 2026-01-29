import numpy as np
import logging


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
    accelerometer_data : np.ndarray
        The input accelerometer signal data to analyze.
    gyroscope_data : np.ndarray
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
    # Parameters for fall detection
    impact_threshold = 30.0  # m/s^2 (approx 3g)
    free_fall_threshold = 6.0  # m/s^2 (approx 0.6g)
    window_duration = 0.5  # seconds (time window to look for free fall before impact)

    # Find indices where magnitude exceeds impact threshold
    impact_indices = np.where(magnitude > impact_threshold)[0]

    if len(impact_indices) == 0:
        return False

    # Calculate window size in samples
    window_samples = int(window_duration * frequency)

    for i in impact_indices:
        # Check a window before the impact for free fall
        start_idx = max(0, i - window_samples)
        pre_impact_window = magnitude[start_idx:i]

        # If we find a free fall period shortly before the impact, it's likely a fall
        if np.any(pre_impact_window < free_fall_threshold):
            logger.debug(f"Fall detected: Impact at sample {i} preceded by free fall.")
            return True

    return False
