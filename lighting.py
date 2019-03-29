from argparse import ArgumentParser

import aura
import subprocess

def setLighting(primary, accent, aura_mode='gy', cam_mode='CoveringMarquee'):
  aura.update_aura(aura_mode, primary)
  subprocess.call(f'node keyboard.js --bg {primary} --fg {accent}')
  subprocess.call('python C:/Users/Scott/AppData/Local/Programs/Python/Python37/Scripts/colctl.py ' \
    f'-m {cam_mode} -c0 {primary} -c1 {accent} -cc 2 ' \
    f'-c {primary} ' \
    '-as 1'
  )

def setRainbow():
  aura.update_aura('r')
  subprocess.call('node keyboard.js --r')
  subprocess.call('python C:/Users/Scott/AppData/Local/Programs/Python/Python37/Scripts/colctl.py ' \
    '-m SpectrumWave ' \
    '-as 2'
  )
  
# get args
parser = ArgumentParser()
parser.add_argument('preset', help='Lighting preset')
ARGS = parser.parse_args()
# set preset
{
  '1': lambda: setLighting('159,0,255', '0,142,255', 'gy', 'CoveringMarquee'),
  '2': lambda: setLighting('159,0,255', '0,142,255', 'gy', 'CoveringMarquee'),
  'r': lambda: setRainbow(),
}.get(ARGS.preset, lambda: print('No preset for ' + ARGS.preset))()