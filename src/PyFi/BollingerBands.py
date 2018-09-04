'''
Created on Sep 10, 2017

@author: micha
'''

from matplotlib import pyplot as pypl
from matplotlib.pyplot import xlabel, ylabel
import numpy as np
import pandas as pd


# https://www.linkedin.com/pulse/python-tutorial-bollinger-bands-andrew-hamlet

#THis is how you do it by hand ---- or just use the prebuilt functions below
def calc_ma_the_hard_way(df, n):
    mylist = df
    N = n 
    cumsum, moving_aves = [0], []
    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            moving_aves.append(moving_ave)
    
    ma = pd.DataFrame(moving_aves, columns=['MA'])
    return ma
    

def calc_moving_average(df_close):
    df_ma = pd.DataFrame()
    df_ma['20'] = np.round(df_close.rolling(window=20).mean(), 2)
    df_ma['50'] = np.round(df_close.rolling(window=50).mean(), 2)
    df_ma['100'] = np.round(df_close.rolling(window=100).mean(), 2)
    df_ma['252'] = np.round(df_close.rolling(window=252).mean(), 2)
    
    #CALCULATE EXponential moving averages using df.ewm(span = #).mean()
    
    bands = pd.DataFrame()
    bands['middle'] = df_ma['20']
    bands['upper'] = df_ma['20'] + (df_close.rolling(window=20).std() * 2)
    bands['lower'] = df_ma['20'] - (df_close.rolling(window=20).std() * 2)

    return bands
    '''All code blow charts the above data'''


    # fig = pypl.figure( figsize = (12,15))
    # ax1 = fig.add_subplot(211)

    # ax1.plot(df['Date'], df_close, 'b-', label='Close', color='black', linewidth=2)
    # ax1.plot(df['Date'], df_ma['20'], '-', label='20MA', color='blue', linewidth=0.75)
    # ax1.plot(df['Date'], df_ma['50'], '-', label='50MA', color='pink', linewidth=0.75)
    # ax1.plot(df['Date'], df_ma['100'], '-', label='100MA', color='green', linewidth=0.75)
    # ax1.plot(df['Date'], df_ma['252'], '-', label='252MA', color='yellow', linewidth=0.75)
    # # PLOT BOLLINGER BANDS
    
    # ax1.plot(df['Date'], bands['upper'], '--', color='red', linewidth=0.75)
    # # pypl.plot(df['Date'], bands['middle'], '--', color = 'red') #this is just the 20day MA
    # ax1.plot(df['Date'], bands['lower'], '--', color='red', linewidth=0.75)

    # ax1.legend(loc='best')
    
    # fig.savefig(out_path, bbox_inches='tight')

    

def init_bb(historical_path):
    df = pd.read_table(historical_path, sep=',', skiprows=range(0, 2), names=['Date', 'Open', 'High', 'Low', 'Close', 'Adj.Close', 'Volume'])

    df['Date'] = pd.to_datetime(df['Date'])
    df_close = df['Close']

    bb_ma = calc_moving_average(df_close)
    bb_ma = bb_ma.dropna()
    return bb_ma
