import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

df = pd.read_csv('../data/jj.csv')
train = df[:-4]
test = df[-4:]
historical_mean = np.mean(train['data'])
last_year_mean = np.mean(train.data[-4:])

test.loc[:, 'pred_mean'] = historical_mean 
test.loc[:, 'last_year_mean'] = last_year_mean 
test.loc[:, 'pred_last'] = train.data.iloc[-1]
test.loc[:, 'pred_last_season'] = train['data'][-4:].values

mape_hist_mean = mape(test['data'], test['pred_mean'])
mape_last_year_mean = mape(test['data'], test['last_year_mean'])
mape_last = mape(test['data'], test['pred_last'])
mape_last_season = mape(test['data'], test['pred_last_season'])

print("MAPE with Historical Mean", mape_hist_mean)
print("MAPE with last year mean", mape_last_year_mean)
print("MAPE with last value", mape_last)
print("MAPE with last season", mape_last_season)

fig, ax = plt.subplots()
 
ax.plot(train['date'], train['data'], 'g-.', label='Train')
ax.plot(test['date'], test['data'], 'b-', label='Test')
ax.plot(test['date'], test['pred_mean'], 'r--', label='Predicted by mean')
ax.plot(test['date'], test['last_year_mean'], 'd--', label='Predicted by Last Year Mean')
ax.plot(test['date'], test['pred_last'], 'o--', label='Predicted by Last Value')
ax.plot(test['date'], test['pred_last_season'], 'b--', label='Predicted by Last Season')
ax.set_xlabel('Date')
ax.set_ylabel('Earnings per share (USD)')
ax.axvspan(80, 83, color='#808080', alpha=0.2)
ax.legend(loc=2)
 
plt.xticks(np.arange(0, 85, 8), [1960, 1962, 1964, 1966, 1968, 1970, 1972, 1974, 1976, 1978, 1980])
 
fig.autofmt_xdate()
plt.tight_layout()
plt.show()

