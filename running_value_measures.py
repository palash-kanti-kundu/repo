import matplotlib.pyplot as plt
import pandas as pd
'''
fields = ['date', fields[1]]
df = pd.read_csv('data/DailyDelhiClimateTrain.csv',
                 parse_dates=['date'],
                 skipinitialspace=True,
                 usecols=fields, header=0, index_col=0)
'''

fields = ['Date', 'Value']
df = pd.read_csv('data/random_data.csv',
                 parse_dates=['Date'],
                 skipinitialspace=True,
                 usecols=fields, header=0, index_col=0)

# Calculate different rolling averages
df['6d'] = df[fields[1]].rolling(6).mean()
df['30d'] = df[fields[1]].rolling(30).mean()
df['60d'] = df[fields[1]].rolling(60).mean()

# Calculate the max and min of 30 day average
df['mean30'] = df[fields[1]].rolling(30).mean()
df['max30'] = df[fields[1]].rolling(30).max()
df['min30'] = df[fields[1]].rolling(30).min()

# Calculate Bollinger Band
bollinger_constant = 2
df['bbup'] = df['mean30'] + bollinger_constant * \
    df[fields[1]].rolling(30).std()
df['bbdown'] = df['mean30'] - bollinger_constant * \
    df[fields[1]].rolling(30).std()

upcrosses = df[df[fields[1]] > df['bbup']]
downcrosses = df[df[fields[1]] < df['bbdown']]

print(upcrosses)
print(downcrosses)

# Calculate Exponentially Weighted Moving Averages
df['ewm1'] = df[fields[1]].ewm(adjust=False, alpha=1).mean()
df['ewm0.5'] = df[fields[1]].ewm(adjust=False, alpha=0.5).mean()
df['ewm0.3'] = df[fields[1]].ewm(adjust=False, alpha=0.3).mean()
df['ewm0.2'] = df[fields[1]].ewm(adjust=False, alpha=0.2).mean()
df['ewm0.1'] = df[fields[1]].ewm(adjust=False, alpha=0.1).mean()

fig = plt.figure(figsize=(8, 6), dpi=65)

# Plot different moving averages
ax1 = fig.add_subplot(4, 1, 1)
ax1.plot(df[[fields[1], '6d', '30d', '60d']])
ax1.set_title("Data ")
ax1.legend(['Daily', '6D avg', '30D avg', '60D avg'])

# Plot Running Average with max and min
ax2 = fig.add_subplot(4, 1, 2)
ax2.plot(df[[fields[1], 'mean30', 'max30', 'min30']])
ax2.fill_between(x=df.index, y1=df['max30'].values,
                 y2=df['min30'].values, alpha=0.5)
ax2.legend(['Daily', '30D avg', 'Max', 'Min'])

# Plot Bollinger Band
ax3 = fig.add_subplot(4, 1, 3)
ax3.plot(df[[fields[1], 'mean30', 'bbup', 'bbdown']])
ax3.fill_between(x=df.index, y1=df['bbup'].values,
                 y2=df['bbdown'].values, alpha=0.5)
ymax, ymin = ax3.get_ylim()
ax3.vlines(x=upcrosses.index, ymax=ymax, ymin=ymin,
           colors='r', lw=0.2, alpha=0.4)
ax3.vlines(x=downcrosses.index, ymax=ymax,
           ymin=ymin, colors='b', lw=0.2, alpha=0.4)
ax3.legend(['Daily', '30D avg', 'Bollinger Max', 'Bollinger Min'])

# Plot Exponentially Weighted Moving Average
ax4 = fig.add_subplot(4, 1, 4)
ax4.plot(df[['ewm1', 'ewm0.5', 'ewm0.3', 'ewm0.1']])
ax4.legend(['ewm1', 'ewm0.5', 'ewm0.3', 'ewm0.1'])
plt.show()
