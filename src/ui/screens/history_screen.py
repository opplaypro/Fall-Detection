from kivy.properties import StringProperty, ColorProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from pathlib import Path
import kivy
import logging
import json

logger = logging.getLogger(__name__)


class DateCard(MDCard):
    date_text = StringProperty()
    time_text = StringProperty()
    bg_color = ColorProperty()


# temporary class, will change, not documented
class HistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

    def create_card(
            self,
            date: str,
            time: str,
            event: str
            ) -> DateCard:
        """
        Builds a card for the history screen.

        Parameters
        ----------
        date : str
            The date of the event.
        time : str
            The time of the event.
        event : str
            The event description.

        Returns
        -------
        DateCard
            The constructed date card.
        """

        if event == "false_alarm":
            color = self.theme_cls.primaryContainerColor
        elif event == "fall_detected":
            color = self.theme_cls.errorContainerColor
        else:
            color = self.theme_cls.primaryColor
        return DateCard(
            date_text=date,
            time_text=time,
            bg_color=color
        )

    def load_history(self) -> None:
        App = MDApp.get_running_app()
        file_rel = App.config.get(  # type: ignore
            'fall_log', {}).get('file', 'data/history.json')
        path = Path(App.user_data_dir) / file_rel  # type: ignore
        if kivy.platform == "linux":
            path = Path(__file__).parent / ".." / ".." / file_rel
        data = json.load(open(path, 'r', encoding='utf-8'))
        self.ids.card_container.clear_widgets()

        for entry in data:
            card = self.create_card(
                date=entry.get('date', 'N/A'),
                time=entry.get('time', 'N/A'),
                event=entry.get('event', 'N/A')
            )
            self.ids.card_container.add_widget(card)

    def on_enter(self, *args):
        self.load_history()
        logger.debug("Entered History Screen")

    def on_leave(self, *args):
        logger.debug("Left History Screen")
