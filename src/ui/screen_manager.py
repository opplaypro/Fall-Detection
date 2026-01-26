from kivy.uix.screenmanager import ScreenManager, FadeTransition
import logging

logger = logging.getLogger(__name__)


class AppScreenManager(ScreenManager):
    """
    Manages transitions between different screens in the app.
    """
    def __init__(self, **kwargs):
        super(AppScreenManager, self).__init__(**kwargs)
        self.transition = FadeTransition()

    def switch_to(self, screen, **options):
        """
        Switches the current display to the specified screen name.
        """
        direction = options.get('direction', 'left')
        if self.has_screen(screen):
            if hasattr(self.transition, 'direction'):
                self.transition.direction = direction
            self.current = screen
        else:
            logger.error(f"Screen '{screen}' not found in ScreenManager.")
