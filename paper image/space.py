import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FuncFormatter


def upperpower2(x: int) -> int:
	tmp = math.log2(x)
	tmp = math.pow(2, math.ceil(tmp))
	return tmp


# original Cuckoo Filter
def ocf(keys: int) -> int:
	assoc = 4
	num_buckets = upperpower2(max(1, keys / assoc))
	frac = keys / num_buckets / assoc
	if frac > 0.96:
		return num_buckets * 2

	return num_buckets


def rounddown(a: int, b: int) -> int:
	return a - (a % b)


def roundup(a: int, b: int) -> int:
	return rounddown(a + (b - 1), b)


def balls_in_bins_max_load(balls: float, bins: float) -> float:
	m = balls
	n = bins
	if n == 1:
		return m
	ret = (m / n) + 1.5 * math.sqrt(2 * m / n * math.log(n))
	return ret


def proper_alt_range(M: int) -> int:
	b = 4
	lf = 0.95
	alt_range = 8
	while alt_range < M:
		if balls_in_bins_max_load(b * lf * M, M / alt_range) <= 0.96 * b * alt_range:
			return alt_range
		alt_range <<= 1
	return alt_range


# Vacuum Filter
def vf(keys: int) -> int:
	num_buckets = math.floor(keys / 0.95 / 4)
	big_seg = max(1024, proper_alt_range(num_buckets))
	return roundup(num_buckets, big_seg)


def balls_in_bins(balls: float, bins: float, alpha: float) -> float:
	return balls / bins + alpha * math.sqrt(2 * balls / bins * math.log(bins))


# flexibly chunked Cuckoo Filter
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


def y(n: int) -> int:
	return math.log10(n)


def power_update_scale_value(temp, position) -> str:
	return r'2$^{%s}$' % int(temp)


if __name__ == "__main__":
	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	fig = plt.figure(figsize=(2.5, 1.9))
	ax1 = plt.subplot(1, 1, 1)
	keys = np.linspace(19, 26, 8)

	f_res = list()
	for i in keys:
		if i < 23:
			f_res.append(fccf(2 ** i, 1))
		else:
			f_res.append(fccf(2 ** i, 1.5))

	f_chunks = [f_res[i][0] for i in range(len(f_res))]
	f_buckets = [math.log2(f_res[i][1]) for i in range(len(f_res))]

	lns1 = ax1.bar(keys, f_buckets, alpha=0.9, label='buckets')
	plt.gca().xaxis.set_major_formatter(FuncFormatter(power_update_scale_value))

	x_major_locator = MultipleLocator(1)
	ax1.xaxis.set_major_locator(x_major_locator)
	ax1.set_ylim(11.5, 13.5)
	y_major_locator = MultipleLocator(1)
	ax1.yaxis.set_major_locator(y_major_locator)
	ax1.yaxis.set_major_formatter(FuncFormatter(power_update_scale_value))

	ax1.tick_params(direction='in')
	ax1.tick_params(axis='x', length=0)
	ax1.set_xlabel('Number of items')
	ax1.set_ylabel('Number of buckets each sub-filter')

	ax2 = ax1.twinx()
	lns2 = ax2.plot(keys, f_chunks, 'o-', linewidth=2, color='#ff502f', label='sub-filters')
	ax2.set_ylabel('Number of sub-filters')

	fig.legend(bbox_to_anchor=(0.49, 1), bbox_transform=ax1.transAxes)

	plt.tick_params(direction='in')
	plt.savefig('number.tiff', format='tiff', dpi=300, bbox_inches='tight')
	plt.show()

	plt.figure(figsize=(3.5, 2.5))
	keys = [i for i in range(1 << 19, 1 << 20)]

	o_buckets = [y(ocf(i)) for i in keys]
	plt.plot(keys, o_buckets, label='cuckoo filter')

	v_buckets = [y(vf(i)) for i in keys]
	plt.plot(keys, v_buckets, label='vacuum filter')

	f_res = [fccf(i, 1) for i in keys]
	f_plt = [y(item[0] * item[1]) for item in f_res]
	plt.plot(keys, f_plt, label='flexibly chunked cuckoo filter')

	lf = [y(i / 4 / 0.95) for i in keys]
	plt.plot(keys, lf, label='load factor = 0.95')

	plt.tick_params(direction='in')

	plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda temp, position: '{}K'.format(int(temp // 1000))))
	plt.xlabel('Number of elements')
	plt.ylabel('Sum of buckets (log)')
	plt.legend()

	plt.savefig('buckets.tiff', format='tiff', dpi=300, bbox_inches='tight')
	plt.show()
