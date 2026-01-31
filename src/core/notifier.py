from jnius import autoclass
from pathlib import Path
import time
import json


def log_file(level: str, message: str) -> None:
    """
    Logs a message to the Android service log.

    Parameters
    ----------
    level : str
        The log level ("INFO", "ERROR", etc.).
    message : str
        The message to log.
    """
    print(f"SERVICE_LOGGER_{level.upper()}: {message}")


def save_to_history(
        event_date: str,
        event_time: str,
        event: str,
        ) -> None:
    """
    Saves a fall event to the history file.

    Parameters
    ----------
    event_date : str
        The date of the event.
    event_time : str
        The time of the event.
    event : str
        The type of event (e.g., "fall_detected", "false_alarm").
    """
    history_file = Path(__file__).parent.parent / 'data' / 'history.json'
    history_data = []
    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        except Exception as e:
            log_file("ERROR", f"Error reading history file: {e}")
    new_entry = {
        "date": event_date,
        "time": event_time,
        "event": event
    }
    history_data.append(new_entry)
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        log_file("INFO", "Event saved to history.")
    except Exception as e:
        log_file("ERROR", f"Error writing to history file: {e}")


def launch_app():
    """
    Launches the main application.
    """
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        service = autoclass('org.kivy.android.PythonService').mService
        Intent = autoclass('android.content.Intent')

        intent = Intent(service, PythonActivity)

        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
        intent.putExtra("fall_detected", True)

        log_file("INFO", "Launching main application")
        service.startActivity(intent)
    except Exception as e:
        log_file("ERROR", f"Error launching main application: {e}")


class Alert:
    """
    Class to handle playing alert sounds using Android's MediaPlayer.

    Parameters
    ----------
    file_path : Path | str
        The file path to the alert sound file (wav)
    """
    def __init__(self, file_path: Path | str) -> None:
        # initialize MediaPlayer
        self.MediaPlayer = autoclass('android.media.MediaPlayer')
        self.AudioManager = autoclass('android.media.AudioManager')

        # set alarm volume to max
        Context = autoclass('android.content.Context')
        mService = autoclass('org.kivy.android.PythonService').mService
        self.audio_manager = mService.getSystemService(Context.AUDIO_SERVICE)
        max_volume = self.audio_manager.getStreamMaxVolume(
            self.AudioManager.STREAM_ALARM
            )
        self.audio_manager.setStreamVolume(
            self.AudioManager.STREAM_ALARM,
            max_volume,
            0
            )

        self.player = self.MediaPlayer()
        try:
            self.player.setDataSource(str(file_path))
            self.player.setAudioStreamType(self.AudioManager.STREAM_ALARM)
            self.player.prepare()
        except Exception as e:
            log_file("ERROR", f"Error initializing MediaPlayer: {e}")

    def play(self):
        if self.player is not None:
            max_vol = self.audio_manager.getStreamMaxVolume(
                self.AudioManager.STREAM_ALARM
                )
            self.audio_manager.setStreamVolume(
                self.AudioManager.STREAM_ALARM,
                max_vol,
                0
                )
            if not self.player.isPlaying():
                self.player.start()
                time.sleep(10)
                self.player.pause()
                self.player.seekTo(0)

    def stop(self):
        if self.player is not None:
            if self.player.isPlaying():
                self.player.pause()
                self.player.seekTo(0)

    def release(self):
        if self.player is not None:
            self.player.release()
            self.player = None
