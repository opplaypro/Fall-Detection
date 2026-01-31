from kivymd.uix.screen import MDScreen
from kivy.properties import BooleanProperty, StringProperty
import logging

logger = logging.getLogger(__name__)


class SettingPanel(MDScreen):
    setting_name = StringProperty()
    enabled = BooleanProperty()


# temporary class, will change, not documented
class SettingsScreen(MDScreen):

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def create_setting_panel(
            self,
            name: str,
            enabled: bool
            ) -> SettingPanel:
        """
        Builds a setting panel for the settings screen.

        Parameters
        ----------
        name : str
            The name of the setting.
        enabled : bool
            The enabled state of the setting.

        Returns
        -------
        SettingPanel
            The constructed setting panel.
        """
        return SettingPanel(
            setting_name=name,
            enabled=enabled
        )

    def load_settings(self) -> None:
        from kivymd.app import MDApp
        app = MDApp.get_running_app()

        # Load settings from app config
        # If settings section doesn't exist, use empty dict
        data = app.config.get('settings', {})  # type: ignore

        if not data:
            logger.warning("No settings found in config, screen will be empty")

        self.ids.settings_container.clear_widgets()

        for setting, state in data.items():
            panel = self.create_setting_panel(setting, state)
            self.ids.settings_container.add_widget(panel)

    def on_enter(self, *args):
        self.load_settings()
        logger.debug("Entered Settings Screen")

    def on_leave(self, *args):
        logger.debug("Left Settings Screen")
