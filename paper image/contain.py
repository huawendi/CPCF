import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

CF: dict = {
	'positive': [
		22.09, 22.33, 22.46, 22.36, 22.33, 21.92, 22.41, 22.44, 22.12, 22.59,
		22.60, 22.51, 22.68, 22.61, 22.61, 22.56, 22.63, 22.65, 22.68
	],
	'negative': [
		23.44, 23.02, 23.04, 23.05, 22.97, 22.53, 22.94, 23.04, 22.62, 23.04,
		23.03, 23.18, 23.09, 23.15, 23.08, 23.27, 23.27, 23.27, 23.28
	],
	'mixed': [
		22.99, 23.13, 22.92, 22.77, 22.77, 22.45, 23.01, 23.05, 23.13, 23.10,
		23.18, 23.12, 23.19, 23.16, 23.20, 23.22, 23.24, 23.19, 23.23
	],
	'proportion': [
		22.98, 22.80, 22.67, 22.47, 22.24, 22.11, 21.79, 21.81, 21.64, 21.42, 21.26
	],
}

SS_CF: dict = {
	'positive': [
		8.58, 8.58, 8.56, 8.64, 8.67, 8.70, 8.70, 8.68, 8.69, 8.70,
		8.71, 8.69, 8.69, 8.70, 8.70, 8.72, 8.72, 8.71, 8.71
	],
	'negative': [
		8.62, 8.60, 8.39, 8.47, 8.55, 8.62, 8.64, 8.64, 8.64, 8.66,
		8.67, 8.66, 8.67, 8.68, 8.68, 8.69, 8.69, 8.68, 8.68
	],
	'mixed': [
		8.63, 8.57, 8.50, 8.46, 8.67, 8.69, 8.69, 8.69, 8.70, 8.71,
		8.71, 8.70, 8.70, 8.70, 8.71, 8.71, 8.71, 8.71, 8.71
	],
	'proportion': [
		8.44, 8.63, 8.61, 8.61, 8.57, 8.65, 8.63, 8.65, 8.62, 8.671, 8.699
	],
}

BCF: dict = {
	'positive': [
		23.82, 22.97, 23.74, 23.48, 23.80, 23.71, 23.88, 23.86, 23.42, 23.98,
		24.02, 23.98, 24.03, 24.08, 23.96, 24.11, 24.08, 24.10, 24.07
	],
	'negative': [
		23.53, 22.82, 23.17, 22.90, 23.33, 23.03, 23.33, 23.35, 23.11, 23.46,
		23.52, 23.54, 23.53, 23.61, 23.58, 23.62, 23.58, 23.65, 23.64
	],
	'mixed': [
		23.44, 22.69, 23.62, 22.87, 23.68, 23.77, 23.75, 23.77, 23.46, 23.85,
		23.84, 23.74, 23.70, 23.86, 23.86, 23.84, 23.87, 23.85, 23.70
	],
	'proportion': [
		22.13, 23.79, 23.83, 23.73, 23.93, 23.94, 23.91, 24.03, 24.04, 24.02, 24.03
	],
}

VF: dict = {
	'positive': [
		34.27, 33.42, 33.35, 33.75, 32.43, 32.76, 32.87, 32.61, 32.09, 31.47,
		30.84, 30.08, 29.35, 28.47, 27.57, 26.63, 25.51, 24.17, 21.89
	],
	'negative': [
		20.75, 19.75, 20.62, 20.71, 20.31, 20.26, 20.61, 20.58, 20.34, 20.64,
		20.70, 20.74, 20.71, 20.74, 20.76, 20.80, 20.83, 20.83, 20.87
	],
	'mixed': [
		24.91, 25.42, 25.64, 25.57, 25.60, 25.79, 25.66, 25.31, 25.71, 25.61,
		25.53, 25.31, 25.15, 24.89, 24.54, 24.13, 23.58, 22.81, 21.60
	],
	'proportion': [
		20.04, 20.74, 20.62, 20.88, 21.23, 21.34, 21.43, 21.57, 21.61, 21.66, 21.81
	],
}

MF: dict = {
	'positive': [
		24.54, 25.25, 25.49, 25.16, 25.24, 25.56, 24.88, 25.55, 25.55, 25.55,
		25.51, 25.52, 25.59, 25.68, 25.66, 25.67, 25.66, 25.70, 25.66
	],
	'negative': [
		26.07, 25.96, 23.96, 24.53, 25.16, 25.22, 24.76, 25.12, 25.24, 25.29,
		25.33, 25.35, 25.41, 25.41, 25.45, 25.48, 25.56, 25.50, 25.53
	],
	'mixed': [
		25.99, 25.13, 24.97, 25.53, 25.53, 25.43, 25.42, 25.52, 25.51, 25.54,
		25.35, 25.62, 25.59, 25.69, 25.64, 25.61, 25.66, 25.68, 25.64
	],
	'proportion': [
		25.27, 25.22, 25.17, 25.29, 25.25, 24.68, 24.97, 25.31, 25.38, 25.43, 25.37
	],
}

