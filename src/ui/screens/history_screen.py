from kivy.properties import StringProperty, ColorProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
import logging

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
            color = [1, 1, 1, 1]
        elif event == "fall_detected":
            color = [250/255, 220/255, 224/255, 1]
        else:
            color = [1, 0, 0, 1]
        return DateCard(
            date_text=date,
            time_text=time,
            bg_color=color
        )

    def load_history(self) -> None:
        data = MDApp.get_running_app().history  # type: ignore
        self.ids.card_container.clear_widgets()

        for entry in data[::-1]:  # from newest to oldest
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
