import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def x_update_scale_value(temp, position) -> str:
	result = temp * 100
	return '{}%'.format(int(result))


CF: dict = {
	'insert': [
		24.69, 24.18, 22.73, 21.50, 20.51, 19.65, 18.92, 18.32, 17.93, 17.20,
		16.61, 15.99, 15.20, 14.34, 13.28, 12.05, 10.55, 8.59, 5.46
	],
	'delete': [
		26.20, 24.87, 24.59, 23.64, 22.91, 22.10, 21.55, 20.90, 20.41, 19.61,
		18.69, 17.83, 16.89, 16.01, 15.11, 14.18, 13.22, 12.41, 12.17
	],
}

SSCF: dict = {
	'insert': [
		7.50, 7.54, 7.42, 7.42, 7.38, 7.31, 7.25, 7.16, 7.07, 6.97,
		6.85, 6.72, 6.55, 6.37, 6.15, 5.87, 5.49, 4.87, 3.56
	],
	'delete': [
		7.49, 7.44, 7.31, 7.24, 7.28, 7.23, 7.13, 7.08, 7.01, 6.92,
		6.82, 6.71, 6.59, 6.47, 6.36, 6.24, 6.15, 6.12, 6.16
	],
}

BCF: dict = {
	'insert': [
		6.72, 6.79, 6.76, 6.70, 6.75, 6.73, 6.76, 6.76, 6.76, 6.78,
		6.78, 6.78, 6.78, 6.77, 6.75, 6.67, 6.47, 6.01, 4.69
	],
	'delete': [
		28.09, 24.35, 22.25, 20.87, 20.09, 19.47, 18.89, 18.36, 17.83, 17.63,
		17.34, 17.08, 16.71, 16.54, 16.25, 15.87, 15.31, 14.61, 13.72
	],
}

VF: dict = {
	'insert': [
		24.12, 22.97, 21.77, 20.88, 20.00, 18.97, 18.48, 17.97, 17.35, 17.00,
		16.55, 16.03, 15.47, 14.81, 14.18, 13.42, 12.52, 11.25, 8.77
	],
	'delete': [
		30.08, 28.14, 26.44, 24.45, 23.49, 23.21, 22.48, 21.73, 21.37, 20.70,
		20.07, 19.42, 18.74, 18.04, 17.33, 16.55, 15.63, 14.59, 13.56
	],
}

CGCF: dict = {
	'insert': [
		32.31, 30.54, 28.84, 27.33, 25.99, 24.70, 23.59, 22.57, 21.51, 20.72,
		20.03, 19.35, 18.67, 17.86, 17.00, 15.86, 14.44, 12.72, 9.83
	],
	'delete': [
		29.10, 28.06, 26.43, 24.90, 23.63, 22.58, 21.50, 20.45, 19.57, 18.70,
		18.00, 17.35, 16.87, 16.40, 16.00, 15.58, 15.13, 14.69, 14.07
	],
}

CGCF_HP: dict = {
	'insert': [
		36.20, 34.20, 32.44, 30.69, 29.07, 27.64, 26.16, 25.02, 24.15, 23.27,
		22.54, 21.77, 21.18, 20.47, 19.64, 18.53, 17.08, 15.11, 11.47
	],
	'delete': [
		34.54, 31.99, 29.97, 27.92, 26.57, 25.25, 24.06, 22.95, 21.92, 21.07,
		20.34, 19.76, 19.21, 18.73, 18.31, 17.88, 17.46, 17.02, 16.42
	]
}

if __name__ == '__main__':
	plt.figure(figsize=(8.3, 2.5))
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	occupancy = np.linspace(0.05, 0.95, 19)

	plt.subplot(1, 2, 1)
	plt.plot(occupancy, CF['insert'], 'v-', color='#0072bd', label='CF')
	plt.plot(occupancy, SSCF['insert'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(occupancy, BCF['insert'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(occupancy, VF['insert'], '*-', color='#3d9140', label='VF')
	plt.plot(occupancy, CGCF['insert'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(occupancy, CGCF_HP['insert'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.xlim(-0.01, 1.01)

	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel('Table occupancy')
	plt.ylabel('Insert throughput (MOPS)')
	plt.legend(ncol=2)

	plt.subplot(1, 2, 2)
	plt.plot(occupancy, CF['delete'], 'v-', color='#0072bd', label='CF')
	plt.plot(occupancy, SSCF['delete'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(occupancy, BCF['delete'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(occupancy, VF['delete'], '*-', color='#3d9140', label='VF')
	plt.plot(occupancy, CGCF['delete'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(occupancy, CGCF_HP['delete'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.xlim(-0.01, 1.01)

	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel('Table occupancy')
	plt.ylabel('Delete throughput (MOPS)')
	plt.legend(ncol=2)

	plt.savefig('occupancy.tiff', format='tiff', dpi=300, bbox_inches='tight')

	plt.show()
