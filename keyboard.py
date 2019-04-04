import json
import os
import subprocess
import time

KBAV_PATH = r'C:/Program Files/KeyboardAudioVisualizer'
DIR = os.path.dirname(os.path.realpath(__file__))
RAINBOW_COLORS = {
	'Primary': [
		(0, 255, 64),
		(128, 255, 0),
		(255, 192, 0),
		(255, 0, 0),
		(255, 0, 255),
		(0, 64, 255),
		(0, 255, 255),
	],
	'Background': [
		(255, 0, 255),
		(0, 64, 255),
		(0, 255, 255),
		(0, 255, 64),
		(128, 255, 0),
		(255, 192, 0),
		(255, 0, 0),
	],
}

def startVisualizer():
	os.startfile(f'{DIR}\\KBAV.lnk')

def killVisualizer():
	subprocess.call(r'taskkill /IM "KeyboardAudioVisualizer.exe" /F /FI "Status eq RUNNING"')

def switchToSpeakers():
	subprocess.call(f'{DIR}\\AHK\\SetSpeakerOutput.ahk', shell=True)

def switchToHeadset():
	subprocess.call(f'{DIR}\\AHK\\SetHeadsetOutput.ahk', shell=True)

def setRainbow(settings):
	for (i, grad) in enumerate(settings['Visualizations']['Primary']['Gradient']['GradientStops']):
		grad['Color']['R'] = RAINBOW_COLORS['Primary'][i][0]
		grad['Color']['G'] = RAINBOW_COLORS['Primary'][i][1]
		grad['Color']['B'] = RAINBOW_COLORS['Primary'][i][2]

	for (i, grad) in enumerate(settings['Background']['GradientStops']):
		grad['Color']['R'] = RAINBOW_COLORS['Background'][i][0]
		grad['Color']['G'] = RAINBOW_COLORS['Background'][i][1]
		grad['Color']['B'] = RAINBOW_COLORS['Background'][i][2]

def setForeground(settings, R, G, B):
	for grad in settings['Visualizations']['Primary']['Gradient']['GradientStops']:
		grad['Color']['R'] = R
		grad['Color']['G'] = G
		grad['Color']['B'] = B

def setBackground(settings, R, G, B):
	for grad in settings['Background']['GradientStops']:
		grad['Color']['R'] = R
		grad['Color']['G'] = G
		grad['Color']['B'] = B

def parse_color(color):
		if type(color) == list and len(color) == 1:
			color = color[0].split(',')
		elif type(color) == str:
			color = color.split(',')

		assert type(color) == list and len(color) == 3
		
		return list(map(int, color))

def update_kb(bg=None, fg=None):
	with open(f'{KBAV_PATH}\\Settings.json', 'r') as f:
		settings = json.load(f)

	if fg and bg:
		setForeground(settings, *parse_color(fg))
		setBackground(settings, *parse_color(bg))
	else:
		setRainbow(settings)

	with open(f'{KBAV_PATH}\\Settings.json', 'w') as f:
		json.dump(settings, f)
	
	killVisualizer()
	switchToSpeakers()
	startVisualizer()
	time.sleep(.4)
	switchToHeadset()

if __name__ == '__main__':
	from argparse import ArgumentParser

	parser = ArgumentParser()
	parser.add_argument('-bg', '--background', nargs='+', \
		help='RGB background color as R,G,B or R G B, leave blank for rainbow mode')
	parser.add_argument('-fg', '--foreground', nargs='+',	\
		help='RGB foreground color as R,G,B or R G B, leave blank for rainbow mode')
	args = parser.parse_args()

	update_kb(args.background, args.foreground)