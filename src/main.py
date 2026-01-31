from core import log
import ui  # noqa: F401

import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import mainthread, Clock
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from jnius import autoclass

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.was_minimized = False

    def build(self):
        self.logger = logging.getLogger(__name__)

        # load configuration
        self.config_path = Path(__file__).parent / 'config' / 'config.json'
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
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

        # load fonts
        fonts_path = Path(__file__).parent / 'assets' / 'fonts'
        LabelBase.register(
            name='Roboto',
            fn_regular=str(fonts_path / 'Roboto-Regular.ttf'),
            fn_bold=str(fonts_path / 'Roboto-Bold.ttf')
        )

        LabelBase.register(
            name='Cabin',
            fn_regular=str(fonts_path / 'Cabin-Regular.ttf'),
            fn_bold=str(fonts_path / 'Cabin-Bold.ttf')
        )

        # set fonts to theme
        self.theme_cls.font_styles["Display"] = {
            "large": {
                "font-name": "Cabin",
                "font-size": "32sp",
                "line-height": 1.1,
                "letter-spacing": 0,
            },
            "medium": {
                "font-name": "Cabin",
                "font-size": "28sp",
                "line-height": 1.1,
                "letter-spacing": 0,
            },
            "small": {
                "font-name": "Cabin",
                "font-size": "24sp",
                "line-height": 1.1,
                "letter-spacing": 0,
            }
        }

        self.theme_cls.font_styles["Headline"] = {
            "large": {
                "font-name": "Roboto",
                "font-size": "32sp",
                "line-height": 1.1,
                "letter-spacing": 0,
            },
            "medium": {
                "font-name": "Roboto",
                "font-size": "28sp",
                "line-height": 1.1,
                "letter-spacing": 0,
            },
            "small": {
                "font-name": "Roboto",
                "font-size": "24sp",
                "line-height": 1.1,
                "letter-spacing": 0,
            }
        }

        # get tranlations
        lang_path = self.config.get('general', {}).get('language', 'en')
        self.logger.info(f"Setting application language to: {lang_path}")
        self.lang = json.load(open(
            Path(__file__).parent / 'assets' / 'lang' / f'{lang_path}.json'
            ))

        self.history = json.load(open(
            Path(__file__).parent / 'data' / 'history.json'
            ))

        return RootLayout()

    def on_setting_toggle(self, setting_name: str, enabled: bool):
        """
        Handle setting toggle changes.

        Parameters
        ----------
        setting_name : str
            The name of the setting that was toggled.
        enabled : bool
            The new state of the setting.
        """
        self.logger.info(f"Setting '{setting_name}' toggled to: {enabled}")

        # Update the config
        if 'settings' not in self.config:
            self.config['settings'] = {}

        self.config['settings'][setting_name] = enabled

        # Save the config to file
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.debug(f"Configuration saved: {setting_name}={enabled}")
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")

    def on_switch_tabs(self, bar, item, icon, label):
        self.logger.debug(f"Switching to tab: {label}")
        self.logger.debug(f"Switching to screen id: {item.tag}")

        self.root.ids.screen_manager.current = item.tag  # type: ignore

    def switch_to_alert_screen(self):
        self.logger.info("Switching to Alert Screen")
        self.root.ids.screen_manager.current = "alert_screen"  # type: ignore

    def on_false_alarm(self):
        sm = self.root.ids.screen_manager  # type: ignore

        if sm.current == 'alert_screen':
            sm.current = 'home'

            if self.was_minimized:
                self.minimize_app()
                self.was_minimized = False

    def no_false_alarm(self):
        pass

    def minimize_app(self):
        try:
            PyActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            intent = Intent(Intent.ACTION_MAIN)
            intent.addCategory(Intent.CATEGORY_HOME)
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            PyActivity.mActivity.startActivity(intent)
        except Exception as e:
            self.logger.error(f"Error minimizing app: {e}")

    # ran when app is started
    def on_start(self):
        if kivy.platform != 'android':
            self.logger.warning("Not running on Android, skipping service")
            return
        from android import AndroidService  # type: ignore
        service = AndroidService(
            'Fall Detection Service',
            'Fall detection running',
            )
        service.start('service started')
        self.logger.info("SERVICE: Android service started")

        # Setup OSC server to receive messages from the service
        self.osc_server = OSCThreadServer()
        self.osc_server.listen(address='127.0.0.1', port=3000, default=True)
        self.osc_server.bind(b'/fall_detected', self.handle_fall_detected)
        self.osc_server.bind(b'/error', self.handle_error)
        self.osc_client = OSCClient('127.0.0.1', 3001)

    def on_pause(self):
        self.was_minimized = True
        return True

    def on_resume(self):
        pass

    # handle messages from service
    @mainthread
    def handle_fall_detected(self, message):
        try:
            message = message.decode('utf-8')
            self.logger.debug(f"Received update: {message}")
            Clock.schedule_once(lambda dt: self.switch_to_alert_screen())
        except Exception as e:
            self.logger.error(f"Error handling update message: {e}")

    @mainthread
    def handle_error(self, message):
        try:
            data = message.decode('utf-8')
            self.logger.error(f"Received error: {data}")
        except Exception as e:
            self.logger.error(f"Error handling error message: {e}")


if __name__ == '__main__':
    if kivy.platform == 'linux':  # only for testing on PC
        Window.size = (412, 915)
    app = FallDetectionApp()
    log.setup_logging(app)
    logger = logging.getLogger(__name__)
    logger.info(logger.name + " started")
    app.run()
