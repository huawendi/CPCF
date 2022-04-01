import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FuncFormatter

bit_and: list = [
	1.915, 1.908, 1.932, 1.901, 1.928, 1.918, 1.894, 1.92, 1.928, 1.941
]

bit_move: list = [
	2.035, 2.031, 2.185, 2.058, 2.036, 2.12, 2.071, 2.054, 2.031, 2.165
]

num_mod: list = [
	2.301, 2.285, 2.305, 2.306, 2.309, 2.316, 2.319, 2.294, 2.275, 2.295
]


def x_update_scale_value(temp, position) -> str:
	result = int(temp) + 21
	return r'2$^{%s}$' % result


if __name__ == '__main__':
	x: np.ndarray = np.arange(10)

	total_width, n = 0.8, 3
	width = total_width / n
	x = x - (total_width - width) / 2

	plt.figure(figsize=(3.5, 2))
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	plt.bar(x, bit_and, width=width, color='#0088ff', edgecolor='black', label='and')
	plt.bar(x + width, num_mod, width=width, color='#94cc94', edgecolor='black', label='mod')
	plt.bar(x + 2 * width, bit_move, width=width, color='#fdc897', edgecolor='black', label='shift')

	major_locator = MultipleLocator(1)
	plt.gca().yaxis.set_major_locator(major_locator)
	plt.gca().xaxis.set_major_locator(major_locator)
	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))

	plt.tick_params(direction='in')
	plt.tick_params(axis='x', length=0)

	plt.ylim(0.8, 3.2)

	plt.xlabel('Mapping range')
	plt.ylabel('Time (' + chr(956) + 's)')
	plt.legend(ncol=3)

	plt.savefig('speed.tiff', format='tiff', dpi=300, bbox_inches='tight')

	plt.show()
