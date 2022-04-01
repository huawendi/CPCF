import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import FuncFormatter
from matplotlib.pyplot import MultipleLocator


def upperpower2(x: int) -> int:
	tmp = math.log2(x)
	tmp = math.pow(2, math.ceil(tmp))
	return tmp


def balls_in_bins(balls: float, bins: float, alpha: float) -> float:
	return balls / bins + alpha * math.sqrt(2 * balls / bins * math.log(bins))


def fccf(keys: int, alpha: float) -> tuple:
	buckets: float = keys / 4 / 0.95
	chunks: float = 1
	tmp: int = 1

	while tmp <= buckets:
		num: float = buckets / tmp
		if balls_in_bins(keys, num, alpha) <= 0.96 * 4 * tmp:
			keys /= num
			chunks *= num
			buckets = tmp
			break
		tmp <<= 1

	# 此时 num_buckets 一定为 2 的 n 次幂
	while num >= 2:
		tmp = 1
		while tmp <= buckets:
			num: float = buckets / tmp
			if balls_in_bins(keys, num, alpha) <= 0.96 * 4 * tmp:
				keys /= num
				chunks *= num
				buckets = tmp
				break
			tmp <<= 1

	return math.ceil(chunks), upperpower2(math.ceil(buckets))


def logb(n: int) -> float:
	a: float = math.log(3 * n + 1)
	b: float = math.log(4)
	return a / b


def kicknum(chunks, buckets) -> int:
	c = math.log(chunks)
	b = logb(buckets)
	return math.ceil(2 * 4 * c * b)


data: list = [
	[79, 102, 70, 80, 182, 75, 83, 78, 80, 64],
	[96, 151, 132, 193, 156, 104, 83, 84, 99, 181],
	[99, 89, 143, 109, 174, 153, 223, 110, 108, 83],
	[211, 155, 160, 191, 234, 248, 177, 181, 127, 172],
	[210, 242, 267, 159, 191, 196, 260, 249, 227, 287],
	[114, 138, 117, 157, 145, 162, 139, 91, 127, 123],
	[180, 171, 116, 123, 117, 162, 118, 125, 211, 120],
	[335, 141, 153, 156, 131, 126, 170, 173, 196, 205],
	[170, 170, 183, 176, 162, 323, 232, 213, 185, 171],
	[169, 253, 194, 420, 222, 252, 263, 312, 232, 209],
]

if __name__ == "__main__":
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	x = np.linspace(0, 9, 10)
	average = [np.mean(i) for i in data]

	plt.figure(figsize=(3.5, 2.5))

	res = list()
	for i in np.linspace(18, 22, 5):
		res.append(fccf(2 ** i * 0.95, 1))
	for i in np.linspace(23, 27, 5):
		res.append(fccf(2 ** i * 0.95, 1.5))

	threshold = [kicknum(i[0], i[1]) for i in res]
	plt.plot(x, threshold, 'o-', linewidth=2, color='#0088ff', label='CGCF\'s threshold')

	exceeded: bool = False
	normal: bool = False
	for i in range(10):
		for item in data[i]:
			if item > threshold[i]:
				if not exceeded:
					plt.scatter(i, item, c='red', label='exceeded data')
					exceeded = True
				else:
					plt.scatter(i, item, c='red')
			else:
				if not normal:
					plt.scatter(i, item, c='gray', label='normal data')
					normal = True
				else:
					plt.scatter(i, item, c='gray')

	plt.scatter(x, average, color='#fdc897', label='average value')

	# plt.scatter([10] * 10, data[9], color='gray', label='normal data')
	# for i in range(len(data) - 1):
	# 	plt.scatter([i + 1] * 10, data[i], color='gray')

	# log_x1 = np.log(x[: 5])
	# coe1 = np.polyfit(log_x1, average[: 5], 1)
	# plt.plot(x[: 5], coe1[0] * log_x1 + coe1[1], 'o-', linewidth=2, color='#94cc94', label='1st fitting curve')

	# log_x2 = np.log(x[5:])
	# coe2 = np.polyfit(log_x2, average[5:], 1)
	# plt.plot(x[5:], coe2[0] * log_x2 + coe2[1], 'o-', linewidth=2, color='#fdc897', label='2nd fitting curve')

	x_major_locator = MultipleLocator(1)
	plt.gca().xaxis.set_major_locator(x_major_locator)
	plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda temp, position: r'2$^{%s}$' % (int(temp) + 18)))
	plt.xlabel(r'Number of elements ($\times$0.95)')
	plt.ylabel('Max kick out value')
	plt.legend()

	plt.tick_params(direction='in')
	plt.savefig('kickout.tiff', format='tiff', dpi=300, bbox_inches='tight')
	plt.show()
