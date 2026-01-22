from kivy.clock import Clock
from plyer import accelerometer, gyroscope
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DataBuffer:
    def __init__(
            self,
            buffer_size=100
            ) -> None:
        """
        Creates a data buffer to hold sensor data.

        Parameters
        ----------
        buffer_size : int
            how many samples to keep in buffer
        """
        self.buffer_size = buffer_size
        self.buffer_x = np.ndarray([])
        self.buffer_y = np.ndarray([])
        self.buffer_z = np.ndarray([])
        self.is_full = False

        logger.info(f"Initializing DataBuffer with size {buffer_size}")

    def add_sample(self, x: float, y: float, z: float) -> None:
        """
        Adds a new sample to the buffer.

        Parameters
        ----------
        x : float
            x-axis data
        y : float
            y-axis data
        z : float
            z-axis data
        """
        if self.buffer_x.size < self.buffer_size:
            self.buffer_x = np.append(self.buffer_x, x)
            self.buffer_y = np.append(self.buffer_y, y)
            self.buffer_z = np.append(self.buffer_z, z)
            if self.buffer_x.size == self.buffer_size:
                self.is_full = True
        else:
            self.buffer_x = np.roll(self.buffer_x, -1)
            self.buffer_y = np.roll(self.buffer_y, -1)
            self.buffer_z = np.roll(self.buffer_z, -1)
            self.buffer_x[-1] = x
            self.buffer_y[-1] = y
            self.buffer_z[-1] = z

    def get_data(self) -> np.ndarray:
        """
        Returns the buffered data as a numpy array of shape (buffer_size, 3).

        Returns
        -------
        np.ndarray
            Buffered data
        """
        if not self.is_full:
            logger.error("Buffer is not full yet, cannot get data.")

            raise ValueError("Buffer is not full yet, cannot get data.")

        data = np.column_stack((self.buffer_x, self.buffer_y, self.buffer_z))
        return data


class Sensor:
    """
    docstring for Sensor
    """
    def __init__(
            self,
            frequency: int = 50,
            ) -> None:
        """
        Initializes the Sensor class.

        Parameters
        ----------
        frequency : int
            Frequency of data collection in Hz.
        """
        self.is_active = False
        self.frequency = frequency
        self.accelerometer_data_buffer = DataBuffer()
        self.gyroscope_data_buffer = DataBuffer()
        self.accelerometer = accelerometer
        self.gyroscope = gyroscope

    def start_sensor(self):
        """
        Starts the sensor data collection.
        """
        if not self.is_active:
            try:
                if not self.accelerometer:
                    raise RuntimeError("Accelerometer not available.")
                elif not hasattr(self.accelerometer, 'enable'):
                    raise RuntimeError("Accelerometer enable not available.")
                elif not callable(self.accelerometer.enable):
                    raise RuntimeError("Accelerometer enable not callable.")
                else:
                    self.accelerometer.enable()

                if not self.gyroscope:
                    raise RuntimeError("Gyroscope not available.")
                elif not hasattr(self.gyroscope, 'enable'):
                    raise RuntimeError("Gyroscope enable not available.")
                elif not callable(self.gyroscope.enable):
                    raise RuntimeError("Gyroscope enable not callable.")
                else:
                    self.gyroscope.enable()
                Clock.schedule_interval(self.update, 1.0 / self.frequency)
                self.is_active = True
                logger.info("Sensors started")
            except Exception as e:
                logger.error(f"Error starting sensors: {e}")
        else:
            logger.warning("Sensors are already active")

    def stop_sensor(self):
        """
        Stops the sensor data collection.
        """
        if self.is_active:
            try:
                if not self.accelerometer:
                    raise RuntimeError("Accelerometer not available.")
                elif not hasattr(self.accelerometer, 'disable'):
                    raise RuntimeError("Accelerometer disable not available.")
                elif not callable(self.accelerometer.disable):
                    raise RuntimeError("Accelerometer disable not callable.")
                else:
                    self.accelerometer.disable()

                if not self.gyroscope:
                    raise RuntimeError("Gyroscope not available.")
                elif not hasattr(self.gyroscope, 'disable'):
                    raise RuntimeError("Gyroscope disable not available.")
                elif not callable(self.gyroscope.disable):
                    raise RuntimeError("Gyroscope disable not callable.")
                else:
                    self.gyroscope.disable()

                Clock.unschedule(self.update)
                self.is_active = False
                logger.info("Sensors stopped")
            except Exception as e:
                logger.error(f"Error stopping sensors: {e}")
        else:
            logger.warning("Sensors are not active")

    def update(self, dt):
        """
        Updates the sensor data buffers.
        """
        try:
            acc_val = self.accelerometer.acceleration
            gyro_val = self.gyroscope.rotation

            if acc_val is not None:
                x, y, z = acc_val
                self.accelerometer_data_buffer.add_sample(x, y, z)

            if gyro_val is not None:
                x, y, z = gyro_val
                self.gyroscope_data_buffer.add_sample(x, y, z)

        except Exception as e:
            logger.error(f"Error reading sensors: {e}")

    def get_accelerometer_data(self) -> np.ndarray:
        """
        Returns the buffered accelerometer data.

        Returns
        -------
        np.ndarray
            Buffered accelerometer data
        """
        return self.accelerometer_data_buffer.get_data()

    def get_gyroscope_data(self) -> np.ndarray:
        """
        Returns the buffered gyroscope data.

        Returns
        -------
        np.ndarray
            Buffered gyroscope data
        """
        return self.gyroscope_data_buffer.get_data()
