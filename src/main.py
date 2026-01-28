from core import log
import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import DictProperty
import numpy as np
from kivy.lang import Builder
from pathlib import Path
import logging

# Import our screen
from ui.screens.home_screen import HomeScreen

kivy.require('2.0.0')

# Explicitly load the kv file
kv_path = Path(__file__).parent / 'ui' / 'screens' / 'home_screen.kv'
Builder.load_file(str(kv_path))


class MyApp(MDApp):

    colors = DictProperty({
            'warn': np.array([255, 103, 0, 255])/255,
            'bg': np.array([235, 235, 235, 255])/255,
            'acc1': np.array([58, 110, 165, 255])/255,
            'acc2': np.array([0, 78, 152, 255])/255,
            'shade': np.array([235, 235, 235, 255])/255,
            'green': np.array([112, 224, 0, 255])/255
            })

    def build(self):
        log.setup_logging(self)
        logger = logging.getLogger(__name__)
        logger.info("Building the application UI")
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm


if __name__ == '__main__':
    MyApp().run()
