from pathlib import Path

import json
import subprocess

import aura
import led_sync
import keyboard
import paths


def set_lighting(**kwargs):
  aura.update_aura(kwargs['aura_mode'], kwargs['primary'])
  led_sync.update_LED_Sync(kwargs['led_sync_mode'], kwargs['primary'], kwargs['accent'])
  keyboard.update_kb(kwargs['primary'], kwargs['accent'])
  subprocess.call(f'python {paths.COLCTL} ' \
    f"-m {kwargs['cam_mode']} -c0 {kwargs['primary']} -c1 {kwargs['accent']} -cc 2 " \
    f"-c {kwargs['primary']} " \
    '-as 1'
  )

def set_rainbow():
  aura.update_aura('rainbow')
  led_sync.update_LED_Sync('rainbow')
  keyboard.update_kb()
  subprocess.call(f'python {paths.COLCTL} ' \
    '-m SpectrumWave ' \
    '-as 2'
  )

def update_lighting(preset):
  with open('presets.json', 'r') as f:
    preset = json.load(f).get(preset)
  
  if preset:
    if preset.get('rainbow'):
      set_rainbow()
    else:
      set_lighting(**preset)
  else:
    print('No preset found')


if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('preset', help='Lighting preset')
  args = parser.parse_args()

  update_lighting(args.preset)