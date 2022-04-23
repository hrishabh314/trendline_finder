import parameters as pmts

import numpy as np
from sortedcontainers import SortedList

def get_support_trendlines(close, high, low, open):
	close = np.array([float(i) for i in close])
	high = np.array([float(i) for i in high])
	low = np.array([float(i) for i in low])
	open = np.array([float(i) for i in open])

	trendlines = list()
	slope_for_candle = dict()

	for j in range(len(close)):
		sl = SortedList()
		for i in range(j-1, -1, -1):
			x1 = i
			y10 = low[i]
			y11 = min(open[i], close[i], y10 + (high[i] - low[i]) / 2)
			
			x2 = j
			y2 = low[j]

			slope0 = (y2 - y10) / (x2 - x1)
			slope1 = (y2 - y11) / (x2 - x1)
			
			number_of_candles_so_far = j - i + 1
			if (number_of_candles_so_far >= pmts.min_candles_for_trendline_threshold):
				number_of_slopes_in_between = sl.bisect_left(slope0) - sl.bisect_left(slope1)
				number_of_breakouts = len(sl) - sl.bisect_left(slope0)

				condition1 = number_of_candles_so_far * pmts.breakout_tolerance_factor >= number_of_breakouts
				condition2 = number_of_candles_so_far * pmts.touch_requirement_factor <= number_of_slopes_in_between
				if condition1 and condition2:

					# new trendline
					if slope_for_candle.get(i, np.inf) == np.inf:
						slope_for_candle[i] = slope0
						trendlines.append((x1, x2, y10, y2))
					
					# extension of existing trendline
					else:
						y_value_j = y10 + slope_for_candle[i] * (j - i)
						if low[j] < y_value_j and y_value_j < min(open[j], close[j]):
							trendlines.append((x1, x2, y10, y_value_j))


			sl.add(slope0)

	return trendlines


def get_resistance_trendlines(close, high, low, open):
	close = np.array([float(i) for i in close])
	high = np.array([float(i) for i in high])
	low = np.array([float(i) for i in low])
	open = np.array([float(i) for i in open])

	trendlines = list()
	slope_for_candle = dict()

	for j in range(len(close)):
		sl = SortedList()
		for i in range(j-1, -1, -1):
			x1 = i
			y11 = high[i]
			y10 = max(open[i], close[i], y11 - (high[i] - low[i]) / 2)
			
			x2 = j
			y2 = high[j]

			slope0 = (y2 - y10) / (x2 - x1)
			slope1 = (y2 - y11) / (x2 - x1)
			
			number_of_candles_so_far = j - i + 1
			if (number_of_candles_so_far >= pmts.min_candles_for_trendline_threshold):
				number_of_slopes_in_between = sl.bisect_left(slope0) - sl.bisect_left(slope1)
				number_of_breakouts = sl.bisect_left(slope1)

				condition1 = number_of_candles_so_far * pmts.breakout_tolerance_factor >= number_of_breakouts
				condition2 = number_of_candles_so_far * pmts.touch_requirement_factor <= number_of_slopes_in_between
				if condition1 and condition2:

					# new trendline
					if slope_for_candle.get(i, np.inf) == np.inf:
						slope_for_candle[i] = slope1
						trendlines.append((x1, x2, y11, y2))
					
					# extension of existing trendline
					else:
						y_value_j = y11 + slope_for_candle[i] * (j - i)
						if max(open[j], close[j]) < y_value_j and y_value_j < high[j]:
							trendlines.append((x1, x2, y11, y_value_j))


			sl.add(slope1)

	return trendlines







# def temp_func():
# 	from sortedcontainers import SortedList
# 	sl = SortedList()
# 	n = int(input())
	
# 	for i in range(n):
# 		x = int(input())
# 		print(sl.bisect_left(x))
# 		sl.add(x)

# 	print(sl)
# 	sl.remove(sl[3])
# 	print(sl)

# temp_func()