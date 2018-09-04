'''
Created on Sep 20, 2017

@author: micha
'''
#https://coinmarketcap.com/


import csv
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request



def init():
    #df = marketcap()


    df2 = pctvolume()
    print(df2.head())



def marketcap():
    url = 'https://coinmarketcap.com/'
    df = pd.DataFrame()

    with urllib.request.urlopen(url) as response:
        html = response.read()
         
    soup = BeautifulSoup(html, 'html.parser')


    namelist = soup.find_all('span', attrs={'class': 'currency-symbol'})
    mc = soup.find_all('td', attrs={'class': 'no-wrap market-cap text-right'})
    vol = soup.find_all('a', attrs={'class': 'volume'})


    symbols = []
    markcaps = []
    volumes = []
    coins = []
    names = []
    for i in range(len(namelist)):
        startindex = str(namelist[i]).index('s/')
        endindex = str(namelist[i]).index('/"')
        name = str(namelist[i])[startindex +2 :endindex].upper()

        names.append(name)
        coins.append(namelist[i])
        symbols.append(namelist[i].text.strip())
        markcaps.append(mc[i].text.strip())
        volumes.append(vol[i].text.strip())



    df['name'] = names
    df['coin'] = symbols
    df['markcap'] = markcaps
    df['volume24hr'] = volumes

    return df




def pctvolume():
    url = 'https://coinmarketcap.com/currencies/volume/24-hour/'
    df = pd.DataFrame()

    with urllib.request.urlopen(url) as response:
        html = response.read()
         
    soup = BeautifulSoup(html, 'html.parser')

    pctvol = soup.find_all('h3', attrs={'class': 'volume-header'})

    pctvols = []
    for i in range(100):
        pctvols.append(str(pctvol[i].text.strip()).upper())



    df['pct'] = pctvols

    return df
    



def gainersloosers():
    return ''






init()

