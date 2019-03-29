const argv = require('yargs').argv;
const fs = require('fs');

const util = require('util');
const exec = util.promisify(require('child_process').exec);

const SETTINGS_PATH = 'C:/Program Files/KeyboardAudioVisualizer/Settings.json';
const SET_SPEAKER_OUTPUT_AHK = 'C:/Projects/Lighting/SetSpeakerOutput.ahk';
const SET_HEADSET_OUTPUT_AHK = 'C:/Projects/Lighting/SetHeadsetOutput.ahk';

var settings = require(SETTINGS_PATH);

const RAINBOW_COLORS = {
  'Primary': [
    { 'R': 0, 'G': 255, 'B': 64 },
    { 'R': 128, 'G': 255, 'B': 0 },
    { 'R': 255, 'G': 192, 'B': 0 },
    { 'R': 255, 'G': 0, 'B': 0 },
    { 'R': 255, 'G': 0, 'B': 255 },
    { 'R': 0, 'G': 64, 'B': 255 },
    { 'R': 0, 'G': 255, 'B': 255 },
  ],
  'Background': [
    { 'R': 255, 'G': 0, 'B': 255 },
    { 'R': 0, 'G': 64, 'B': 255 },
    { 'R': 0, 'G': 255, 'B': 255 },
    { 'R': 0, 'G': 255, 'B': 64 },
    { 'R': 128, 'G': 255, 'B': 0 },
    { 'R': 255, 'G': 192, 'B': 0 },
    { 'R': 255, 'G': 0, 'B': 0 },
  ],
}

async function killVisualizer() {
  await exec('taskkill /IM "KeyboardAudioVisualizer.exe" /F /FI "Status eq RUNNING"');
}
async function startVisualizer() {
  await exec('START /D "C:/Program Files/KeyboardAudioVisualizer/" KeyboardAudioVisualizer.exe');
}

async function switchToSpeakers() {
  await exec(SET_SPEAKER_OUTPUT_AHK);
}
async function switchToHeadset() {
  await exec(SET_HEADSET_OUTPUT_AHK);
}

function setRainbow() {
  settings.Visualizations.Primary.Gradient.GradientStops.forEach((gradient, i) => {
    gradient.Color.R = RAINBOW_COLORS.Primary[i].R;
    gradient.Color.G = RAINBOW_COLORS.Primary[i].G;
    gradient.Color.B = RAINBOW_COLORS.Primary[i].B;
  });

  settings.Background.GradientStops.forEach((gradient, i) => {
    gradient.Color.R = RAINBOW_COLORS.Background[i].R;
    gradient.Color.G = RAINBOW_COLORS.Background[i].G;
    gradient.Color.B = RAINBOW_COLORS.Background[i].B;
  });
}

function setForeground(R, G, B) {
  settings.Visualizations.Primary.Gradient.GradientStops.forEach(gradient => {
    gradient.Color.R = R;
    gradient.Color.G = G;
    gradient.Color.B = B;
  });
}

function setBackground(R, G, B) {
  settings.Background.GradientStops.forEach(gradient => {
    gradient.Color.R = R;
    gradient.Color.G = G;
    gradient.Color.B = B;
  });
}

function saveSettings() {
  fs.writeFileSync(SETTINGS_PATH, JSON.stringify(settings));
}

function sleep(ms) {
  return new Promise(resolve => {
    setTimeout(resolve, ms);
  });
}

(async function() {
  killVisualizer();
  if(argv.rainbow || argv.r) {
    setRainbow()
  } else {
    let fg = argv.foreground || argv.fg;
    let bg = argv.background || argv.bg;
    setForeground(...fg.split(','));
    setBackground(...bg.split(','));
  }
  saveSettings();
  switchToSpeakers();
  startVisualizer();
  await sleep(500);
  switchToHeadset();
})()