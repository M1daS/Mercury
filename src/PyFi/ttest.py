'''
Created on Jun 27, 2017

@author: michaelsands
'''

from __future__ import print_function
from scipy import stats

import numpy as np
import pandas as pd

def init_ttest(ticker, YAHOO_HISTORIC_PATH):
    cols = ['date', 'open', 'high', 'low', 'close', 'adjClose', 'volume']
    path_tsla = YAHOO_HISTORIC_PATH
    print(YAHOO_HISTORIC_PATH)
    
    data_tsla = pd.read_csv(path_tsla, names=cols, skiprows=range(0, 1), parse_dates=['date'], index_col=['date'])
    tsla_close = pd.DataFrame(data_tsla, columns = ['close'])
    daily_return1 = tsla_close.pct_change()
    daily_return = daily_return1.dropna()
    
    print('Average Daily Returns (mean)')
    print(round(np.mean(daily_return['close']), 4), 'or ', (round(np.mean(daily_return['close']), 4) * 100), '%')
    
    statlist = []
    print('T-VALUE        ', 'P-VALUE        ')
    out1 = stats.ttest_1samp(daily_return['close'], 5.0)#TEST WEATHER THE SAMPLE HAS A MEAN OF 0.5
    statlist.append(out1)
    out2 = stats.ttest_1samp(daily_return['close'], 0)#TEST WEATHER THE SAMPLE HAS A MEAN OF 0.0
    statlist.append(out2)
    print(statlist)
    return(statlist)


