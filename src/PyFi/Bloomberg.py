'''
Created on Sep 20, 2017

@author: micha
'''
#https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe


import csv
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
from decimal import *

def bloomberg_index(tickers):
#THIS CODE NOW USES MARKETWATCH NOT BLOOMBERG...RENAME
    
    closeprice = []
    pointchange = []
    pctchange = []
    df = pd.DataFrame()
    for item in tickers:
        url ='https://www.marketwatch.com/investing/index/' + str(item)

        
        with urllib.request.urlopen(url) as response:
            html = response.read()

        try:
            soup = BeautifulSoup(html, 'html.parser')
            ticker_box = soup.find('span', attrs={'class':'value'})
            close = ticker_box.text.strip()

            pointchange_box = soup.find('span', attrs={'class':'change--point--q'})
            point = pointchange_box.text.strip()
            print(type(point))

            percentbox = soup.find('span', attrs={'class':'change--percent--q'})
            pct = percentbox.text.strip()
            print(type(pct))

            closeprice.append(float(close.replace(',','')))
            pointchange.append(float(point.replace(',','')))
            pctchange.append(float(pct.replace('%','')))
        except:
            close = 'na'
            pointchange = 'na'
            pct = 'na'


    df['close'] = closeprice
    df['pointchange'] = pointchange
    df['pct'] = pctchange
    return df
    
    
def marketwatch_stock(tickers):
    for item in tickers:
        url = 'https://www.marketwatch.com/investing/stock/' + str(item)

        with urllib.request.urlopen(url) as response:
            html = response.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        ticker_box = soup.find('td', attrs={'class':'table__cell u-semi'})
        close = ticker_box.text.strip()
        print('cloooose')
        print(close)

    return ''
