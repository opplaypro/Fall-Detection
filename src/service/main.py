import time
from jnius import autoclass
import sys
import importlib.util
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from pathlib import Path
import json

# ---------------------
# --- CONFIGURATION ---
# ---------------------

HOST = '127.0.0.1'
PORT = 3000
SAMPLING_FREQ = 50
CALL_FREQ = 5


def load_module(module_name, module_path):
    """
    Dynamically loads a module from the given file path.

    Parameters
    ----------
    module_name : str
        The name to assign to the loaded module.
    module_path : str
        The file path to the module to load.

    Returns
    -------
    module
        The loaded module.
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore
    return module


print("### SERVICE STARTED ###")

# set up Android service
PythonService = autoclass('org.kivy.android.PythonService')
service = PythonService.mService
service.setAutoRestartService(True)

# import modules
try:
    # get paths to modules
    main_path = Path(__file__).parent.parent

    path_sensors = main_path / 'core' / 'sensors.pyc'
    path_algorithm = main_path / 'core' / 'algorithm.pyc'
    path_notifier = main_path / 'core' / 'notifier.pyc'
    path_config = main_path / 'config' / 'config.json'

    # load modules
    sensors = load_module('sensors', str(path_sensors))
    algorithm = load_module('algorithm', str(path_algorithm))
    notifier = load_module('notifier', str(path_notifier))
    print("SERVICE_LOGGER_INFO: Modules loaded")
except Exception as e:
    print(f"SERVICE_LOGGER_ERROR: Error loading modules: {e}")
    sys.exit(-1)


# setup notifier
launch_app = notifier.launch_app
Alert = notifier.Alert
save_to_history = notifier.save_to_history
# send_message = notifier.send_message

alert = Alert(
    file_path=main_path / 'assets' / 'audio' / '300.wav'
    )


def stop_callback(*args):
    print("SERVICE_LOGGER_INFO: Stop signal received, stopping service")
    alert.stop()


# load if enabled config
with open(path_config, 'r') as f:
    config = json.load(f)
open_app_enabled = config.get('settings', {}).get('open_app', False)
detect_enabled = config.get('settings', {}).get('fall_detection', True)
alert_enabled = config.get('settings', {}).get('play_alert', False)
message_enabled = config.get('settings', {}).get('send_message', False)
fall_log_path = config.get('fall_log', {}).get('file', 'data/history.json')

# setup OSC client and seerver
client = OSCClient(HOST, PORT)
print("SERVICE_LOGGER_INFO: OSC Client initialized")
osc_server = OSCThreadServer()
osc_server.listen(address=HOST, port=PORT+1, default=True)
osc_server.bind(b"/stop_alert", alert.stop)

# setup sensors
Sensor = sensors.Sensor
detect_fall = algorithm.detect_fall

sensor = Sensor(frequency=SAMPLING_FREQ)
print("SERVICE_LOGGER_INFO: Sensor initialized")


last_detect = False
while True:
    # main loop
    # uncomment for debugging, to see if service is running
    # print("SERVICE_LOGGER_DEBUG: Collecting sensor data")
    # update config
    with open(path_config, 'r') as f:
        config = json.load(f)
    detect_enabled = config.get('settings', {}).get('fall_detection', True)
    open_app_enabled = config.get('settings', {}).get('open_app', False)
    alert_enabled = config.get('settings', {}).get('play_alert', False)
    message_enabled = config.get('settings', {}).get('send_message', False)

    if not detect_enabled:
        time.sleep(10.0 / CALL_FREQ)
        continue
    # get sensor data and detect fall
    acc_data = sensor.get_accelerometer_data()
    gyro_data = sensor.get_gyroscope_data()
    fall_detected = detect_fall(
        accelerometer_data=acc_data,
        gyroscope_data=gyro_data,
        frequency=SAMPLING_FREQ
    )

    # send OSC message if fall detected
    if fall_detected and last_detect is False:
        # print("SERVICE_LOGGER_INFO: Fall detected, sending OSC message")
        try:
            client.send_message(
                b'/fall_detected', ['fall_detected'.encode('utf-8')]
            )
            last_detect = True
            save_to_history(
                event_date=time.strftime("%Y-%m-%d"),
                event_time=time.strftime("%H:%M:%S"),
                event="fall_detected",
                )
            if open_app_enabled:
                launch_app()  # launch main app
            if alert_enabled:
                alert.play()  # play alert sound
            print("SERVICE_LOGGER_INFO: OSC message sent, FALL DETECTED")

        except Exception as e:
            print(f"SERVICE_LOGGER_ERROR: Error sending OSC message: {e}")

    if not fall_detected:
        last_detect = False
    else:
        last_detect = True
    time.sleep(1.0 / CALL_FREQ)

alert.release()
print("### SERVICE STOPPED ###")
