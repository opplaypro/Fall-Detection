import time
from jnius import autoclass

print("### SERVICE STARTED ###")

PythonService = autoclass('org.kivy.android.PythonService')
service = PythonService.mService
service.setAutoRestartService(True)

while True:
    print("SERVICE RUNNING")
    time.sleep(1)
