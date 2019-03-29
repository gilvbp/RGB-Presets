# Lighting

Program to setup lighting presets in my computer. Controls Corsair iCUE keyboard, NZXT CAM CPU cooler, and ASUS AURA.

Relevant links:
 * https://github.com/KsenijaS/krakenx/
 * https://github.com/DarthAffe/KeyboardAudioVisualizer
 * https://github.com/Drugoy/Autohotkey-scripts-.ahk/blob/master/Libraries/VA.ahk

## Setup
* run `git clone`
* run `npm i`
* follow instructions for installing and setting up krakenx

## Running
* `lighting.py`: main file with presets
  * `python lighting.py <preset>`
* `aura.py`: controls ASUS AURA
  * `python aura.py <mode> [<RGB color>]`
* `keyboard.js`: controls KeyboardAudioVisualizer
  * `node keyboard.js --foreground <RGB color>  --background <RGB color>`
* For CAM follow instructions on krakenx repo