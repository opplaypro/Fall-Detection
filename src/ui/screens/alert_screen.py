from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.properties import ListProperty
import logging

logger = logging.getLogger(__name__)


# temporary class, will change, not documented
class AlertScreen(MDScreen):

    background_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(AlertScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        logger.debug("Entered Alert Screen")

    def on_leave(self, *args):
        logger.debug("Left Alert Screen")

    def false_alarm(self):
        app = MDApp.get_running_app()
        try:
            app.osc_client.send_message(b'/stop_alert', [])  # type: ignore
        except Exception as e:
            logger.error(f"Error sending stop_alert message: {e}")
        logger.info("False alarm triggered from Alert Screen")
        app.on_false_alarm()
