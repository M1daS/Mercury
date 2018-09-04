# =    /home/msands/Dropbox/ProgrammingFiles/Present/Linux/DjangoDirectory/Midas104/Midas104


import os





p_PATHFILE = os.path.abspath('Mercury/Pathsfile.py')
p_MYMODULES = os.path.dirname(os.path.abspath('src/PyFi/NewsRSS.py'))
p_CryptoMODULES = os.path.dirname(os.path.abspath('src/PyCrypto/Correlate.py'))


p_Cookies = os.path.dirname(os.path.abspath('Mercury/Cookies/Cookies.csv'))




p_historic = os.path.dirname(os.path.abspath('src/DataFiles/Historical/historical.txt'))
p_HISTORICAL_DATA = p_historic + '/'

p_financial = os.path.dirname(os.path.abspath('src/DataFiles/Financial/financial.txt'))
p_FINANCIAL_DATA = p_financial + '/'

p_output = os.path.dirname(os.path.abspath('src/DataFiles/ProgramOutput/programoutput.txt'))
p_PRGM_OUTPUT = p_output + '/'


p_cryptohistoric = os.path.dirname(os.path.abspath('src/DataFiles/CryptoData/USDT_BTC_300.csv'))
p_CRYPTO_DATA = p_cryptohistoric + '/'