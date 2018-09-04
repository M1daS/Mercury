'''
Created on Jul 20, 2017

@author: michaelsands
'''
'''
Created on Jul 17, 2017

@author: micha
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
path = 'C:/Users/micha/Dropbox/EclipsePC_Workspace/RetrievedFinancialData/YahooHistorical/^GSPC.csv'
df = pd.read_table(path, sep = ',')
df['Date'] = pd.to_datetime(df['Date'])

#add moving avrages to our df of data
df['MA42']= np.round(df['Close'].rolling(window=50).mean(),2)
df['MA252']= np.round(df['Close'].rolling(window=252).mean(),2)


df['MAdiff'] = df['MA42'] - df['MA252']
diff_goal = 15
df['Stance'] = np.where(df['MAdiff'] > diff_goal, 1, 0)
df['Stance'] = np.where(df['MAdiff'] < diff_goal, -1, df['Stance'])
df['Stance'].value_counts()

df['Market Returns'] = np.log(df['Close'] / df['Close'].shift(1))
df['Strategy'] = df['Market Returns'] * df['Stance'].shift(1)
print(df)


fig = plt.figure()

ax1 = fig.add_subplot(211)
ax1.plot(df['Date'], df['Close'], 'b-', label = 'Close', color = 'blue')
ax1.plot(df['Date'], df['MA42'], '--', label = '42 day MA', color = 'green')
ax1.plot(df['Date'], df['MA252'], '-.', label = '252 day MA', color = 'orange')
ax1.legend(loc='best')

ax2 = fig.add_subplot(212)
ax2.plot(df['Date'], df['Market Returns'].cumsum(), 'b-', label = 'MktReturn', color = 'blue')
ax2.plot(df['Date'], df['Strategy'].cumsum(), ':', label = 'Strategy', color = 'green') #cumulative sum
ax2.legend(loc='best')

plt.show()




'''RULES
 buy - if 42 day is x points above the 200 day
otherwise hold
or sell if 42 is x points below the 200 day
'''



