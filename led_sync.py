from collections import namedtuple

import re
import subprocess

import paths

Mode = namedtuple('Mode', ['name', 'index', 'color1', 'color2', 'speed'])
MODES = {
  'STATIC': Mode('StaticOn', 0, 4, None, None),
  'RAINBOW': Mode('Rainbow', 2, None, None, 6),
  'BREATHING': Mode('Breathing', 3, 8, 9, 10),
  'PULSE': Mode('Pulse', 4, 12, 13, 14),
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

def update_LED_Sync(mode, color1=None, color2=None, speed=None):
  mode = mode.upper()
  assert mode in MODES
  mode = MODES[mode]

  with open(f'{paths.LED_SYNC}\\LedSync.cfg', 'r') as file:
    cfg = file.read().splitlines()

  cfg[2] = cfg[2][:-1] + str(mode.index)

  if mode.color1 and color1:
    cfg[mode.color1] = re.sub(f'(?<==).*', parse_color(color1), cfg[mode.color1])

  if mode.color2 and color2:
    cfg[mode.color2] = re.sub(f'(?<==).*', parse_color(color2), cfg[mode.color2])

  if mode.speed and speed:
    cfg[mode.speed] = re.sub(f'(?<==).*', str(speed), cfg[mode.speed])

  with open(f'{paths.LED_SYNC}\\LedSync.cfg', 'w', encoding='utf8') as file:
    file.write('\n'.join(cfg))
  restart_LED_Sync()

if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('mode', help='LED SYNC lighting mode')
  parser.add_argument('-c1', '--color1', nargs='+', help='RGB color value as R G B or R,G,B')
  parser.add_argument('-c2', '--color2', nargs='+', help='RGB color value as R G B or R,G,B')
  parser.add_argument('-s', '--speed', help='LED SYNC animation speed [0-5]')
  args = parser.parse_args()

  update_LED_Sync(args.mode, args.color1, args.color2, args.speed)