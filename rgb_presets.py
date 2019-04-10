from pathlib import Path

import json
import subprocess

import aura
import led_sync
import keyboard
import paths


def set_rgb(**kwargs):
  primary = kwargs.get('primary')
  accent = kwargs.get('accent')

  # call rgb updates
  aura.update_aura(kwargs.get('aura_mode'), primary)
  led_sync.update_LED_Sync(kwargs.get('led_sync_mode'), primary, accent, kwargs.get('led_sync_speed'))
  keyboard.update_kb(primary, accent)
  cam = f"python {paths.COLCTL} -m {kwargs.get('cam_mode')} -as {kwargs.get('cam_speed')} "
  if primary:
    cam += f"-c0 {primary} -c1 {accent} -cc 2 -c {primary} "
  subprocess.call(cam)

  # save profile for cam startup
  cam += '--fan_speed "(20,25),(30,60),(40,90),(45,100)" ' \
    '--pump_speed "(20,60),(50,100)" '
  with open('CAM Startup.bat', 'w') as f:
    f.write(cam)


def update_rgb(preset_name):
  with open(f'{paths.CURR_DIR}\\presets.json', 'r') as f:
    presets = json.load(f)
    
  if preset_name in presets:
    set_rgb(**{**presets['default_values'], **presets.get(preset_name)})
  else:
    presets_list = ''
    for p in presets.keys():
      if p != 'default_values':
        presets_list += '\n\t' + p
    
    print(f'No preset for {preset_name}, must be one of:{presets_list}')


if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('preset', help='RGB preset')
  args = parser.parse_args()

  update_rgb(args.preset)