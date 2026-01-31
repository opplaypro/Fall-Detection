# Fall Detection

Mobile app that detects when user falls and sends an alert/

---

## Features

- works fully in background (even when app is closed)
- when fall is detected, plays loud sound adn displays a screen, where user can say it was a false alarm (if it was)
- history of detected falls

---

## Settings in-app

- Fall detection - should fall detection work (default: true)
- Open App - should app be opened when fall is  detected. If fall is detected and this is false, you cannot cancel the alarm (default: true, recommended: true)
- Play Alert - shoud app play a loud alert when fall is detected

### Installation

To install app on your phone, download .apk file for your architecture and install\
If asks to install from unknown sources, agree\

#### Build it yourself

Download all files
to build app for android, you need a linux, for iOS, you need macOS

clone repository and change branch

```bash
git clone https://github.com/opplaypro/Fall-Detection.git
cd FallDetection
git checkout develompent
```

create virtual environment and install required dependencies (e.g. with uv)

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

to create a debugging apk, connect your to your phone with adb and run

```bash
buildozer android debug deploy run
```

#### Run on desktop

Do all steps as mentioned [earlier](#build-it-yourself) except running `buildozer`
then simply run

```bash
python3 src/main.py
```
