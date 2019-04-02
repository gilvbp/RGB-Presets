from argparse import ArgumentParser
from pathlib import Path

import subprocess

import aura
import led_sync

COLCTL_PATH = str(Path.home()) + '/AppData/Local/Programs/Python/Python37/Scripts/colctl.py'

def set_lighting(primary, accent, aura_mode, cam_mode, led_sync_mode):
  aura.update_aura(aura_mode, primary)
  subprocess.call(f'node keyboard.js --bg {primary} --fg {accent}')
  subprocess.call(f'python {COLCTL_PATH} ' \
    f'-m {cam_mode} -c0 {primary} -c1 {accent} -cc 2 ' \
    f'-c {primary} ' \
    '-as 1'
  )
  led_sync.update_LED_Sync(led_sync_mode, primary, accent)

def set_rainbow():
  aura.update_aura('r')
  subprocess.call('node keyboard.js --r')
  subprocess.call(f'python {COLCTL_PATH} ' \
    '-m SpectrumWave ' \
    '-as 2'
  )
  led_sync.update_LED_Sync('r')
  
# get args
parser = ArgumentParser()
parser.add_argument('preset', help='Lighting preset')
ARGS = parser.parse_args()
# set preset
{
  'pb': lambda: set_lighting('159,0,255', '0,142,255', 'gy', 'CoveringMarquee', 'b'),
  'by': lambda: set_lighting('0,142,255', '255,255,0', 'sn', 'CoveringMarquee', 'b'),
  'w': lambda: set_lighting('255,255,255', '0,0,255', 'b', 'CoveringMarquee', 'b'),
  'bg': lambda: set_lighting('0,255,255', '0,255,0', 'gy', 'CoveringMarquee', 'b'),
  'rp': lambda: set_lighting('255,0,0', '150,0,255', 'sn', 'CoveringMarquee', 'b'),
  'dr': lambda: set_lighting('155,0,0', '72,0,155', 'sn', 'CoveringMarquee', 'b'),
  'r': lambda: set_rainbow(),
}.get(ARGS.preset, lambda: print('No preset for ' + ARGS.preset))()