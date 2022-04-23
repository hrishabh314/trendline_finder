import fetcher
import formatter
import trendline_generator
import plotter
import os
import shutil

path = 'Plots'
if os.path.exists(path):
	shutil.rmtree(path)
os.makedirs(path)

coin_names = ["BTC_USDT", "XRP_USDT", "LUNA_USDT", "LTC_USDT"]
# coin_names = ["BTC_USDT"]

limit = 1000

for coin_name in coin_names:
	api_response = fetcher.fetch(coin_name, limit = limit)

	timestamp, volume, close, high, low, open = formatter.format(api_response)

	support_trendlines = trendline_generator.get_support_trendlines(close, high, low, open)
	resistance_trendlines = trendline_generator.get_resistance_trendlines(close, high, low, open)
	trendlines = support_trendlines + resistance_trendlines
	print(sorted(trendlines))
	print(len(trendlines))
	print(coin_name)
	print()

	plotter.plot(api_response = api_response, coin_name = coin_name, trendlines = trendlines)