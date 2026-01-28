from core import log
import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from pathlib import Path
import logging
import toml

# Import our screen
from ui.screens.home_screen import HomeScreen

kivy.require('2.0.0')

# Explicitly load the kv file
kv_path = Path(__file__).parent / 'ui' / 'screens' / 'home_screen.kv'
Builder.load_file(str(kv_path))


class FallDetectionApp(MDApp):

    def build(self):
        # logging errors to file and console
        log.setup_logging(self)
        logger = logging.getLogger(__name__)
        logger.info("Building the application UI")

        # Set theme
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "deepskyblue"
        self.theme_cls.accent_palette = "crimson"

        # load configuration
        config_path = Path(__file__).parent / 'config' / 'config.toml'
        self.config = toml.load(config_path)
        logger.info("Configuration loaded")

        # get tranlations
        lang_path = self.config.get('general', {}).get('language', 'en')
        logger.info(f"Setting application language to: {lang_path}")
        self.lang = toml.load(
            Path(__file__).parent / 'assets' / 'lang' / f'{lang_path}.toml'
            )

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    FallDetectionApp().run()
