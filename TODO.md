# TODO

## list of TODO things

- [x] core library
  - [x] accelerometer reading
  - [x] detection mechanism
    - [x] g-force threshold
  - [x] background service handler

- [x] UI
  - [x] home screen
  - [ ] UI manager
    - [ ] screen transitions
  - [x] all other screens
    - [x] log history
    - [x] settings
  - [x] alert (when detected)

- [x] main.py
- [x] app info in buildozer.spec
- [x] file logging

- [ ] assets
  - [ ] translations (one or two)
    - [ ] polish
    - [x] english ← main focus
    - [x] config
  - [x] icons and images

## TODO part two

- [ ] ui.screens.contacts
- [ ] core.algorithm.ML

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
