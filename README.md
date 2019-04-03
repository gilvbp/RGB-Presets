# Lighting

Program to setup lighting presets in my computer. Controls Corsair iCUE keyboard, NZXT CAM CPU cooler, EVGA LED Sync GPU, and ASUS AURA.

## Setup
* run `git clone`
* run `npm install`
* follow instructions for installing and setting up [krakenx](https://github.com/KsenijaS/krakenx/)

## Running
* `lighting.py`: main file with presets
  * `python lighting.py <preset>`
* `aura.py`: controls ASUS AURA
  * `python aura.py <mode> [<RGB color>]`
* `led_sync.py`: controls EVGA LED Sync
  * `python led_sync.py <mode> [--color1 <RGB color> [--color2 <RGB color>]]`
* `keyboard.js`: controls [KeyboardAudioVisualizer](https://github.com/DarthAffe/KeyboardAudioVisualizer)
  * `node keyboard.js --foreground <RGB color>  --background <RGB color>`
* For CAM follow instructions on krakenx repo

## Info
### ASUS AURA
Settings are stored in a `LastProfile.xml` file in the `LightingService` folder. The `aura.py` script writes to this file and then restarts the `LightingService`, which updates the settings. Colors are stored as BGR -> hex -> decimal values. Color HSL values are also stored.
### EVGA LED Sync
Setting are stored in a `LedSync.cfg` file. Colors are stored as BGR -> hex -> decimal values.
### Keyboard Audio Visualiser
Settings are stored in a `Settings.json` file. Also uses [this AHK script](https://github.com/Drugoy/Autohotkey-scripts-.ahk/blob/master/Libraries/VA.ahk) to change audio outputs.
### CAM
Calls krakenx.