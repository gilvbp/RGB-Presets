from pathlib import Path

import json
import subprocess

from src import aura
from src import kracken
from src import led_sync
from src import keyboard
from src import paths

def set_rgb(**kwargs):
	primary = kwargs.get('primary')
	accent = kwargs.get('accent')

	# call rgb updates
	aura.update_aura(kwargs.get('aura_mode'), primary)
	led_sync.update_LED_Sync(kwargs.get('led_sync_mode'), primary, accent, kwargs.get('led_sync_speed'))

	if kwargs.get('kb_mode', '').lower() == 'rainbow':
		keyboard.update_kb()
	else:
		keyboard.update_kb(primary, accent)

	kracken_args = {
		'mode': kwargs.get('kracken_mode'),
		'aspeed': kwargs.get('kracken_speed'),
		'fspeed': kwargs.get('kracken_fan_curve', [(20,25), (30,60), (40,90), (45,100)]),
		'pspeed': kwargs.get('kracken_pump_curve', [(20,60), (50,100)])
	}

	if primary:
		kracken_args = { **kracken_args, **{
				'color0': primary,
				'color1': accent,
				'color_count': 2,
				'text_color': primary
			}
		}

	kracken.update_kracken(**kracken_args)


def update_rgb(preset_name):
	with open(f'{paths.SRC_DIR}\\..\\presets.json', 'r') as f:
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
	parser.add_argument('-p', '--preset', help='RGB preset')
	parser.add_argument('-pc', '--primary', nargs='+', help='RGB primary color as R,G,B or R G B')
	parser.add_argument('-ac', '--accent', nargs='+', help='RGB accent color as R,G,B or R G B')
	parser.add_argument('-am', '--aura_mode', nargs='+', help='ASUS AURA lighting mode')
	parser.add_argument('-cm', '--kracken_mode', nargs='+', help='NZXT Kracken lighting mode')
	parser.add_argument('-lm', '--led_sync_mode', nargs='+', help='EVGA LED Sync lighting mode')
	parser.add_argument('-cs', '--kracken_speed', nargs='+', help='NZXT Kracken lighting animation speed')
	parser.add_argument('-ls', '--led_sync_speed', nargs='+', help='EVGA LED Sync lighting animation speed')
	args = parser.parse_args()

	with open(f'{paths.SRC_DIR}\\..\\presets.json', 'r') as f:
		presets = json.load(f)

	if args.preset:
		if args.preset in presets:
			set_rgb(**{**presets['default_values'], **presets.get(args.preset)})
		else:
			presets_list = ''
			for p in presets.keys():
				if p != 'default_values':
					presets_list += '\n\t' + p

			print(f'No preset for {args.preset}, must be one of:{presets_list}')
	else:
		set_rgb(**{**presets['default_values'], **args})