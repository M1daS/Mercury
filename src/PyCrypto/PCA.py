# Dec 29, 2017

#Principal Component Analysis for Correlation Detections
#http://www.quantatrisk.com/2017/03/31/cryptocurrency-portfolio-correlation-pca-python/
import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests

def init_pca(tickers):
	df = pd.DataFrame()

	global PATH
	for symbol in tickers:
		PATH = '/home/msands/Dropbox/ProgrammingFiles/Present/Linux/Hash/PriceDataFiles/'
		df[symbol] = pd.read_csv(PATH + symbol +'_' + str(frequency) + '.csv', index_col = 'date')['close']
		
		df.dropna(inplace=True)
	print(df.tail())



	#CORRELATION MATRIX

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



	#BI PLOT OF RELATIVE WEIGHTS


	# choose PC-k numbers
	k1 = -1  # the last PC column in 'v' PCA matrix
	k2 = -2  # the second last PC column
	 
	# begin constructing bi-plot for PC(k1) and PC(k2)
	# loadings
	plt.figure(figsize=(7,7))
	plt.grid()
	 
	# compute the distance from (0,0) point
	dist = []
	for i in range(v.shape[0]):
	    x = v[i,k1]
	    y = v[i,k2]
	    plt.plot(x, y, '.k')
	    plt.plot([0,x], [0,y], '-', color='grey')
	    d = np.sqrt(x**2 + y**2)
	    dist.append(d)
	#print(dist)

	# check and save membership of a coin to
	# a quarter number 1, 2, 3 or 4 on the plane
	quar = []
	for i in range(v.shape[0]):
	    x = v[i,k1]
	    y = v[i,k2]
	    d = np.sqrt(x**2 + y**2)




	    #change > to < to display all graphical properties
	    #THE > IS WHAT IS PREVENTING THE CALCULATION OF PROPERTIES BELOW
	    #IHAVE CHANGED THIS TO BE 0.5 STDEVS (0sd)
	    if(d > np.mean(dist) + (np.std(dist, ddof=1) * 0)): 
	    	plt.plot(x, y, '.r', markersize=10)
	    	plt.plot([0,x], [0,y], '-', color='grey')
	    	if((x > 0) and (y > 0)):
	    		quar.append((i, 1))
	    	elif((x < 0) and (y > 0)):
	    		quar.append((i, 2))
	    	elif((x < 0) and (y < 0)):
	    		quar.append((i, 3))
	    	elif((x > 0) and (y < 0)):
	    		quar.append((i, 4))

	    # print(quar)
	    # print(quar[0])
	    plt.text(x, y, tickers[i], color='k')
	 
	plt.xlabel("PC-" + str(len(tickers)+k1+1))
	plt.ylabel("PC-" + str(len(tickers)+k2+1))





	# #HIGHEST CORRELATION
	for i in range(len(quar)):

		# Q1 vs Q3
		if(quar[i][1] == 1):
			for j in range(len(quar)):
				if(quar[j][1] == 3):
					plt.figure(figsize=(7,4))
					# highly correlated coins according to the PC analysis
					print(tickers[quar[i][0]], tickers[quar[j][0]])
					ts1 = df[tickers[quar[i][0]]]  # time-series
					ts2 = df[tickers[quar[j][0]]]
					# correlation metrics and their p_values
					slope, intercept, r2, pvalue, _ = stats.linregress(ts1, ts2)
					ktau, kpvalue = stats.kendalltau(ts1, ts2)
					print(r2, pvalue)
					print(ktau, kpvalue)
					plt.plot(ts1, ts2, '.k')
					xline = np.linspace(np.min(ts1), np.max(ts1), 100)
					yline = slope*xline + intercept
					plt.plot(xline, yline,'--', color='b')  # linear model fit
					plt.xlabel(tickers[quar[i][0]])
					plt.ylabel(tickers[quar[j][0]])
					#plt.show()
		# Q2 vs Q4
		if(quar[i][1] == 2):
			for j in range(len(quar)):
				if(quar[j][1] == 4):
					plt.figure(figsize=(7,4))
					print(tickers[quar[i][0]], tickers[quar[j][0]])
					ts1 = df[tickers[quar[i][0]]]
					ts2 = df[tickers[quar[j][0]]]
					slope, intercept, r2, pvalue, _ = stats.linregress(ts1, ts2)
					ktau, kpvalue = stats.kendalltau(ts1, ts2)
					print(r2, pvalue)
					print(ktau, kpvalue)
					plt.plot(ts1, ts2, '.k')
					xline = np.linspace(np.min(ts1), np.max(ts1), 100)
					yline = slope*xline + intercept
					plt.plot(xline, yline,'--', color='b')
					plt.xlabel(tickers[quar[i][0]])
					plt.ylabel(tickers[quar[j][0]])
					#plt.show()


	plt.show()


tickers = [ 'USDT_XRP', 'USDT_BTC', 'USDT_ETH', 'USDT_ETC', 'USDT_BCH', 'USDT_XMR','USDT_ZEC', 'USDT_LTC', 'USDT_STR', 'USDT_DASH']
init_pca(tickers)




