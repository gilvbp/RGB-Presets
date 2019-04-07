# RGB Presets

Program to setup lighting presets in my computer. Controls Corsair iCUE keyboard, NZXT CAM CPU cooler, EVGA LED Sync GPU, and ASUS AURA.

## Requirements
* [AutoHotkey](https://www.autohotkey.com/)
* [krakenx](https://github.com/KsenijaS/krakenx/)
* [KeyboardAudioVisualizer](https://github.com/DarthAffe/KeyboardAudioVisualizer)

## Setup
* run `git clone`
* run `npm install`
* add a shortcut that runs KeyboardAudioVisualizer as administrator to the project directory named `KBAV.lnk`
* make sure the paths in `paths.py` work for your system
* add presets to `presets.json`

## Running
* `rgb_presets.py`: main file with presets
  * `python rgb_presets.py <preset>`
* `aura.py`: controls ASUS AURA
  * `python aura.py <mode> [<RGB color>]`
* `led_sync.py`: controls EVGA LED Sync
  * `python led_sync.py <mode> [--color1 <RGB color>] [--color2 <RGB color>] [--speed <0-5>]`
* `keyboard.py`: controls KeyboardAudioVisualizer
  * `python keyboard.py --foreground <RGB color>  --background <RGB color>`
* For CAM follow instructions on krakenx repo

## Info
### ASUS AURA
Settings are stored in `LastProfile.xml` in the `LightingService` folder. The `aura.py` script writes to this file and then restarts the `LightingService`, which updates the settings. Colors are stored as BGR -> hex -> decimal values. Color HSL values are also stored.
### EVGA LED Sync
Setting are stored in `LedSync.cfg`. Colors are stored as BGR -> hex -> decimal values.
### Keyboard Audio Visualiser
Settings are stored in `Settings.json`. Also uses [VA.ahk](https://github.com/Drugoy/Autohotkey-scripts-.ahk/blob/master/Libraries/VA.ahk) to change audio outputs.

I set up my music to always come through my speakers (even if my headset is the default device), but KBAV samples the sound from the default device. The script will check if my headset is the current output device and quickly switch to speaker output when it starts KBAV (so the visualization appears for the music) and then switch it back.
### CAM
Calls krakenx.