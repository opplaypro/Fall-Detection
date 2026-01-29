import time
import importlib.util
import sys
from oscpy.client import OSCClient
from pathlib import Path

# Configuration
HOST = '127.0.0.1'
PORT = 3000
SAMPLING_FREQ = 10


def load_module(module_name, module_path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)  # type: ignore
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore
    return module


if __name__ == '__main__':
    osc = OSCClient(HOST, PORT)
    print(f"Connecting to OSC server at {HOST}:{PORT}")

    try:
        service_path = Path(__file__).parent.resolve()
        path_sensors = service_path / 'sensors.py'
        path_algorithm = service_path / 'algorithm.py'
        sensors = load_module('sensors', str(path_sensors))
        algorithm = load_module('algorithm', str(path_algorithm))
        print("Modules loaded successfully.")
        Sensor = sensors.Sensor
        sensor = Sensor()
        detect_fall = algorithm.detect_fall
    except Exception as e:
        print(f"Error loading modules: {e}")
        sys.exit(1)

    while True:
        try:
            accel_data = sensor.get_accelerometer_data()
            gyro_data = sensor.get_gyroscope_data()
            frequency = sensor.get_sampling_frequency()

            fall_detected = detect_fall(
                accelerometer_data=accel_data,
                gyroscope_data=gyro_data,
                frequency=frequency
            )

            if fall_detected:
                print("Fall detected! Sending OSC message.")
                osc.send_message(b'/update', [True])
            else:
                print("No fall detected.")

            time.sleep(1/SAMPLING_FREQ)
        except Exception as e:
            osc.send_message(b'/error', [str(e).encode('utf-8')])
            print(f"Error during fall detection loop: {e}")
            time.sleep(1/SAMPLING_FREQ)
