'''
Created on Jul 13, 2017

@author: michaelsands
'''
'''
Created on Jun 25, 2017

@author: michaelsands
'''
import pandas as pd
import BalanceSheet as b_s  
import IncomeStatement as i_s
import Buffett as buf
import Vause as vause
import numpy as np


def get_competitor_metrics(TICKER, filetype, competitors_list_path, MORNINGSTAR_PATH, OUTPUT_PATH, YEAR):
    
    colnames = ['Co','Compet1', 'Compet2', 'Compet3', 'Compet4']
    competitors_file = pd.read_table(competitors_list_path, sep = ',', skiprows=range(0, 1), names = colnames)
    
    full_competitor_list = pd.DataFrame()
    full_competitor_list['Co'] = competitors_file['Co']
    full_competitor_list['Compet1'] = competitors_file['Compet1']
    full_competitor_list['Compet2'] = competitors_file['Compet2']
    full_competitor_list['Compet3'] = competitors_file['Compet3']
    full_competitor_list['Compet4'] = competitors_file['Compet4']
    full_competitor_list = full_competitor_list.set_index(full_competitor_list['Co'])
    
    del full_competitor_list['Co']

    
    temp = []
    for item in full_competitor_list.ix[TICKER]:
        path = MORNINGSTAR_PATH + str(YEAR) + '/' + item + '/' + item + ' Balance Sheet.csv'
        b_s.get_balance_sheet(TICKER, path, MORNINGSTAR_PATH, YEAR )
        path = MORNINGSTAR_PATH + str(YEAR) + '/' + item + '/' + item + ' Income Statement.csv'
        i_s.get_income_statement(TICKER, path, MORNINGSTAR_PATH, YEAR )
        bsout = MORNINGSTAR_PATH + str(YEAR) + '/' +  item + '/' + 'OUTPUT ' + item+ ' Balance Sheet.csv'
        incout = MORNINGSTAR_PATH + str(YEAR) + '/' +  item + '/' + 'OUTPUT ' + item+ ' Income Statement.csv'
        
        if filetype == 'VauseCompetitors':
            path = MORNINGSTAR_PATH + str(YEAR) + '/' + item + '/' + item + ' Balance Sheet.csv'
            b_s.get_balance_sheet(TICKER, path, MORNINGSTAR_PATH, YEAR )
            path = MORNINGSTAR_PATH + str(YEAR) + '/' + item + '/' + item + ' Income Statement.csv'
            i_s.get_income_statement(TICKER, path, MORNINGSTAR_PATH, YEAR )
            path_bs = MORNINGSTAR_PATH + str(YEAR) + '/' +  item + '/' + 'OUTPUT ' + item+ ' Balance Sheet.csv'
            path_is = MORNINGSTAR_PATH + str(YEAR) + '/' +  item + '/' + 'OUTPUT ' + item+ ' Income Statement.csv'

    
            compet = vause.get_vause_metrics(TICKER, MORNINGSTAR_PATH, path_bs, path_is, OUTPUT_PATH, YEAR)

            colnames = [TICKER, YEAR-4, YEAR - 3, YEAR - 2, YEAR - 1, YEAR]
            vausefile = pd.read_table(compet, sep = ',', skiprows=range(0, 1), names = colnames)
    

            desired = vausefile[YEAR]
            temp.append(desired)


        if filetype == 'BuffettCompetitors':
            path = MORNINGSTAR_PATH + str(YEAR) + '/' + item + '/' + item + ' Balance Sheet.csv'
            b_s.get_balance_sheet(TICKER, path, MORNINGSTAR_PATH, YEAR )
            path = MORNINGSTAR_PATH + str(YEAR) + '/' + item + '/' + item + ' Income Statement.csv'
            i_s.get_income_statement(TICKER, path, MORNINGSTAR_PATH, YEAR )
            path_bs = MORNINGSTAR_PATH + str(YEAR) + '/' +  item + '/' + 'OUTPUT ' + item+ ' Balance Sheet.csv'
            path_is = MORNINGSTAR_PATH + str(YEAR) + '/' +  item + '/' + 'OUTPUT ' + item+ ' Income Statement.csv'
    
            compet = buf.get_buffett_metrics(TICKER, MORNINGSTAR_PATH, path_bs, path_is, OUTPUT_PATH, YEAR)

            colnames = [TICKER, YEAR-4, YEAR - 3, YEAR - 2, YEAR - 1, YEAR]
            buffile = pd.read_table(compet, sep = ',', skiprows=range(0, 1), names = colnames)
    

            desired = buffile[YEAR]
            temp.append(desired)

    df = pd.DataFrame([alist for alist in temp]).transpose()
    df.columns = full_competitor_list.ix[TICKER]
  
  
    path = OUTPUT_PATH +  TICKER + ' Competitors ' + filetype +  '.csv'
    df.to_csv(path, sep=',')
    
    return(path)
    



