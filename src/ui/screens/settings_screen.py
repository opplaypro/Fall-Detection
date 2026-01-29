import kivy
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.app import MDApp
from core.algorithm import detect_fall
import logging

logger = logging.getLogger(__name__)


# temporary class, will change, not documented
class SettingsScreen(MDScreen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        app = MDApp.get_running_app()
        if app is None or not hasattr(app, 'sensor'):
            logger.error("Sensor instance not found in MDApp.")
            raise ValueError("Sensor instance not found in MDApp.")
        self.sensor = app.sensor

    def on_enter(self, *args):
        # Update color only on mobile platforms
        if kivy.platform == 'android' or kivy.platform == 'ios':
            Clock.schedule_interval(self.update_color, 1.0 / 10.0)

    def on_leave(self, *args):
        Clock.unschedule(self.update_color)

    def update_color(self, dt):
        try:
            acc_val = self.sensor.get_accelerometer_data()
            gyro_val = self.sensor.get_gyroscope_data()
            if acc_val is not None:
                fall_detected = detect_fall(
                    acc_val,
                    gyro_val,
                    self.sensor.frequency)
                # Ensure we have a python float, not a numpy float
                if fall_detected:
                    self.ids.status_icon.icon = "shield-alert"
                    self.ids.status_icon.color = (1, 0, 0, 1)
                else:
                    self.ids.status_icon.icon = "shield-check"
                    self.ids.status_icon.color = (0, 1, 0, 1)
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
