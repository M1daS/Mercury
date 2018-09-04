#Company Name folder must exist as a folder in morningstarfinancials path in dropbox prior to files being downloaded
STOCK_QUERRY_LIST_PATH = 'C:/Users/micha/Dropbox/ProgrammingFiles/Present/PC/Midas3.3.2/Rscripts/StockQuerryList.csv'
MORNINGSTAR_PATH = 'C:/Users/micha/Dropbox/ProgrammingFiles/Present/Share/Input/MorningstarFinancials/'
YAHOO_HISTORIC_PATH = 'C:/Users/micha/Dropbox/ProgrammingFiles/Present/Share/Input/YahooHistorical/'

retrieve_morningstar <- function(STOCK_QUERRY_LIST_PATH, MORNINGSTAR_PATH,YAHOO_HISTORIC_PATH ){
  data  = read.csv(STOCK_QUERRY_LIST_PATH, header = TRUE, sep = ',', stringsAsFactors = FALSE)
  for (i in 1:nrow(data)){
    ticker = data$Stock[i]
    msex =  data$MSex[i]
    yex = data$Yex[i]
  
    #MORNINGSTAR BALANCE SHEET
    ms_bs1 = paste0('http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=', msex ,':')
    ms_bs2 = paste0(ticker,'&region=usa&culture=en-US&cur=&reportType=bs&period=12&dataType=A&order=asc&columnYear=5')
    ms_bs3 = paste0('&curYearPart=1st5year&rounding=3&view=raw&r=926076&denominatorView=raw&number=3')
    bs_url = paste0(ms_bs1, ms_bs2, ms_bs3)
    bs_out_path = paste0(MORNINGSTAR_PATH, '2017/', ticker, '/', ticker, ' Balance Sheet.csv')
    download.file(bs_url, bs_out_path, quiet = TRUE)#Quiet supreses the auto print output
    #MORNINGSTAR INCOME STATEMENT
    ms_is1 = paste0('http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=', msex ,':')
    ms_is2 = paste0(ticker,'&region=usa&culture=en-US&cur=&reportType=is&period=12&dataType=A&order=asc&columnYear=5')
    ms_is3 = paste0('&curYearPart=1st5year&rounding=3&view=raw&r=926076&denominatorView=raw&number=3')
    is_url = paste0(ms_is1, ms_is2, ms_is3)
    is_out_path = paste0(MORNINGSTAR_PATH, '2017/', ticker, '/', ticker, ' Income Statement.csv')
    download.file(is_url, is_out_path, quiet = TRUE)#Quiet supreses the auto print output
    
    #MORNINGSTAR Timestamp / DOWNLOAD INFORMATION / TIME STAMP
    dwnldinfo_path = paste0(MORNINGSTAR_PATH, '2017/', ticker, '/', ticker, 'Timestamp.txt')
    sink(dwnldinfo_path)
    print(Sys.Date())
    print(Sys.time())
    sink()
    
    print(ticker)
    print(bs_url)
  }
  print('...Morningstar Financials Process Complete...')
}




retrieve_morningstar(STOCK_QUERRY_LIST_PATH, MORNINGSTAR_PATH,YAHOO_HISTORIC_PATH)
#retrieve_yahoohistorical(STOCK_QUERRY_LIST_PATH, MORNINGSTAR_PATH,YAHOO_HISTORIC_PATH)
#retrieve_quantmod_historical(STOCK_QUERRY_LIST_PATH, YAHOO_HISTORIC_PATH)
