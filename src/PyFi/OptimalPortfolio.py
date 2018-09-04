'''
Created on Jul 20, 2017

@author: michaelsands
'''
'''
Created on Jul 15, 2017

@author: micha
'''
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

 #http://www.pythonforfinance.net/2017/01/21/investment-portfolio-optimisation-with-python/
 #http://www.pythonforfinance.net/2017/01/21/investment-portfolio-optimisation-with-python/

def optimize(tickerlist, YAHOO_HISTORIC_PATH): 
    #list of stocks in portfolio
    #stock1 = input('Ticker No. 1')
    
    #download daily price data for each of the stocks in the portfolio

    path = YAHOO_HISTORIC_PATH + tickerlist[0] + '1Y.csv'
    path2 = YAHOO_HISTORIC_PATH + tickerlist[1] + '1Y.csv'
    path3 = YAHOO_HISTORIC_PATH + tickerlist[2] + '1Y.csv'
    path4 = YAHOO_HISTORIC_PATH + tickerlist[3] + '1Y.csv'
    stocks = [tickerlist[0], tickerlist[1], tickerlist[2], tickerlist[3]]
    
    
    df = pd.read_table(path, sep = ',')
    close = df['Adj Close']
    
    df2 = pd.read_table(path2, sep = ',')
    close2 = df2['Adj Close']
    
    df3 = pd.read_table(path3, sep = ',')
    close3 = df3['Adj Close']
    
    df4 = pd.read_table(path4, sep = ',')
    close4 = df4['Adj Close']
    
    
    data = pd.concat([close, close2, close3, close4], axis=1).dropna()
    #print(data)
    #convert daily stock prices into daily returns
    returns = data.pct_change().dropna()
    
    
    mean_return = returns.mean()
    return_stdev = returns.std()
     
          
            
    #calculate mean daily return and covariance of daily returns
    mean_daily_returns = returns.mean()
    cov_matrix = returns.cov()
    
    
    #set number of runs of random portfolio weights
    num_portfolios = 10000
     
    #set up array to hold results
    #We have increased the size of the array to hold the weight values for each stock
    results = np.zeros((4+len(stocks)-1,num_portfolios))
     
    
    for i in range(num_portfolios):
        #select random weights for portfolio holdings
        weights = np.array(np.random.random(4))
        #rebalance weights to sum to 1
        weights /= np.sum(weights)
     
        #calculate portfolio return and volatility
        portfolio_return = np.sum(mean_daily_returns * weights) * 252
        portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252)
     
        #store results in results array
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
        results[2,i] = results[0,i] / results[1,i]
    
        #iterate through the weight vector and add data to results array
        for j in range(len(weights)):
            results[j+3,i] = weights[j]
     
    #convert results array to Pandas DataFrame
    results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe',stocks[0],stocks[1],stocks[2],stocks[3]])
     
    #locate position of portfolio with highest Sharpe Ratio
    max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
    #locate positon of portfolio with minimum standard deviation
    min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]
    

    outdf = pd.DataFrame()
    outdf['maxsharpe'] = max_sharpe_port
    outdf['minvol'] = min_vol_port

    # #create scatter plot coloured by Sharpe Ratio
    # plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
    # plt.xlabel('Volatility')
    # plt.ylabel('Returns')
    # plt.colorbar()
    # #plot red star to highlight position of portfolio with highest Sharpe Ratio
    # plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=1000)
    
    # #plot green star to highlight position of minimum variance portfolio
    # plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='g',s=1000)

    # outpath = OUTPUT_PATH + ' OptimalPortfolio'
    # plt.savefig(OUTPUT_PATH, bbox_inches='tight')

    #print('max sharpe portfolio')
    #print(max_sharpe_port)
    #print('min volitility')
    #print(min_vol_port)
    
    # frames = [max_sharpe_port, min_vol_port]

    #text = max_sharpe_port, '\n', min_vol_port
    return outdf