HG: dict = {
	'positive': [
		29.68, 29.78, 28.95, 29.28, 29.07, 29.32, 29.2, 29.11, 29.13, 28.96,
		29.18, 29.20, 29.21, 29.29, 29.43, 29.38, 29.31, 29.39, 29.40
	],
	'negative': [
		29.78, 28.68, 28.93, 29.02, 28.97, 28.83, 29.02, 28.97, 29.12, 29.09,
		29.25, 29.33, 29.24, 29.35, 29.19, 29.38, 29.43, 29.37, 29.42
	],
	'mixed': [
		29.59, 29.50, 29.47, 29.13, 29.26, 29.28, 28.97, 29.21, 29.15, 29.10,
		29.26, 29.29, 29.32, 29.32, 29.4, 29.34, 29.37, 29.43, 29.47
	],
	'proportion': [
		29.42, 29.45, 29.44, 29.40, 29.43, 29.47, 29.40, 29.34, 29.44, 29.28, 29.40
	],
}


def x_update_scale_value(temp, position) -> str:
	result = temp * 100
	return '{}%'.format(int(result))


if __name__ == '__main__':
	fig = plt.figure(figsize=(7, 4.5), constrained_layout=True)
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	occupancy = np.linspace(0.05, 0.95, 19)

	plt.subplot(2, 2, 1)
	plt.plot(occupancy, CF['positive'], 'v-', color='#0072bd', label='CF')
	plt.plot(occupancy, SS_CF['positive'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(occupancy, BCF['positive'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(occupancy, VF['positive'], '*-', color='#3d9140', label='VF')
	plt.plot(occupancy, MF['positive'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(occupancy, HG['positive'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.xlim(-0.01, 1.01)

	plt.text(0.5, 0, '(a) 100% positive lookup', fontsize=8, horizontalalignment='center')
	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel('Table occupancy')
	plt.ylabel('Lookup throughput (MOPS)')
	plt.legend(ncol=2, loc='lower right', bbox_to_anchor=(1, 0.1))

	plt.subplot(2, 2, 2)
	plt.plot(occupancy, CF['negative'], 'v-', color='#0072bd', label='CF')
	plt.plot(occupancy, SS_CF['negative'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(occupancy, BCF['negative'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(occupancy, VF['negative'], '*-', color='#3d9140', label='VF')
	plt.plot(occupancy, MF['negative'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(occupancy, HG['negative'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.xlim(-0.01, 1.01)

	plt.text(0.5, 1.5, '(b) 100% negative lookup', fontsize=8, verticalalignment='center', horizontalalignment='center')
	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel('Table occupancy')
	plt.ylabel('Lookup throughput (MOPS)')
	plt.legend(ncol=2, loc='lower right', bbox_to_anchor=(1, 0.1))

	plt.subplot(2, 2, 3)
	plt.plot(occupancy, CF['mixed'], 'v-', color='#0072bd', label='CF')
	plt.plot(occupancy, SS_CF['mixed'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(occupancy, BCF['mixed'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(occupancy, VF['mixed'], '*-', color='#3d9140', label='VF')
	plt.plot(occupancy, MF['mixed'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(occupancy, HG['mixed'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.xlim(-0.01, 1.01)

	plt.text(0.5, 1.5, '(c) 50% positive and 50% negative lookup', fontsize=8, horizontalalignment='center')
	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel('Table occupancy')
	plt.ylabel('Mixed lookup throughput (MOPS)')
	plt.legend(ncol=2, loc='lower right', bbox_to_anchor=(1, 0.1))

	plt.subplot(2, 2, 4)
	proportion = np.linspace(0, 1, 11)
	plt.plot(proportion, CF['proportion'], 'v-', color='#0072bd', label='CF')
	plt.plot(proportion, SS_CF['proportion'], 'p-', color='#8968cd', label='SSCF')
	plt.plot(proportion, BCF['proportion'], 'h-', color='#ca3e47', label='BCF')
	plt.plot(proportion, VF['proportion'], '*-', color='#3d9140', label='VF')
	plt.plot(proportion, MF['proportion'], 's-', color='#b26d5f', label='CGCF')
	plt.plot(proportion, HG['proportion'], 'd-', color='#edb120', label='CGCF_HP')

	plt.tick_params(direction='in')

	plt.text(0.5, 1.5, '(d) mix of positive and negative lookup', fontsize=8, horizontalalignment='center')
	plt.gca().xaxis.set_major_formatter(FuncFormatter(x_update_scale_value))
	plt.xlabel('proportion of existing items')
	plt.ylabel('Lookup throughput (MOPS)')
	plt.legend(ncol=2, loc='lower right', bbox_to_anchor=(1, 0.1))

	plt.savefig('contain.tiff', format='tiff', dpi=300, bbox_inches='tight')
	plt.show()
