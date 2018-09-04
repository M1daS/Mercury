#Find any Coin whos Last trade price is > upper BB, or < lower BB based upon specified time chart


import pandas as pd
import numpy as np
import datetime
import urllib.request

'''


IN CRYPTO DOWNLOAD CHANGE THE START PARAM TO THE PREVIOUS
DWNLOADED MATERIAL SO WE DONT HAVE TO REDOWNLOAD ALL DATA
THAN MERGE THE OLD MATERIAL WITH THE NEW DOWNLOAD?



'''



def init(path, outputpathbuy, outputpathsell):

	tickers = ['USDT_BTC','USDT_ETH', 'USDT_BCH','USDT_ETC','USDT_XMR','USDT_DASH', 'USDT_XRP','USDT_LTC',
	'BTC_ETH', 'BTC_BCH','BTC_ETC','BTC_XMR','BTC_DASH', 'BTC_XRP','BTC_LTC', 'BTC_NAV',
	'BTC_STRAT', 'BTC_STORJ','BTC_LSK', 'BTC_VTC', 'USDT_NXT', 'USDT_ZEC']
	frequency = 300


	print('Latest Download @: ' + str(datetime.datetime.now().time().strftime('%H:%M:%S')))

	df = pd.DataFrame()
	for symbol in tickers:
		df[symbol] = pd.read_csv(path + symbol + '_' + str(frequency) + '.csv', index_col = 'date')['close']
		df.dropna(inplace=True)

	df_ma = pd.DataFrame()
	df_upperband = pd.DataFrame()
	df_lowerband = pd.DataFrame()
	for symbol in tickers:
		df_ma[symbol] = np.round(df[symbol].rolling(window=20).mean(), 6)
		df_upperband[symbol] = df_ma[symbol] + (df_ma[symbol].rolling(window=20).std() * 6)
		df_lowerband[symbol] = df_ma[symbol] - (df_ma[symbol].rolling(window=20).std() * 6)
	

	#print(df_upperband.tail())

	df_analyze = pd.DataFrame()
	df_analyze['upperband'] = np.round(df_upperband.ix[-1],6)
	df_analyze['close'] = np.round(df.ix[-1], 6)
	df_analyze['lowerband'] = np.round(df_lowerband.ix[-1],6)

	buy = df.where(df_analyze['close'] < df_analyze['lowerband']).dropna()
	sell = df.where(df_analyze['close'] > df_analyze['upperband']).dropna()
	print(buy)
	print(sell)

	buy.to_csv(outputpathbuy)
	sell.to_csv(outputpathsell)

	return (buy, sell)


# def cryptodata_download():
#     #Params: String symbol, int frequency = 300(5MIN),900 (15),1800 (30),7200 (120),14400,86400 (DAY)

# 	tickers = ['USDT_BTC','USDT_ETH', 'USDT_BCH','USDT_ETC','USDT_XMR','USDT_DASH', 'USDT_XRP','USDT_LTC',
# 	'BTC_ETH', 'BTC_BCH','BTC_ETC','BTC_XMR','BTC_DASH', 'BTC_XRP','BTC_LTC', 'BTC_NAV',
# 	 'BTC_STRAT', 'BTC_STORJ','BTC_LSK', 'BTC_VTC', 'USDT_NXT', 'USDT_ZEC']
# 	frequency = 300
# 	global PATH
# 	for symbol in tickers:
# 		try:
# 		    url ='https://poloniex.com/public?command=returnChartData&currencyPair='+symbol+'&end=9999999999&period='+str(frequency)+'&start=0'
# 		    df = pd.read_json(url)
# 		    df.set_index('date',inplace=True)
# 		    PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Linux/Hash/PriceDataFiles/'
# 		    df.to_csv(PATH + symbol + '_' + str(frequency) + '.csv')
# 		    print('Processed: ' + symbol)
# 		except(urllib.error.HTTPError):
# 			print('http error')
# 			continue

# 	to_df(tickers, frequency)





#cryptodata_download()


