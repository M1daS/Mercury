#Compare the coorelation between all crypto coins
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator







def to_df(pathtohistoric, tickers, frequency):
	df = pd.DataFrame()

	'''1. Retrieve Close price data'''
	for symbol in tickers:

		df[symbol] = pd.read_csv(pathtohistoric + symbol + '_' +str(frequency) + '.csv', index_col = 'date')['close']
		df.dropna(inplace=True)




	'''2. Normalize Closing Price data to reflect percent changes'''
	normalized = df.divide(df.ix[0]) #Convert Price into Percent Returns
	pctreturns = df.pct_change().dropna() #Remove NA's

	pctrtn_period = pctreturns.tail(7) #7 periods (days)
	pctrtn_period_values = np.sum(pctrtn_period)

	correlation = pctreturns.corr() #Calculate Correlation based on Percent Returns
	#print(correlation)


	'''3. Find the most highly correlated currency pairs'''
	'''4.  Find weekly change in close price of all currencies'''
	'''5. Return the difference in weekly close percent change amoung highly correlated currency pairs'''


	max_corr_df = pd.DataFrame()
	coinlist = []
	pairlist = []
	valuelist = []
	coinpctrtn = []
	pairpctrtn = []

	for symbol in tickers:
		max_corr = np.sort(correlation[symbol])
		max_corr_value = max_corr[-2]

		for i in range(len(correlation[symbol])):
			if correlation[symbol][i] == max_corr_value:
				max_corr_row_label = correlation.index[i]
				max_corr_row_col = symbol
				coinlist.append(max_corr_row_col)
				pairlist.append(max_corr_row_label)
				valuelist.append(max_corr_value)
				coinpctrtn.append(pctrtn_period_values.ix[symbol])
				pairpctrtn.append(pctrtn_period_values.ix[max_corr_row_label])

	max_corr_df['Coin'] = coinlist
	max_corr_df['Pair'] = pairlist
	max_corr_df['Coin%Rtn'] = np.round(coinpctrtn, 5)
	max_corr_df['Pair%Rtn'] = np.round(pairpctrtn, 5)
	#If the return of the coin, is less than the return of it's highest correlated pair, the diff column
	#will be negative, and thus indicate that the coin is underperforming and thus the Coin should be
	# purchased and/or the pair should be shorted
	max_corr_df['Corr'] = np.round(valuelist, 5)
	max_corr_df['Diff.'] = np.round(max_corr_df['Coin%Rtn'] - max_corr_df['Pair%Rtn'], 5)
	max_corr_df['score'] = np.round((3 * max_corr_df['Corr']) + abs(1.5 * max_corr_df['Diff.']), 5)

	print(max_corr_df.sort_values('score'))

	return max_corr_df.sort_values('score')




	'''6. Apply Statistical Regression Analysis for further exploration'''
	# model = sm.OLS(pctreturns['USDT_ETH'],pctreturns['USDT_LTC']).fit()
	# print(model.summary())





def init(pathtohistoric, outputpath):

	tickers = ['USDT_BTC','USDT_ETH', 'USDT_BCH','USDT_ETC','USDT_XMR','USDT_DASH', 'USDT_XRP','USDT_LTC',
	'BTC_ETH', 'BTC_BCH','BTC_ETC','BTC_XMR','BTC_DASH', 'BTC_XRP','BTC_LTC', 'BTC_NAV',
	 'BTC_STRAT', 'BTC_STORJ','BTC_LSK', 'BTC_VTC', 'USDT_NXT', 'USDT_ZEC']
	frequency = 300

	out = to_df(pathtohistoric, tickers, frequency)
	out.to_csv(outputpath)
	return out

