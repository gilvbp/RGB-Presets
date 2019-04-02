from argparse import ArgumentParser

import pyautogui
import subprocess
import time

AURA_PATH = r'C:\Program Files (x86)\ASUS\AURA\Aura.exe'
SCREEN_W, SCREEN_H = pyautogui.size()
AURA_T = SCREEN_H / 2 - 371
AURA_B = SCREEN_H / 2 + 330
AURA_L = SCREEN_W / 2 - 450
AURA_R = SCREEN_W / 2 + 451

MODES = {
  'STATIC': 0,
  'S': 0,
  'BREATHING': 1,
  'B': 1,
  'COLOR_CYCLE': 2,
  'CC': 2,
  'RAINBOW': 3,
  'R': 3,
  'COMET': 4,
  'C': 4,
  'FLASH_AND_DASH': 5,
  'FD': 5,
  'WAVE': 6,
  'W': 6,
  'GLOWING_YOYO': 7,
  'GY': 7,
  'STARRY_NIGHT': 8,
  'SN': 8,
  'STROBING': 9,
  'SB': 9,
}

def select_mode(mode):
  pyautogui.moveTo(AURA_L + 100, AURA_T + 215 + 38 * MODES[mode])
  pyautogui.click()

  if mode in {'RAINBOW', 'R'}:
    pyautogui.moveTo(SCREEN_W / 2, SCREEN_H / 2 - 130)
    pyautogui.click()
    pyautogui.moveRel(None, 60)
    pyautogui.click()

def set_color(mode, r, g, b):
  w = 133 if MODES[mode] > 1 else 377
  pyautogui.moveTo(SCREEN_W / 2 + w, SCREEN_H / 2 - 37)
  pyautogui.doubleClick()
  pyautogui.typewrite(str(r))
  pyautogui.moveRel(None, 39)
  pyautogui.doubleClick()
  pyautogui.typewrite(str(g))
  pyautogui.moveRel(None, 39)
  pyautogui.doubleClick()
  pyautogui.typewrite(str(b))

def apply():
  pyautogui.moveTo(AURA_R - 90, AURA_B - 40)
  pyautogui.click()

def update_aura(mode, color=None):
  subprocess.Popen(AURA_PATH)
  time.sleep(.5)

  mode = mode.upper()
  assert mode in MODES
  select_mode(mode)

  if color:
    if type(color) == list and len(color) == 1:
      color = color[0].split(',')
    elif type(color) == str:
      color = color.split(',')
    assert type(color) == list and len(color) == 3
    set_color(mode, *color)

  apply()
  time.sleep(1.5)
  pyautogui.hotkey('alt', 'f4')

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('mode', help='ASUS AURA lighting mode')
  parser.add_argument('color', nargs='*', help='RGB color value as R G B or R,G,B')
  ARGS = parser.parse_args()

  update_aura(ARGS.mode, ARGS.color)