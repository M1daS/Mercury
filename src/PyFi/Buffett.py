'''
Created on Jul 13, 2017

@author: michaelsands
'''
'''
Created on Jul 12, 2017

@author: michaelsands
'''
import pandas as pd
import numpy as np

ALLTEXT = []
def get_buffett_metrics(ticker, MORNINGSTAR_PATH, bs_path, is_path, path_output, YEAR):
    #CALLING THIS METHOD CRASHES THE PROGRAM....
    
    #print(bs_path)
    colnames = [ticker, YEAR-4, YEAR - 3, YEAR - 2, YEAR - 1, YEAR]
    
    df_income =  pd.read_csv(is_path, skiprows=range(0, 1), names = colnames) #, parse_dates=['date'], index_col=['date']
    df_balance = pd.read_csv(bs_path, skiprows=range(0, 1), names = colnames)

    bal_metrics = df_balance[ticker]
    del df_balance[ticker]
    balance = df_balance.set_index(bal_metrics)
    
    inc_metrics = df_income[ticker]
    del df_income[ticker]
    income = df_income.set_index(inc_metrics)
    
    gp = income.ix['Revenue'] - income.ix['Cost of revenue']
    gpm = income.ix['Gross profit'] / income.ix['Revenue']
    oppprofloss = gp - income.ix['Total operating expenses']
    currentratio = balance.ix['Total current assets'] / balance.ix['Tot. Current Liab.']
    asstrtrnratio = balance.ix['Total assets'] / income.ix['Net income']
    debttoequityratio = balance.ix['Total liabilities'] / balance.ix['Total stockholders\' equity']
    retainedearnings = balance.ix['Retained earnings']
    rtnsharhldrequity = income.ix['Net income'] / balance.ix['Total stockholders\' equity']
    # GROSS PROFIT MARGIN
    
    
    data = [gp, gpm, oppprofloss, currentratio, asstrtrnratio, debttoequityratio, retainedearnings, rtnsharhldrequity ]
    metrics = ['GrossProfit', 'GrProfitMargin', 'OppProfitLoss', 'currentRatio', 'AssetTurnRatio', 'DebtToEquityRatio', 'RetainedEarnings', 'RtndSharehldrEquity']
    econ_df1 = pd.DataFrame(data, index=metrics)
    econ_df1.index.name = ticker
    econ_df = econ_df1.apply(lambda x: np.round(x, decimals=2))
    
    
    path = MORNINGSTAR_PATH + str(YEAR) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' BuffettMetrics.csv'
    econ_df.to_csv(path, sep = ',')
    
    return path
    


    '''
    out_path = path_output + ticker + ' BuffettMetrics.csv'
    econ_df.to_csv(out_path, sep=',')
    analyze_buffett(ticker, econ_df)
    '''
    
def analyze_buffett(ticker, df):
    print(df)
    
    gpm = df.ix['GrProfitMargin']
    if (gpm.all() > .30):  # gpm.any()F
        gpmtext = 'ALL years have a GPM > 30%'
    
    ALLTEXT.append(gpmtext)
    print(ALLTEXT)
    # mean_gp_change = np.round(np.mean(gp_change), 3) + 100
    # print('mean_gross prft change', mean_gp_change)
    
    
def get_buffet_analysis_text():
    return ALLTEXT
   
    
