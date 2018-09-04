'''
Created on Jul 13, 2017

@author: michaelsands
'''
'''
Created on Jun 25, 2017

@author: michaelsands
'''
import pandas as pd
import numpy as np



def get_income_statement(ticker, is_path, morning_path, year):
    colnames = ['metric', year - 4, year - 3, year - 2, year - 1, year, 'TTM']
    data = pd.read_table(is_path, sep = ",", skiprows = range(0,2), names = colnames)
    metrics = data['metric']
    #print(metrics)
    del data['metric']
    df_unindex = pd.DataFrame(data, columns = [year - 4, year - 3, year - 2, year - 1, year, 'TTM'])
    df_indexed = df_unindex.set_index(metrics)
    df_indexed.index.name = ticker
    del df_indexed['TTM']
    
    
    rows_names = ['Revenue','Cost of revenue','Gross profit','Research and development','Sales, General and administrative','Total operating expenses','Operating income','Net income from continuing operations','Net income','EBITDA','Earnings per share']
    midas_df = pd.DataFrame(df_indexed.ix[rows_names])
    midas1 = midas_df.rename(index={"Sales, General and administrative": 'Sales'}) #SALES, GENERAL AND ADMINISTRATIVE
    midas2 = midas1.rename(index={"Net income from continuing operations": "Net Inc. frm Opp."})#NET INCOME FROM OPPERATIONS
    midas3 = midas2.rename(index={"Earnings per share": "EPS"})
    midas_final = midas3.apply(lambda x: np.round(x, decimals=2))
    
    path = morning_path + str(year) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' Income Statement.csv'
    midas_final.to_csv(path, sep=',')

    return(path)
    


