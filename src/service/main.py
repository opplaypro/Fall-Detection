import time
from jnius import autoclass
import sys
import logging
import importlib.util
from oscpy.client import OSCClient
from pathlib import Path

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
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore
    return module


print("### SERVICE STARTED ###")

PythonService = autoclass('org.kivy.android.PythonService')
service = PythonService.mService
service.setAutoRestartService(True)

# import modules
try:
    main_path = Path(__file__).parent.parent
    path_sensors = main_path / 'core' / 'sensors.pyc'
    path_algorithm = main_path / 'core' / 'algorithm.pyc'

    sensors = load_module('sensors', str(path_sensors))
    algorithm = load_module('algorithm', str(path_algorithm))
    print("SERVICE_LOGGER_INFO: Modules loaded")
except Exception as e:
    print(f"SERVICE_LOGGER_ERROR: Error loading modules: {e}")
    sys.exit(-1)

# setup OSC client
client = OSCClient(HOST, PORT)
print("SERVICE_LOGGER_INFO: OSC Client initialized")

# setup sensors
Sensor = sensors.Sensor
detect_fall = algorithm.detect_fall

sensor = Sensor(frequency=SAMPLING_FREQ)
print("SERVICE_LOGGER_INFO: Sensor initialized")


while True:
    # main loop
    # uncomment for debugging, to see if service is running
    # print("SERVICE_LOGGER_DEBUG: Collecting sensor data")
    acc_data = sensor.get_accelerometer_data()
    gyro_data = sensor.get_gyroscope_data()
    fall_detected = detect_fall(
        accelerometer_data=acc_data,
        gyroscope_data=gyro_data,
        frequency=SAMPLING_FREQ
    )

    if fall_detected:
        # print("SERVICE_LOGGER_INFO: Fall detected, sending OSC message")
        try:
            client.send_message(
                b'/fall_detected', ['fall_detected'.encode('utf-8')]
                )
            print("SERVICE_LOGGER_INFO: OSC message sent, FALL DETECTED")
        except Exception as e:
            print(f"SERVICE_LOGGER_ERROR: Error sending OSC message: {e}")

    time.sleep(1 / CALL_FREQ)
