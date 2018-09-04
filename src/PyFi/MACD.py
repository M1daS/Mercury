'''
Created on Sep 25, 2017

@author: micha
'''

import numpy as np
import pandas as pd

def run_macd( historic_path):
    #http://www.andrewshamlet.net/2017/01/19/python-tutorial-macd-moving-average-convergencedivergence/
  
    df = pd.read_table(historic_path, sep=',', skiprows=range(0, 2), names=['Date', 'Open', 'High', 'Low', 'Close', 'Adj.Close', 'Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    
    sma30= np.round(df['Close'].rolling(window=30).mean(), 2)
    ema26 = df['Close'].ewm(span = 26).mean()
    ema12 = df['Close'].ewm(span = 12).mean()
    macd = ema12 - ema26
    
    signal_line = macd.ewm(span = 9).mean()

    outdf = pd.DataFrame()
    outdf['signal'] = signal_line
    outdf['macd'] = macd

    
    return(outdf)
    