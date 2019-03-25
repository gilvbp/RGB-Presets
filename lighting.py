from argparse import ArgumentParser

import aura
'''
C:/Users/Scott/AppData/Local/Programs/Python/Python37/Scripts/colctl

(<temperature>, <speed>)
colctl --fan_speed "(20,25),(30,60),(40,90),(45,100)" --pump_speed "(20,60),(50,100)"

colctl -m CoveringMarquee -c0 159,0,255 -c1 0,142,255 -cc 2 -c 159,0,255 -as 1
'''

# get args
parser = ArgumentParser()
parser.add_argument('mode', help='ASUS AURA lighting mode')
parser.add_argument('color', nargs='*', help='RGB color value as R G B or R,G,B')
# parser.print_help()
ARGS = parser.parse_args()
ARGS.mode = ARGS.mode.upper()
if len(ARGS.color) == 1:
  ARGS.color = ARGS.color[0].split(',')

aura.update_aura(ARGS.mode, ARGS.color)