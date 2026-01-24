from datetime import datetime
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
        self.setup_logging()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm

    def setup_logging(self) -> None:
        """
        Sets up logging configuration. Creates a logs directory,
        renames the existing latest.log file and initializes a new latest.log
        file with the current date and time.
        """
        user_data = Path(App.get_running_app().user_data_dir)  # type: ignore
        log_directory = user_data / 'logs'
        log_directory.mkdir(parents=True, exist_ok=True)
        latest_log = log_directory / 'latest.log'

        if latest_log.exists():
            try:
                date = latest_log.read_text().splitlines()[0]
                old_date = date.replace(' ', '_').replace(':', '_')
                latest_log.rename(log_directory / f'log_{old_date}.log')
            except Exception as e:
                print(f"Error renaming log file: {e}")
        current_time = datetime.now().strftime('%Y_%m_%d %H_%M_%S')
        latest_log.write_text(current_time + '\n', encoding='utf-8')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=latest_log,
            filemode='a'
            )
        logger = logging.getLogger(__name__)
        logger.info("Starting application")


if __name__ == '__main__':
    MyApp().run()
