import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def heatmap(df):
	m = df.mean(axis=0)
	s = df.std(ddof=1, axis=0)
	 
	# normalised time-series as an input for PCA
	dfPort = (df - m)/s
	 
	c = np.cov(dfPort.values.T)     # covariance matrix
	co = np.corrcoef(df.values.T)  # correlation matrix
	 
	tickers = list(df.columns)
	 
	plt.figure(figsize=(8,8))
	plt.imshow(co, cmap="RdGy", interpolation="nearest")
	cb = plt.colorbar()
	cb.set_label("Correlation Matrix Coefficients")
	plt.title("Correlation Matrix", fontsize=14)
	plt.xticks(np.arange(len(tickers)), tickers, rotation=90)
	plt.yticks(np.arange(len(tickers)), tickers)
	 
	# perform PCA
	w, v = np.linalg.eig(c)  
	ax = plt.figure(figsize=(8,8)).gca()
	plt.imshow(v, cmap="bwr", interpolation="nearest")
	cb = plt.colorbar()
	plt.yticks(np.arange(len(tickers)), tickers)
	plt.xlabel("PC Number")
	plt.title("PCA", fontsize=14)
	# force x-tickers to be displayed as integers (not floats)
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	plt.show()



def to_df(pathtohistoric, tickers, frequency):
	df = pd.DataFrame()

	'''1. Retrieve Close price data'''
	for symbol in tickers:

		df[symbol] = pd.read_csv(pathtohistoric + symbol + '_' +str(frequency) + '.csv', index_col = 'date')['close']
		df.dropna(inplace=True)

	heatmap(df)



def init(pathtohistoric):

	tickers = ['USDT_BTC','USDT_BCH','USDT_ETC','USDT_XMR','USDT_ETH','USDT_DASH',
	'USDT_XRP','USDT_LTC','USDT_NXT','USDT_STR','USDT_REP','USDT_ZEC', 'USDT_NXT',
	'BTC_PASC', 'BTC_STRAT', 'BTC_STORJ', 'BTC_DOGE', 'BTC_GNT', 'BTC_DGB', 'BTC_BTS','BTC_XEM','BTC_SC',
	'BTC_OMG', 'BTC_POT', 'BTC_LSK', 'BTC_ARDR', 'BTC_FCT', 'BTC_BCN', 'BTC_ZRX', 'BTC_OMNI', 'BTC_SYS',
	'BTC_BURST','BTC_MAID','BTC_VTC', 'BTC_STEEM', 'BTC_CVC', 'BTC_NEOS', 'BTC_EMC2', 'BTC_CLAM', 'BTC_GAS']
	frequency = 300
	to_df(pathtohistoric, tickers, frequency)



