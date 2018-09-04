from __future__ import print_function
import pandas as pd
import numpy as np
from scipy.stats import norm as n

def init_var(ticker, YAHOO_HISTORIC_PATH):

    cols = ['date', 'open', 'high', 'low', 'close', 'adjClose', 'volume']
    
    historicdata = pd.read_csv(YAHOO_HISTORIC_PATH, names=cols, skiprows=range(0, 1), parse_dates=['date'], index_col=['date'])
    close_data = pd.DataFrame(historicdata, columns = ['close'])
    
    n_shares = 1
    confidence_level = 0.95
    #Most commonly used with confidence level = 99 or 95
    n_days = 30
    z = n.ppf(confidence_level)
    #for a 99% confidence level, z = 2.33   : For a 95% confidence level, z = 1.64
    daily_return = close_data.pct_change()
    current_price = close_data.iloc[-1]
    position = n_shares * current_price
    
    VaR = position * z * np.std(daily_return)*np.sqrt(n_days)

    
    cols = ['closeprice', 'max_loss', 'days', 'confidence_level'] 
    outdata = [round(position['close'], 2), round(VaR['close'], 2), n_days, confidence_level]

    output = 'A postion of $', round(position['close'], 2), 'in ', ticker, 'will loose a maximum of $', round(VaR['close'], 2), 'over the next ', n_days, ' days - With a ', confidence_level, '% confidence level'

    #datalist = df.values.T.tolist()

    
    return output
