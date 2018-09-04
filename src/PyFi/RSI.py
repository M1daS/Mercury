'''
Created on Sep 25, 2017

@author: micha
'''
import numpy as np
import pandas as pd
from matplotlib import pyplot as pypl

def init_rsi(historical_path): 

    df = pd.read_table(historical_path, sep=',', skiprows=range(0, 2), names=['Date', 'Open', 'High', 'Low', 'Close', 'Adj.Close', 'Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    '''
    http://www.andrewshamlet.net/2017/06/10/python-tutorial-rsi/
    RSI = 100 - 100 / (1 + RS)
    RS = Average gain of last 14 trading days / Average loss of last 14 trading days
    '''
    #RSI > 70 = Overbought
    #RSI < 30 = Oversold

    def RSI(series, period):
        delta = series.diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
        d = d.drop(d.index[:(period-1)])
        rs = u.ewm(com=period-1, adjust=False).mean() / \
        d.ewm(com=period-1, adjust=False).mean()
        return 100 - 100 / (1 + rs)
    # fig = pypl.figure()
    # ax1 = fig.add_subplot(211)
    # ax1.plot([0, 250], [70, 70], 'k-', lw=2, color = 'yellow')#[x1,x2], [y1,y2]
    # ax1.plot([0, 250], [30, 30], 'k-', lw=2, color = 'yellow')
    # # ax1.ylabel('RSI')
    # # ax1.xlabel('Time')
    # ax1.plot(RSI(df['Close'], 20))
    # ax1.legend(loc = 'best')
    # # ax1.grid()
    # fig.savefig(out_path, bbox_inches='tight')

    rsi = RSI(df['Close'], 20)
    return rsi


# init_rsi('/home/msands/Dropbox/ProgrammingFiles/Present/Share/Input/YahooHistorical/NVDA1Y.csv')





