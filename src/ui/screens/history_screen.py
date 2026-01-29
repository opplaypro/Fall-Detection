from kivymd.uix.screen import MDScreen
import logging

logger = logging.getLogger(__name__)


# temporary class, will change, not documented
class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
