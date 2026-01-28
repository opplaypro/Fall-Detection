from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.clock import Clock
from core.sensors import Sensor, DataBuffer
from core.algorithm import detect_fall
import logging

logger = logging.getLogger(__name__)


# temporary class, will change, not documented
class HomeScreen(Screen):

    background_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        data_buffer_acc: DataBuffer = DataBuffer()
        data_buffer_gyro: DataBuffer = DataBuffer()
        self.sensor: Sensor = Sensor(
            buffer_acc=data_buffer_acc,
            buffer_gyro=data_buffer_gyro,
            frequency=50)

    def on_enter(self, *args):
        self.sensor.start_sensor()
        # Clock.schedule_interval(self.update_color, 1.0 / 10.0)

    def on_leave(self, *args):
        self.sensor.stop_sensor()
        Clock.unschedule(self.update_color)

    def update_color(self, dt):
        try:
            acc_val = self.sensor.get_accelerometer_data()
            if acc_val is not None:
                mag_val, fall_detected = detect_fall(
                    acc_val, self.sensor.frequency)
                # Ensure we have a python float, not a numpy float
                norm_mag = float(min(max(mag_val / 100.0, 0), 1))*10
                fall_detected_val = 1.0 if fall_detected else 0.0
                self.background_color = [norm_mag/3, fall_detected_val, 0, 1]
            elif not self.sensor.accelerometer:
                import math
                import time
                t = time.time()
                r = (math.sin(t) + 1) / 2
                g = (math.cos(t) + 1) / 2
                b = (math.sin(t * 0.5) + 1) / 2
                self.background_color = [r, g, b, 1]
        except Exception as e:
            logger.error(f"Error updating color: {e}")
