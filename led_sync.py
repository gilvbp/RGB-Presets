from argparse import ArgumentParser
from collections import namedtuple

import re
import subprocess

LED_SYNC_PATH = r'C:\Program Files (x86)\EVGA\LED Sync'

Mode = namedtuple('Mode', ['name', 'index', 'color1', 'color2'])
MODES = {
  'S': Mode('StaticOn', 1, 4, None),
  'R': Mode('Rainbow', 2, None, None),
  'B': Mode('Breathing', 3, 8, 9),
  'P': Mode('Pulse', 4, 12, 13),
}

def kill_LED_Sync():
  subprocess.call(r'taskkill /IM "LEDSync.exe" /F /FI "Status eq RUNNING"')

def start_LED_Sync():
  subprocess.Popen([f'{LED_SYNC_PATH}\\LEDSync.exe', '/s'])

def update_LED_Sync(mode, color1=None, color2=None):
  kill_LED_Sync()

  mode = mode.upper()
  assert mode in MODES
  mode = MODES[mode]

  if color1:
    if type(color1) == list and len(color1) == 1:
      color1 = color1[0].split(',')
    elif type(color1) == str:
      color1 = color1.split(',')
  if color2:
    if type(color2) == list and len(color2) == 1:
      color2 = color2[0].split(',')
    elif type(color2) == str:
      color2 = color2.split(',')

  with open(f'{LED_SYNC_PATH}\\LedSync.cfg', 'r') as file:
    cfg = file.read().splitlines()

  cfg[2] = cfg[2][:-1] + str(mode.index)

  if mode.color1:
    assert type(color1) == list and len(color1) == 3
    color1 = list(map(int, color1))
    color1 = int('{:02x}{:02x}{:02x}'.format(*reversed(color1)), base=16)
    
    cfg[mode.color1] = re.sub(f'(?<==).*', str(color1), cfg[mode.color1])

  if mode.color2:
    assert type(color2) == list and len(color2) == 3
    color2 = list(map(int, color2))
    color2 = int('{:02x}{:02x}{:02x}'.format(*reversed(color2)), base=16)
    
    cfg[mode.color2] = re.sub(f'(?<==).*', str(color2), cfg[mode.color2])

  with open(f'{LED_SYNC_PATH}\\LedSync.cfg', 'w', encoding='utf8') as file:
    file.write('\n'.join(cfg))
  start_LED_Sync()

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('mode', help='LED SYNC lighting mode')
  parser.add_argument('-c1', '--color1', nargs='+', help='RGB color value as R G B or R,G,B')
  parser.add_argument('-c2', '--color2', nargs='+', help='RGB color value as R G B or R,G,B')
  ARGS = parser.parse_args()

  update_LED_Sync(ARGS.mode, ARGS.color1, ARGS.color2)