from collections import namedtuple

import re
import subprocess

import paths

Mode = namedtuple('Mode', ['name', 'index', 'color1', 'color2'])
MODES = {
  'STATIC': Mode('StaticOn', 1, 4, None),
  'RAINBOW': Mode('Rainbow', 2, None, None),
  'BREATHING': Mode('Breathing', 3, 8, 9),
  'PULSE': Mode('Pulse', 4, 12, 13),
}

def restart_LED_Sync():
  subprocess.call(r'taskkill /IM "LEDSync.exe" /F /FI "Status eq RUNNING"')
  subprocess.Popen([f'{paths.LED_SYNC}\\LEDSync.exe', '/s'])

def parse_color(color):
    if type(color) == list and len(color) == 1:
      color = color[0].split(',')
    elif type(color) == str:
      color = color.split(',')

    assert type(color) == list and len(color) == 3
    
    color = list(map(int, color))
    color = int('{:02x}{:02x}{:02x}'.format(*reversed(color)), base=16)

    return str(color)

def update_LED_Sync(mode, color1=None, color2=None):
  mode = mode.upper()
  assert mode in MODES
  mode = MODES[mode]

  with open(f'{paths.LED_SYNC}\\LedSync.cfg', 'r') as file:
    cfg = file.read().splitlines()

  cfg[2] = cfg[2][:-1] + str(mode.index)

  if mode.color1:
    cfg[mode.color1] = re.sub(f'(?<==).*', parse_color(color1), cfg[mode.color1])

  if mode.color2:
    cfg[mode.color2] = re.sub(f'(?<==).*', parse_color(color2), cfg[mode.color2])

  with open(f'{paths.LED_SYNC}\\LedSync.cfg', 'w', encoding='utf8') as file:
    file.write('\n'.join(cfg))
  restart_LED_Sync()

if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('mode', help='LED SYNC lighting mode')
  parser.add_argument('-c1', '--color1', nargs='+', help='RGB color value as R G B or R,G,B')
  parser.add_argument('-c2', '--color2', nargs='+', help='RGB color value as R G B or R,G,B')
  ARGS = parser.parse_args()

  update_LED_Sync(ARGS.mode, ARGS.color1, ARGS.color2)