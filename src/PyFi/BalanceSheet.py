'''
Created on Jul 13, 2017

@author: michaelsands
'''
'''
Created on Jun 25, 2017

@author: michaelsands
'''
import numpy as np
import pandas as pd

def get_balance_sheet(ticker, bs_path, morning_path, year):
    #print(bs_path)

    colnames = ['metric', year-4, year - 3, year - 2, year - 1, year]
    data = pd.read_table(bs_path, sep = ",", skiprows = range(0,2), names = colnames)
    metrics = data['metric']
    #print(metrics)
    del data['metric']
    df_unindex = pd.DataFrame(data, columns = [year-4, year - 3, year - 2, year - 1, year])
    df_indexed1 = df_unindex.set_index(metrics)
    df_indexed1.index.name = ticker
    df_indexed2 = df_indexed1.rename(index={"Total non-current liabilities": 'Tot. Non-Current Liab.'})
    df_indexed = df_indexed2.rename(index={"Total current liabilities": 'Tot. Current Liab.'})
    
    
    rows_names = ['Total cash','Total current assets','Total non-current assets','Total assets','Receivables','Tot. Current Liab.','Tot. Non-Current Liab.','Total liabilities','Accounts payable','Treasury stock','Retained earnings','Total stockholders\' equity' ]
    balance1 = pd.DataFrame(df_indexed.ix[rows_names])
    balance = balance1.apply(lambda x: np.round(x, decimals=2))
    
    
    path = morning_path + str(year) + '/' +  ticker + '/' + 'OUTPUT ' + ticker+ ' Balance Sheet.csv'
    #print(path)
    balance.to_csv(path, sep=',')
    
    #print('Balance Sheet: ', df_indexed.index.values.tolist())
    return(path)
    

    


