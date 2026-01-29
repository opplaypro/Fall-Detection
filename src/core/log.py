import logging
from pathlib import Path
from datetime import datetime

import kivy


class LevelFormatter(logging.Formatter):
    """
    Custom logging formatter with fixed column widths.
    """
    def format(self, record):
        # format time
        time_str = self.formatTime(record, "%Y-%m-%d %H:%M:%S")

        # format level name to fixed width of 8 characters
        level_str = f"{record.levelname:<8}"

        # format module and line number
        if record.levelno in [logging.DEBUG, logging.ERROR, logging.CRITICAL]:
            location = f"{record.module}:{record.lineno}"
        else:
            location = ""
        location_str = f"{location:<25}"

        # combine all parts into one line
        fmt = f"{time_str} | {level_str} | {location_str} | "
        message = record.getMessage()
        return fmt + message


def setup_logging(App) -> None:
    """
    Sets up logging configuration. Creates a logs directory,
    renames the existing latest.log file and initializes a new latest.log
    file with the current date and time.
    """
    if kivy.platform == 'linux':
        user_data = Path(__file__).parent.parent
    else:
        user_data = Path(App.get_running_app().user_data_dir)  # type: ignore

    log_directory = user_data / 'logs'
    log_directory.mkdir(parents=True, exist_ok=True)
    latest_log = log_directory / 'latest.log'

    if latest_log.exists():
        try:
            # remove old log file if exists (max 10 files)
            log_files = sorted(log_directory.glob('log_*.log'))
            while len(log_files) >= 10:
                log_files[0].unlink()
                log_files.pop(0)
            date = latest_log.read_text().splitlines()[0]
            old_date = date.replace(' ', '_').replace(':', '_')
            latest_log.rename(log_directory / f'log_{old_date}.log')
        except Exception as e:
            print(f"Error renaming log file: {e}")
    current_time = datetime.now().strftime('%Y_%m_%d %H_%M_%S')
    latest_log.write_text(current_time + '\n', encoding='utf-8')

    # Create a file handler for logging
    file_handler = logging.FileHandler(
        latest_log, mode='a', encoding='utf-8')
    file_handler.setFormatter(LevelFormatter())

    # Add the handler to the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.NOTSET)
    root_logger.addHandler(file_handler)
