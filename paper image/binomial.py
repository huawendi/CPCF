import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def upperpower2(x: int) -> int:
	tmp = math.log2(x)
	tmp = math.pow(2, math.ceil(tmp))
	return tmp


def balls_in_bins(balls: float, bins: float) -> int:
	return math.ceil(balls / bins + math.sqrt(2 * balls / bins * math.log(bins)))


def chunk(keys: int) -> tuple:
	buckets: float = keys / 4 / 0.95
	chunks: float = 1
	tmp: int = 1

	while tmp <= buckets:
		num: float = buckets / tmp
		if balls_in_bins(keys, num) <= 0.96 * 4 * tmp:
			keys /= num
			chunks *= num
			buckets = tmp
			break
		tmp <<= 1

	while num >= 2:
		tmp = 1
		while tmp <= buckets:
			num: float = buckets / tmp
			if balls_in_bins(keys, num) <= 0.96 * 4 * tmp:
				keys /= num
				chunks *= num
				buckets = tmp
				break
			tmp <<= 1

	return math.ceil(chunks), upperpower2(math.ceil(buckets))


def origin(m: int, h: int) -> float:
	return 2 * h / m


if __name__ == '__main__':
	keys = 1 << 20
	chunks, buckets = chunk(keys)

	print('the number of sub-filter is %s' % chunks)
	print('the number of buckets is %s' % buckets)

	p = 1 / chunks

	plt.rcParams['font.family'] = 'Times New Roman'
	plt.rcParams['font.size'] = 8

	plt.figure(figsize=(3.5, 2))

	H = 5
	x: np.array = np.arange(H)
	binomial = stats.binom.pmf(x, H, p)
	plt.plot(x, binomial, 'o-', linewidth=2, label='h = 5')

	for a, b in zip(x, binomial):
		plt.text(a if a != 0 else a + 0.05, b + 0.02 if a != 0 else b - 0.1, '%.3f' % b, ha='center', va='bottom',
		         fontsize=8)

	plt.tick_params(direction='in')
	plt.xlabel('Number of collision(s) in the certain sub-filter')
	plt.ylabel('Probability of collision(s)')
	plt.legend()

	plt.savefig('binomial.tiff', format='tiff', dpi=300, bbox_inches='tight')
	plt.show()
