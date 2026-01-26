from core import log
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from pathlib import Path
import logging

# Import our screen
from ui.screens.home_screen import HomeScreen

kivy.require('2.0.0')

# Explicitly load the kv file
kv_path = Path(__file__).parent / 'ui' / 'screens' / 'home_screen.kv'
Builder.load_file(str(kv_path))


class MyApp(App):
    def build(self):
        log.setup_logging(self)
        logger = logging.getLogger(__name__)
        logger.info("Building the application UI")
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    MyApp().run()
