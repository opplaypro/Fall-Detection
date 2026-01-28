from core import log

import kivy
from kivy.lang import Builder

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

from pathlib import Path
import logging
import json

# Import our screens to register them
import ui  # noqa: F401
kivy.require('2.0.0')

# Load all KV files
for kv_file in Path(__file__).parent.glob('ui/screens/*.kv'):
    Builder.load_file(str(kv_file))


# Root layout of the application
class RootLayout(MDBoxLayout):
    pass


class FallDetectionApp(MDApp):

    def build(self):
        # logging errors to file and console
        log.setup_logging(self)
        logger = logging.getLogger(__name__)
        logger.info("Building the application UI")

        # load configuration
        config_path = Path(__file__).parent / 'config' / 'config.json'
        self.config = json.load(open(config_path))
        logger.info("Configuration loaded")

        # set logging level to config value
        logging_level = self.config.get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, logging_level))

        # Set theme
        self.theme_cls.theme_style = self.config.get(
            'general', {}).get('theme_style', 'Light')
        self.theme_cls.primary_palette = self.config.get(
            'general', {}).get('theme_primary_palette', 'midnightblue')
        self.theme_cls.accent_palette = self.config.get(
            'general', {}).get('theme_accent_palette', 'crimson')

        # get tranlations
        lang_path = self.config.get('general', {}).get('language', 'en')
        logger.info(f"Setting application language to: {lang_path}")
        self.lang = json.load(open(
            Path(__file__).parent / 'assets' / 'lang' / f'{lang_path}.json'
            ))
        return RootLayout()

    def on_switch_tabs(self, bar, item, icon, label):
        logger = logging.getLogger(__name__)
        logger.debug(f"Switching to tab: {label}")
        logger.debug(f"Switching to screen id: {item.tag}")

        self.root.ids.screen_manager.current = item.tag  # type: ignore


if __name__ == '__main__':
    FallDetectionApp().run()
