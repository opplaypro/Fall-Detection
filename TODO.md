# TODO

## list of TODO things

- [x] core library
  - [x] accelerometer reading
  - [x] detection mechanism
    - [ ] ML
    - [x] g-force threshold
  - [x] background service handler

- [ ] UI
  - [x] home screen
  - [ ] UI manager
    - [ ] screen transitions
  - [ ] all other screens
    - [x] log history
    - [ ] settings
    - [ ] contacts
  - [x] alert (when detected)

- [ ] main.py
- [ ] app info in buildozer.spec
- [x] file logging

- [ ] assets
  - [ ] translations (one or two)
    - [ ] polish
    - [ ] english ← main focus
  - [ ] icons and images

## List of things do decite

- ML vs threshold

## Current APP state

- app reads accelerometer and gyroscope, then changes screen color based on values of an accelerometer
- changes to green if a threshold of 30m/s2 is detected
- all screens are a copy of main, when switched to, they break whole app (accelerometer part)

## rewrite TODO (later)

- [x] core.log: logging will be run before anything else, before creating app
- [ ] changeable `SAMPLING_FREQ` inside service.py
- [ ] encrypt user data in `history.json` (if implemented `contacts.json` too)
