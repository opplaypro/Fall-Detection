from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.clock import Clock
from core.sensors import Sensor
import logging

logger = logging.getLogger(__name__)


# temporary class, will change, not documented
class HomeScreen(Screen):
    background_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.sensor = Sensor(frequency=10)

    def on_enter(self):
        self.sensor.start_sensor()
        Clock.schedule_interval(self.update_color, 1.0 / 10.0)

    def on_leave(self):
        self.sensor.stop_sensor()
        Clock.unschedule(self.update_color)

    def update_color(self, dt):
        try:
            acc_val = self.sensor.accelerometer.acceleration
            if acc_val and all(v is not None for v in acc_val):
                x, y, z = acc_val
                r = min(abs(x) / 10.0, 1.0)
                g = min(abs(y) / 10.0, 1.0)
                b = min(abs(z) / 10.0, 1.0)
                self.background_color = [r, g, b, 1]
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
