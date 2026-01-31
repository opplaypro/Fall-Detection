from jnius import autoclass
from pathlib import Path
import time


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

        print("SERVICE_LOGGER_INFO: Launching main application")
        service.startActivity(intent)
    except Exception as e:
        print(f"SERVICE_LOGGER_ERROR: Error launching main application: {e}")


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
            print(f"SERVICE_LOGGER_ERROR: Error initializing MediaPlayer: {e}")

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
