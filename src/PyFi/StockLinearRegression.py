import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


path = 'C:/Users/research/Dropbox/BABA.csv'
dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
file = pd.read_csv(path,  parse_dates=['Date'], date_parser=dateparse)
df = file[['Date','Close']]
dates = df['Date']
# df = df.set_index(['Date']).groupby(pd.TimeGrouper('M')).mean() #Groups by the average value of each month



#Linear Regression Model
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm
df = df[['Close']]

forecast_out = int(50) #Forecasting Period n(days)

df['Prediction'] = df[['Close']].shift(-forecast_out) 
X = np.array(df.drop(['Prediction'], 1))
X = preprocessing.scale(X)
X_forecast = X[-forecast_out:] 
X = X[:-forecast_out] 
y = np.array(df['Prediction'])
y = y[:-forecast_out]


X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.2)

# Training
clf = LinearRegression()
clf.fit(X_train,y_train)

# Testing
confidence = clf.score(X_test, y_test)
print("confidence: ", confidence)

forecast_prediction = clf.predict(X_forecast)



#Combine Forecast and Historical Data
finallist = []
for item in df['Close'].tolist():
	finallist.append(item)
for item in forecast_prediction:
	finallist.append(item)

lastdate = dates.ix[len(dates) - 1]
datelist = []
for item in dates:
	datelist.append(item)
for i in range(forecast_out):
	nextdate =lastdate + pd.DateOffset(i+1)
	datelist.append(nextdate)
#Plot
forecast = plt.plot(datelist, finallist,  color = 'pink')
historical = plt.plot(dates, df['Close'], color = 'blue')

outputDf = pd.DataFrame()
outputDf['Date'] = datelist[-10:]
outputDf['Forecast'] = finallist[-10:]
outputDf = outputDf.set_index(['Date'])
print(outputDf)



plt.title('Linnear Regression')
plt.legend(['Forecast','Historical'])
plt.show()


