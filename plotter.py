import pandas as pd
import mplfinance as mpf
from datetime import datetime

def plot(api_response, coin_name, trendlines = None):
	df = pd.DataFrame(api_response)
	df.columns = ['Time', 'Volume', 'Close', 'High', 'Low', 'Open', 'dummy']
	df['Time'] = [datetime.fromtimestamp(int(df.iloc[i]['Time'])) for i in df.index]
	df = df.set_index('Time')
	df[['Volume', 'Close', 'High', 'Low', 'Open']] = df[['Volume', 'Close', 'High', 'Low', 'Open']].astype(float)

	if trendlines:
		points_for_trendlines = []
		linestyle = []
		for i, j, yi, yj in trendlines:
			points_for_trendlines.append([(str(df.index[i]), yi), (str(df.index[j]), yj)])
			if j >= 700:
				linestyle.append("dotted")
			else:
				linestyle.append("solid")

		mpf.plot(df,
			alines = dict(alines = points_for_trendlines, linestyle = linestyle),
			type = 'candle', style = 'yahoo', figsize = (16*3, 9*3), savefig = "plots/" + coin_name)
	else:
		mpf.plot(df,
			type = 'candle', style = 'yahoo', figsize = (32, 18), savefig = coin_name)