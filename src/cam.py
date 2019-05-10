from krakenx.color_change import KrakenX52

import usb.core

MODES = {
		'solid': KrakenX52.MODE_SOLID,
		'solidall': KrakenX52.MODE_SOLID_ALL,
		'breathing': KrakenX52.MODE_BREATHING,
		'pulse': KrakenX52.MODE_PULSE,
		'fading': KrakenX52.MODE_FADING,
		'marquee': KrakenX52.MODE_MARQUEE,
		'coveringmarquee': KrakenX52.MODE_COVERING_MARQUEE,
		'spectrumwave': KrakenX52.MODE_SPECTRUM_WAVE,
		'police': KrakenX52.MODE_POLICE,
		'spinner': KrakenX52.MODE_SPINNER,
		'chaser': KrakenX52.MODE_CHASER
}

def parse_color(color):
		if type(color) == list and len(color) == 3:
			color = tuple(int(c) for c in color)
		elif type(color) == list and len(color) == 1:
			color = tuple(int(c) for c in color[0].split(','))
		elif type(color) == str:
			color = tuple(int(c) for c in color.split(','))

		assert type(color) == tuple and len(color) == 3

		return color


def update_CAM(**kwargs):
	'''
	kwargs:
	mode
	text_color
	color0
	color1
	color2
	color3
	color4
	color5
	color6
	color7
	color_count
	aspeed
	fspeed
	pspeed
'''
	kwargs['mode'] = MODES[kwargs['mode'].lower()]

	if 'text_color' in kwargs:
		kwargs['text_color'] = parse_color(kwargs['text_color'])

	if 'color_count' in kwargs:
		for i in range(kwargs['color_count']):
			kwargs[f'color{i}'] = parse_color(kwargs[f'color{i}'])

	device = usb.core.find(idVendor=0x1e71, idProduct=0x170e)
	device.set_configuration()

	cooler = KrakenX52(device, **kwargs)
	cooler.update()
