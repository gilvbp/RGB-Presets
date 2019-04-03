from collections import namedtuple

import colorsys
import subprocess
import time
import win32serviceutil
import xml.etree.ElementTree as ET

LIGHTING_SERVICE_PATH = r'C:\Program Files (x86)\LightingService'

Mode = namedtuple('Mode', ['key', 'uses_color'])
MODES = {
  'STATIC': Mode('1', True),
  'BREATHING': Mode('2', True),
  'COLOR_CYCLE': Mode('4', True),
  'RAINBOW': Mode('5', False),
  'COMET': Mode('8', True),
  'FLASH_AND_DASH': Mode('10', True),
  'WAVE': Mode('11', True),
  'GLOWING_YOYO': Mode('12', True),
  'STARRY_NIGHT': Mode('13', True),
  'STROBING': Mode('17', True),
  'SMART': Mode('18', False),
  'MUSIC': Mode('19', False),
}

def update_aura(mode, color=None):
  mode = mode.upper()
  assert mode in MODES
  mode = MODES[mode]
  
  profile = ET.parse(f'{LIGHTING_SERVICE_PATH}\\LastProfile.xml')
  root = profile.getroot()
  m = root.find('device[1]/scene[1]/mode')
  m.attrib['key'] = mode.key

  if color and mode.uses_color:
    if type(color) == list and len(color) == 1:
      color = color[0].split(',')
    elif type(color) == str:
      color = color.split(',')

    assert type(color) == list and len(color) == 3
    color = list(map(int, color))
    hue = f'{colorsys.rgb_to_hsv(*color)[0]:.6f}'
    color = str(int('{:02x}{:02x}{:02x}'.format(*reversed(color)), base=16))

    for led in m.findall('led'):
      led.find('color').text = color
      led.find('hue').text = hue

  if mode != MODES['RAINBOW']:
    m.find('color_type').text = 'Plain'
  else:
    # set to Gradient of the full range
    m.find('color_type').text = 'Gradient'
    m.find('start_end_color_cycle_start').text = '0'
    m.find('start_end_color_cycle_range').text = '.999'
    m.find('start_end_color_cycle_end').text = '.999'

  profile.write(f'{LIGHTING_SERVICE_PATH}\\LastProfile.xml', encoding='utf-8', xml_declaration=True)
  win32serviceutil.RestartService('LightingService')

if __name__ == '__main__':
  from argparse import ArgumentParser

  parser = ArgumentParser()
  parser.add_argument('mode', help='ASUS AURA lighting mode')
  parser.add_argument('color', nargs='*', help='RGB color value as R G B or R,G,B')
  ARGS = parser.parse_args()

  update_aura(ARGS.mode, ARGS.color)