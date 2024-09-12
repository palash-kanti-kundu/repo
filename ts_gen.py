import random
import pandas as pd
import numpy as np

def generate_ar(phi, initials, periods, c = 0):
    if len(initials) != len(phi):
        raise "Number of lags do not match, number of lagged co-efficients"
    if periods <= len(initials):
        raise "Number of lags and periods match, can not generate time series"
    
    lags = len(initials)
    x = initials
    phi.reverse()

    df = pd.DataFrame()
    df['Date'] = pd.date_range(end=pd.Timestamp.today(), periods=periods, freq="D")

    for i in range(len(initials), periods):
        newValue = c + random.random()
        for j in range(lags):
            sub = len(x) - j - 1
            newValue += phi[j] * x[sub] 
        x.append(newValue)
    df['TS_Value'] = x

    return df

def generate_ma(theta, periods, c = 0):
    err = np.random.random(size=periods)
    if periods <= len(theta):
        raise "Number of lags and periods match, can not generate time series"
    
    df = pd.DataFrame()
    df['Date'] = pd.date_range(end=pd.Timestamp.today(), periods=periods - len(theta), freq="D")
    x =[]

    for i in range(len(theta), periods):
        newValue = c + err[i]
        for j in range(len(theta)):
            sub = i - j - 1
            newValue += theta[j] * err[sub] 
        x.append(newValue)
    df['TS_Value'] = x

    return df
    

ts = generate_ar([0.2, 0.1, 0.05], [0, 0.5, 0.7], 728, 5)

ma = generate_ma([0.5, 0.2], 730, 8)

arma = pd.DataFrame()
arma['Date'] = pd.date_range(end=pd.Timestamp.today(), periods=728, freq="D")
arma['TS_Value'] = ts['TS_Value'] 
arma.to_csv('time_series_arima.csv')
print(arma)