'''
Created on Jul 13, 2017
@author: michaelsands
Created on Jun 23, 2017
@author: michaelsands
'''
#THIS PROGRAM CALCULATES THE ROLLING BETA OF A STOCK BASED UPON AN INPUT OF DAILY CLOSE PRICES, ACCUMULATED OVER A ? TIMEPERIODS WORTH OF RETURNS (PCT CHANGES)

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# statsmodels is used to do OLS regression
import statsmodels.api as sm
# we're using yahoo finance data, pandas datareader will import the data we need
from pandas_datareader.data import DataReader
  
# wrapping up the code in a simple function
def calc_stats(df):
    '''
        requires a DataFrame of monthly returns where 
        first column is the stock
        second column is the market index 
    '''
    X = sm.add_constant(df.iloc[:, 1])
    model = sm.OLS(df.iloc[:, 0], X).fit()
    
    beta = model.params["^GSPC"]
    #alpha = model.params["const"]
    r2 = model.rsquared
    return beta, r2 #return alpha when working
    
def rolling_stats(df, window=5):
    # dataframe to hold the results
    res = pd.DataFrame(index=df.index)
    
    for i in range(0, len(df.index)):
    
        if len(df) - i >= window:
            # break the df into smaller chunks
            chunk = df.iloc[i:window + i, :]
            # calc_stats is a function created from the code above, 
            # refer to the Gist at the end of the article.
            beta, r2 = calc_stats(chunk) #add alpha
            res.set_value(chunk.tail(1).index[0], "beta", beta)
            #res.set_value(chunk.tail(1).index[0], "alpha", alpha)
            res.set_value(chunk.tail(1).index[0], "r2", r2)
            # print "%s beta: %.4f \t alpha: %.4f" % (chunk.tail(1).index[0],b,a)
    res = res.dropna()
    return res

def init_beta(ticker, historic_path, market_path, out_path):
    cols = ['date', 'open', 'high', 'low', 'close', 'adjClose', 'volume']
    print(ticker)
    
    path_co = historic_path
    path_market = market_path

    data_co = pd.read_csv(path_co, names=cols, skiprows=range(0, 1), parse_dates=['date'], index_col=['date'])
    tsla_close = pd.DataFrame(data_co['close'])
    tsla_close.columns = [ticker]


    data_market = pd.read_csv(path_market, names=cols, skiprows=range(0, 1), parse_dates=['date'], index_col=['date'])
    sap_close = pd.DataFrame(data_market['close'])
    sap_close.columns = ['^GSPC']
    



    final_close = pd.concat([tsla_close, sap_close], axis=1)
    #THIS BETA IS CALCULATED USING DAILY CLOSE PRICE STOCK DATA - BELEIVE ITS MORE EFFECTIVE TO USE MONTHLY/ANNUALIZED DATA FOR ROLLING BETAS
    dfmret = final_close.pct_change()
    # testing the rolling stats
    dftest = dfmret
    df_rolling = rolling_stats(dftest, window=10)

    return df_rolling
    
    # plotting the rolling beta
    # ax = df_rolling[["beta"]].plot(title=('Rolling Beta _ ' + ticker))
    # ax.grid(True)
    # ax.legend(loc='upper left', ncol=2, fontsize='small')
    #path = path_output + ticker + ' Beta.png'
    # plt.savefig(out_path, bbox_inches='tight')
    
    # #print(df_rolling.head(20))
    
    # #path_stats = stat_out_path + 'Beta.png'
    # #df_rolling.to_csv(path_stats, sep = ',')

    
 
    