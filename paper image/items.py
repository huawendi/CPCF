import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def x_update_scale_value(temp, position) -> str:
	return r'2$^{%s}$' % int(temp)


CF: dict = {
	'insert': [
		16.33, 15.70, 15.47, 12.59, 8.31, 6.61, 5.80, 5.46
	],
	'delete': [
		29.91, 29.30, 29.35, 23.15, 15.81, 13.75, 13.04, 12.17
	],
}

SSCF: dict = {
	'insert': [
		9.55, 8.91, 8.69, 7.39, 5.21, 4.25, 3.82, 3.56
	],
	'delete': [
		17.64, 15.84, 14.94, 12.51, 8.77, 7.21, 6.59, 6.16
	],
}

BCF: dict = {
	'insert': [
		17.62, 17.46, 18.34, 12.97, 7.45, 5.76, 5.10, 4.69
	],
	'delete': [
		31.42, 31.44, 31.73, 25.17, 17.49, 15.24, 14.30, 13.72
	],
}

VF: dict = {
	'insert': [
		19.16, 18.97, 19.50, 17.32, 12.13, 10.25, 9.41, 8.77
	],
	'delete': [
		30.29, 29.76, 29.59, 24.90, 17.33, 15.06, 14.36, 13.56
	],
}

CGCF: dict = {
	'insert': [
		23.68, 23.03, 23.79, 19.95, 13.70, 11.37, 10.34, 9.83
	],
	'delete': [
		30.83, 30.96, 30.63, 25.36, 17.69, 15.45, 14.32, 14.07
	],
}

CGCF_HP: dict = {
	'insert': [
		24.12, 23.27, 23.98, 24.23, 14.95, 12.62, 11.69, 11.47
	],
	'delete': [
		32.62, 32.54, 32.47, 32.42, 19.53, 16.90, 16.50, 16.42
	],
}

if __name__ == '__main__':
	plt.figure(figsize=(8.3, 2.5))
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	items = np.linspace(20, 27, 8)

	plt.subplot(1, 2, 1)
	plt.plot(items, CF['insert'], 'v-', color='#0072bd', label='CF')
	plt.plot(items, SSCF['insert'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(items, BCF['insert'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(items, VF['insert'], '*-', color='#3d9140', label='VF')
	plt.plot(items, CGCF['insert'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(items, CGCF_HP['insert'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel(r'Number of elements ($\times$0.95)')
	plt.ylabel('Insert throughput (MOPS)')
	plt.legend()

	plt.subplot(1, 2, 2)
	plt.plot(items, CF['delete'], 'v-', color='#0072bd', label='CF')
	plt.plot(items, SSCF['delete'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(items, BCF['delete'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(items, VF['delete'], '*-', color='#3d9140', label='VF')
	plt.plot(items, CGCF['delete'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(items, CGCF_HP['delete'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel(r'Number of elements ($\times$0.95)')
	plt.ylabel('Delete throughput (MOPS)')
	plt.legend()

	plt.savefig('items.tiff', format='tiff', dpi=300, bbox_inches='tight')

	plt.show()
