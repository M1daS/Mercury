'''
Created on Jul 13, 2017

@author: michaelsands
'''
'''
Created on Jun 25, 2017

@author: michaelsands
#Formerly the Economist Book Formulas class - by Bob Vause
'''
import numpy as np
import pandas as pd


def get_vause_metrics(ticker, MORNINGSTAR_PATH, bs_path, is_path, path_output, YEAR):
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
    
    
    # GROSS PROFIT MARGIN RATIO
    gpmr = 100 * (income.ix['Gross profit'] / income.ix['Revenue'])
    # OPPERATING PROFIT MARGIN RATIO
    opmr = 100 * (income.ix['Net Inc. frm Opp.'] / income.ix['Revenue'])
    # PERCENT RATE OF RETURN  ON ASSETS
    rra = 100 * (income.ix['Gross profit'] / balance.ix['Total assets'])
    # ASSET TURN
    aturn = 100 * (income.ix['Revenue'] / balance.ix['Total assets'])
    # R&D
    rd = 100 * (income.ix['Research and development'] / income.ix['Revenue'])
    # debt to equity ratio
    equity = balance.ix['Total assets'] - (balance.ix['Tot. Non-Current Liab.'] + balance.ix['Tot. Current Liab.'])
    der = (balance.ix['Tot. Non-Current Liab.'] + balance.ix['Tot. Current Liab.']) / equity
    # asset gearing
    agear = balance.ix['Total assets'] / equity
    # Return on equity
    roe = (income.ix['Gross profit'] / income.ix['Revenue']) * (income.ix['Revenue'] / balance.ix['Total assets']) * (balance.ix['Total assets'] / equity)
   
   
    data = [gpmr, opmr, rra, aturn, rd, der, agear, roe ]
    metrics = ['GR. PROFIT MARGIN', 'OPP. PROFIT MARGIN', 'PCT. RETURN ON ASSETS', 'ASSET TURN', 'R&D', 'DEBT TO EQUITY', 'ASSET GEARING', 'ROE']
    econ_df1 = pd.DataFrame(data, index=metrics)
    econ_df1.index.name = ticker
    econ_df = econ_df1.apply(lambda x: np.round(x, decimals=2))
    
    
    path = MORNINGSTAR_PATH + str(YEAR) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' VauseMetrics.csv'
    econ_df.to_csv(path, sep=',')
    
    
    return path



    
    
    
    
    
    
    
    
'''the methods below were detailed in the vause book but are not
currently being called by the program to do analysis upon the retrieved data'''

def get_common_size(balance, income):
    equity = balance.ix['Total assets'] - (balance.ix['Tot. Non-Current Liab.'] + balance.ix['Tot. Current Liab.'])
    ta = balance.ix['Total assets']
    tncl = balance.ix['Tot. Non-Current Liab.']
    tcl = balance.ix['Tot. Current Liab.']
    
    e_cs = 100 * (equity / ta)
    ncl_cs = 100 * (tncl / ta)
    cl_cs = 100 * (tcl / ta)
    
    data = [e_cs, ncl_cs, cl_cs]
    commonsize_df1 = pd.DataFrame(data, index=['Equity', 'NonCurr Liab', 'Curr Liab'])
    commonsize_df = commonsize_df1.apply(lambda x: np.round(x, decimals=1))
    print(commonsize_df)
    
    # print(rev1)
def get_growth_rates(balance, income, econ_df):
    rev = income.ix['Revenue']
    crev = income.ix['Cost of revenue']
    gp = income.ix['Gross profit']
    opm = econ_df.ix['OPP. PROFIT MARGIN']
    ninc = income.ix['Net income']
    
    rev_chg = rev.pct_change() * 100
    crev_chg = crev.pct_change() * 100
    gp_chg = gp.pct_change() * 100
    opm = opm.pct_change() * 100
    ninc_chg = ninc.pct_change() * 100

    data = [rev_chg, crev_chg, gp_chg, opm, ninc_chg]
    gr = pd.DataFrame(data, index = ['Revenue', 'Cost Of Rev', 'Gross Profit', 'OppProfitMargin', 'NetIncome'])
    growth_df = gr.apply(lambda x: np.round(x, decimals=1))

    print(growth_df)


def get_opperating_profit_margin(balance, income, econ_df):
    # includes all income and expenses (admin, researc, development + general overheads)
    # general assessment of profitability of company after taking into account all costs of producing and supplying goods or services and the income from selling them
    opm = econ_df.ix['OPP. PROFIT MARGIN']
    avg_opm = np.mean(opm)
    
    ninc = income.ix['Net income']
    avg_ninc = np.mean(ninc)
    
    #relation_to_avg_opm = opm - opm.shift(1)
    #relation_to_avg_ninc = ninc - ninc.shift(1)
    movement_from_avg_opm = opm - avg_opm
    movement_from_avg_ninc = ninc - avg_ninc
  
    data = [movement_from_avg_opm, movement_from_avg_ninc ]
    move_from_avg_df = pd.DataFrame(data, index = ['diff from avg OPM', 'diff from avg ninc'])
    print(move_from_avg_df)
