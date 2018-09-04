
import pandas as pd
from pandas_datareader import data
import numpy as np

# Create a scoring system - i.e. 1pt for positive indicator -1 for negative and 0 for neutral
# Do this for every indicator and return dictionary with ticker symbol and total score 
# (Can also add weighting to give some indicators more importance than other)

def market_scan():
	#print('Initializing System...')
	#print('Gathering Data...This may take a few moments.')
	
	path = '/home/msands/Dropbox/ProgrammingFiles/Present/Linux/largemega_tickers.csv'
	#path = '/home/msands/Desktop/largemega_tickers.csv'
	colist = pd.read_csv(path, sep = ',')

	#tickers = colist['Symbol']
	tickers = [ 'BABA', 'NVDA',  'TSLA', 'MU', 'BAC', 'C', 'HD', 'MELI', 'PYPL']


	data_source = 'yahoo'
	start_date = '2016-01-01'
	end_date = '2017-11-08'

	panel_data = data.DataReader(tickers, data_source, start_date, end_date)
	close = panel_data.ix['Close']
	#all_weekdays = pd.date_range(start=start_date, end=end_date) #freq=B returns all weekdays, then reindex each by these weekdays
	#close = close_price.reindex(all_weekdays)


	print('MACD Results:')
	macd_strat = macd(tickers, close)
	print(macd_strat)

	print('RSI Results:')
	rsi_strat = init_rsi(tickers, close)
	print(rsi_strat)
	
	print('BollingerBand Results:')
	bb_strat = bollinger_bands(tickers, close)
	print(bb_strat)


	print('Simple Moving Average Results:')
	sma = moving_averages(tickers, close)
	print(sma)

def macd(tickers, close):
	#MACD line is 12ema - 26 ema
	#signal line is 9 ema

	ema26 = close.ewm(span = 26).mean()
	ema12 = close.ewm(span = 12).mean()
	macd = ema12 - ema26
	signal_line = macd.ewm(span = 9).mean()

	macdline_last = macd.iloc[-1]
	signalline_last = signal_line.iloc[-1]
	lastclose = close.iloc[-1]

	out = pd.DataFrame()
	out['macdline'] = macdline_last
	out['signalline'] = signalline_last


	yes_macd = []
	no_macd = []
	#THis should be if macd line is with in X percent of signal line then add to buy or sell
	#add more points if cross has just occured or is about to etc.
	for i in range(len(tickers)):
		if out['signalline'].ix[i] > out['macdline'].ix[i]:
			yes_macd.append(tickers[i])
		else:
			no_macd.append(tickers[i])


	return (yes_macd, no_macd)



def init_rsi(tickers, close):

	def RSI(series, period):
		#Overbought > 70
		#Oversold < 30

		#Period 
		#norm = 14
		#short term = 7
		#long term = 25

	    delta = series.diff().dropna()
	    u = delta * 0
	    d = u.copy()
	    u[delta > 0] = delta[delta > 0]
	    d[delta < 0] = -delta[delta < 0]
	    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
	    u = u.drop(u.index[:(period-1)])
	    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
	    d = d.drop(d.index[:(period-1)])
	    rs = u.ewm(com=period-1, adjust=False).mean() / d.ewm(com=period-1, adjust=False).mean()
	    return 100 - 100 / (1 + rs)


	rsi_data = pd.DataFrame()
	for symbol in tickers:
		rsi_data[symbol] = RSI(close[symbol], 14)

	last_rsi = []
	for symbol in tickers:
		last_rsi.append(rsi_data[symbol].iloc[-1])

	yes_rsi = []
	no_rsi = []
	for i in range(len(tickers)):
		if last_rsi[i] < 60:
			yes_rsi.append(tickers[i])
		else:
			no_rsi.append(tickers[i])

	return (yes_rsi, no_rsi)




def bollinger_bands(tickers, close):
	lastclose = pd.DataFrame(close.iloc[-1]).transpose()

	temp_ma_20 = []
	for symbol in tickers:
		temp20 = np.round(close[symbol].rolling(window=20).mean(), 2)
		temp_ma_20.append(temp20)

	df_ma_20 = pd.DataFrame(temp_ma_20).transpose()
	df_last_ma_20 = pd.DataFrame(df_ma_20.iloc[-1]).transpose()


	upperband_temp = np.round(df_last_ma_20 + (close.rolling(window = 20).std() * 2))
	upperband = pd.DataFrame(upperband_temp.iloc[-1]).transpose()

	lowerband_temp = np.round(df_last_ma_20 - (close.rolling(window = 20).std() * 2))
	lowerband = pd.DataFrame(lowerband_temp.iloc[-1]).transpose()

	frames = [upperband, df_last_ma_20, lowerband, lastclose]
	df = pd.concat(frames).transpose()
	df.columns = ['upperband', '20dayMA', 'lowerband', 'close']




	#if close < lower band ... buy
	#if close > higher band ... sell
	#if (higher > close < lower) ... neutral
	buy = [] 
	sell = []
	neutral = []
	for i in range(len(tickers)):
		upper = df['upperband'].ix[tickers[i]]
		lower = df['lowerband'].ix[tickers[i]]
		close = df['close'].ix[tickers[i]]
		if close > upper:
			sell.append(tickers[i])
		elif close < lower:
			buy.append(tickers[i])
		else:
			neutral.append(tickers[i])

	return(buy, neutral, sell)


def moving_averages(tickers, close):
	sma20= np.round(close.rolling(window=20).mean(), 2)
	sma50= np.round(close.rolling(window=50).mean(), 2)
	sma100= np.round(close.rolling(window=100).mean(), 2)

	'''

	1. determein if stock is in uptrend or downtrend
	2. if uptrend, MA act as support
	3. if downtrend, MA act as resistance
	#PRICE CROSSOVER
	uptrend = close > MA, downtrend = close < MA
	#GOLDEN CROSS
	short MA crosses above long MA
	#DEATH CROSS
	short MA cross below long MA
	'''
	return 'abc'

	
market_scan()

