from kivymd.uix.screen import MDScreen
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
