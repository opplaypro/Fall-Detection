from kivymd.uix.screen import MDScreen
import logging

logger = logging.getLogger(__name__)


# temporary class, will change, not documented
class SettingsScreen(MDScreen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
