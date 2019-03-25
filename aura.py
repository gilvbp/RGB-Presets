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

# primary color: 159, 0, 255
# primary color: 0, 142, 255

def selectMode(mode):
  pyautogui.moveTo(AURA_L + 100, AURA_T + 215 + 38 * MODES[mode])
  pyautogui.click()

def setColor(mode, r='0', g='0', b='0'):
  if mode in ['COLOR_CYCLE', 'CC', 'RAINBOW', 'R']:
    return
  
  w = 133 if MODES[mode] > 1 else 377
  pyautogui.moveTo(SCREEN_W / 2 + w, SCREEN_H / 2 - 37)
  pyautogui.doubleClick()
  pyautogui.typewrite(r)
  pyautogui.moveRel(None, 39)
  pyautogui.doubleClick()
  pyautogui.typewrite(g)
  pyautogui.moveRel(None, 39)
  pyautogui.doubleClick()
  pyautogui.typewrite(b)

def apply():
  pyautogui.moveTo(AURA_R - 90, AURA_B - 40)
  pyautogui.click()

def update_aura(mode, color):
  subprocess.Popen(AURA_PATH)
  time.sleep(.5)
  selectMode(mode)
  if color:
    setColor(mode, *color)
  apply()
  time.sleep(1.5)
  pyautogui.hotkey('alt', 'f4')