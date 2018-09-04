from pandas_datareader import data
import pandas as pd
import numpy as np
import datetime
'''
http://www.learndatasci.com/python-finance-part-yahoo-finance-api-pandas-matplotlib/
http://www.learndatasci.com/python-finance-part-2-intro-quantitative-trading-strategies/
'''
now = datetime.datetime.now()
# yahoo_input_directory_path = '/home/msands/Dropbox/ProgrammingFiles/Present/Share/Input/YahooHistorical/'


def retrieve_historical_data(timespan, tickers, outputpath):
	#tickers = [ 'BABA', 'TSLA', 'NVDA', 'EEM', 'AAPL', 'C', 'BAC', 'MELI']
	#tickers = ['AMAT', 'AMD', 'LRCX', 'HD', 'JNJ', 'WYN', 'LVS', 'CRM']

	year = now.year
	month = now.month
	day = now.day
	hour = now.hour
	minute = now.minute

	data_source = 'yahoo'
	start_date = str(year - 1) + '-' + str(month) + '-' + str(day)
	end_date = str(year) + '-' + str(month) + '-' + str(day)


	for item in tickers:
		print(item),
		panel_data = data.DataReader(item, data_source, start_date, end_date)
		path = outputpath + item + timespan + '.csv'
		panel_data.to_csv(path)

		

#IF YOU ADJUST THE TIMESPAN BELOW, YOU MUST ADJUST THE START DATE SUBTRACTION AMOUNT ALSO
# timespan = '1Y'
# retrieve_historical_data(timespan)
