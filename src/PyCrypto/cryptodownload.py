import pandas as pd
import matplotlib.pyplot as pypl
import statsmodels.api as sm
import numpy as np
import datetime

def cryptodata_download():
    #Params: String symbol, int frequency = 300(5MIN),900 (15),1800 (30),7200 (120),14400,86400 (DAY)
    #frequency is by number of seconds


    tickers = ['USDT_BTC','USDT_ETH', 'USDT_BCH','USDT_ETC','USDT_XMR','USDT_DASH', 'USDT_XRP','USDT_LTC',
    'BTC_PASC', 'BTC_STRAT', 'BTC_STORJ', 'BTC_DOGE','BTC_LSK', 'BTC_VTC', 'USDT_NXT', 'USDT_ZEC']

    # tickers = ['USDT_BTC','USDT_BCH','USDT_ETC','USDT_XMR','USDT_ETH','USDT_DASH',
    # 'USDT_XRP','USDT_LTC','USDT_NXT','USDT_STR','USDT_REP','USDT_ZEC', 'USDT_NXT', 
    # 'BTC_PASC', 'BTC_STRAT', 'BTC_STORJ', 'BTC_DOGE', 'BTC_GNT', 'BTC_DGB', 'BTC_BTS','BTC_XEM','BTC_SC',
    # 'BTC_OMG', 'BTC_POT', 'BTC_LSK', 'BTC_ARDR', 'BTC_FCT', 'BTC_BCN', 'BTC_ZRX', 'BTC_OMNI', 'BTC_SYS',
    # 'BTC_BURST','BTC_MAID','BTC_VTC', 'BTC_STEEM', 'BTC_CVC', 'BTC_NEOS', 'BTC_EMC2', 'BTC_CLAM', 'BTC_GAS']

    #tickers = [ 'USDT_BTC']

    
    frequency = 900

    global PATH
    for symbol in tickers:
	    url ='https://poloniex.com/public?command=returnChartData&currencyPair='+symbol+'&end=9999999999&period='+str(frequency)+'&start=0'
	    df = pd.read_json(url)
	    df.set_index('date',inplace=True)
	    PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Linux/Hash/PriceDataFiles/'
	    df.to_csv(PATH + symbol + '_' + str(frequency) + '.csv')
	    print('Processed: ' + symbol)


    print(datetime.datetime.now().time())


cryptodata_download()


