from core import log
from core import Sensor, detect_fall
import ui  # noqa: F401

import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp

from pathlib import Path
import logging
import json


kivy.require('2.0.0')

# Load all KV files
for kv_file in Path(__file__).parent.glob('ui/screens/*.kv'):
    Builder.load_file(str(kv_file))


# Root layout of the application
class RootLayout(MDBoxLayout):
    pass


class FallDetectionApp(MDApp):

    def build(self):
        self.logger = logging.getLogger(__name__)

        # load configuration
        config_path = Path(__file__).parent / 'config' / 'config.json'
        self.config = json.load(open(config_path))
        self.logger.info("Configuration loaded")

        # set logging level to config value
        logging_level = self.config.get('logging', {}).get('level', 'INFO')
        self.logger.setLevel(getattr(logging, logging_level))

        # Set theme
        self.theme_cls.theme_style = self.config.get(
            'general', {}).get('theme_style', 'Light')
        self.theme_cls.primary_palette = self.config.get(
            'general', {}).get('theme_primary_palette', 'Red')
        self.theme_cls.accent_palette = self.config.get(
            'general', {}).get('theme_accent_palette', 'Blue')

        # get tranlations
        lang_path = self.config.get('general', {}).get('language', 'en')
        self.logger.info(f"Setting application language to: {lang_path}")
        self.lang = json.load(open(
            Path(__file__).parent / 'assets' / 'lang' / f'{lang_path}.json'
            ))

        return RootLayout()

    def on_switch_tabs(self, bar, item, icon, label):
        self.logger.debug(f"Switching to tab: {label}")
        self.logger.debug(f"Switching to screen id: {item.tag}")

        self.root.ids.screen_manager.current = item.tag  # type: ignore

    def on_start(self):
        if kivy.platform == 'android':
            import android
            android.start_service(
                title='Fall Service',
                description='Fall Detection Service',
                arg=''
            )
        return super().on_start()



if __name__ == '__main__':
    if kivy.platform == 'linux':  # only for testing on PC
        Window.size = (412, 915)
    app = FallDetectionApp()
    log.setup_logging(app)
    logger = logging.getLogger(__name__)
    logger.info(logger.name + " started")
    app.run()