def get_competitor_financials(TICKER, filetype, competitors_list_path, MORNINGSTAR_PATH, OUTPUT_PATH, YEAR):
    a = ''









'''
    if boolean == 'Income':
        TICKER_sheet = i_s.get_income_statement(TICKER, path_morningincome, path_output)
    if boolean == 'Balance':
        TICKER_sheet = b_s.get_balance_sheet(TICKER, path_morningbalance , path_output)

    TICKER_renamed =  TICKER_sheet.rename(columns ={year: TICKER})
    TICKER_sheet_final = pd.DataFrame(TICKER_renamed[TICKER])
    
    temp_list = []
    select_row = competitors_list
    for i in range(len(select_row)):
        competitor = select_row[i]
        try:
            if boolean == 'Income':
                morning_income = competitor + ' Income Statement.csv'
                path_morningincome = '/Users/michaelsands/Dropbox/EclipseOSX_Workspace/FinancialsFiles/Q2_2017/'+ competitor + '/'+  morning_income
                competitor_sheet = i_s.get_income_statement(competitor, path_morningincome, path_output)
            if boolean == 'Balance':
                morning_balance = competitor + ' Balance Sheet.csv'
                path_morningbalance = '/Users/michaelsands/Dropbox/EclipseOSX_Workspace/FinancialsFiles/Q2_2017/'+ competitor + '/'+ morning_balance
                competitor_sheet = b_s.get_balance_sheet(competitor, path_morningbalance, path_output)

            competitor_renamed =  competitor_sheet.rename(columns ={year: competitor})
            temp_list.append(competitor_renamed[competitor])

            #print(comp_bs)
        except IOError:
            print('IOError - File not found - Check existence of desired file in Morningstar Financials folder for company ', competitor)
    competitor_sheet_full = pd.DataFrame(temp_list).transpose()
    combined_sheets = [TICKER_sheet_final, competitor_sheet_full ]
    full_financials = pd.concat(combined_sheets, axis= 1)
    if boolean == 'Income':
        full_financials.index.name = TICKER
    if boolean == 'Balance':
        full_financials.index.name = TICKER
    
    path = path_output + TICKER + '_' +boolean + '_' +year + 'CompetitorsFinancials.csv'

    full_financials.to_csv(path, sep=',')
    return(full_financials) 

def retrieve_competing_companies(boolean, year, TICKER, path_output, path_morningbalance, path_morningincome):
    colnames = ['co', 'co1', 'co2', 'co3', 'co4']
    path = '//Users/michaelsands/Dropbox/EclipseOSX_Workspace/Competitors.csv'
    data = pd.read_table(path, sep=',', names=colnames, index_col=['co'])
    competitors_list = data.ix[TICKER]
    

    competitors_financials = get_competitor_financials(boolean, year, TICKER, competitors_list, path_output, path_morningbalance, path_morningincome)

    return competitors_financials
'''