import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import STL
from datetime import datetime
from statsmodels.tsa.seasonal import STL
from datetime import datetime


def analyse_timeseries(df, valueColumn, name):
    print("\n\n\n==========================================================")
    print("$$$$----", name, "----$$$$")

    # Checking ACF and PACF
    fig = plt.figure(figsize=(8, 6), dpi=65)
    
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(df)
    ax1.set_title("Data " + name )

    ax2 = fig.add_subplot(2, 2, 3)
    ax3 = fig.add_subplot(2, 2, 4)
    plot_acf(df.values, lags=12, ax=ax2)
    plot_pacf(df.values, ax=ax3)
    plt.show(block=False)

    res = adfuller(df.values)

    print('Augmneted Dickey_fuller Statistic: %f' % res[0])
    print('p-value: %f' % res[1])
    print('critical values at different levels:')
    for k, v in res[4].items():
        print('\t%s: %.3f' % (k, v))
    df = df.asfreq(pd.infer_freq(df.index))
    stl = STL(df, period=30)
    result = stl.fit()
    seasonal, trend, resid = result.seasonal, result.trend, result.resid

    plt.figure(figsize=(8, 6), dpi=65)

    plt.subplot(4, 1, 1)
    plt.plot(df)
    plt.title('Original Series ' + name, fontsize=16)
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)

    plt.subplot(4, 1, 2)
    plt.plot(trend)
    plt.title('Trend', fontsize=16)
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)

    plt.subplot(4, 1, 3)
    plt.plot(seasonal)
    plt.title('Seasonal', fontsize=16)
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)

    plt.subplot(4, 1, 4)
    plt.plot(resid)
    plt.title('Residual', fontsize=16)
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)

    plt.tight_layout()

    estimated = trend + seasonal
    plt.figure(figsize=(8, 6), dpi=65)

    plt.subplot(3, 1, 1)
    plt.plot(df)
    plt.plot(estimated)
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)
    plt.title("Estimated Decomposition with original data " + name)
    
    resid_mu = resid.mean()
    resid_dev = resid.std()

    lower = resid_mu - 1.2*resid_dev
    upper = resid_mu + 1.2*resid_dev

    plt.subplot(3, 1, 2)
    plt.plot(resid)
    plt.title('Residuals with error range')
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)
    print(df.first_valid_index(), df.last_valid_index(), lower, upper)
    plt.fill_between([df.first_valid_index(), df.last_valid_index()],
                     lower, upper, color='g',
                     alpha=0.25, linestyle='--', linewidth=2)
    #plt.xlim(df.first_valid_index(), df.last_valid_index())

    anomalies = df[(resid < lower) | (resid > upper)]
    plt.show()
    print("Anomalies detected")
    input("Press any key to continue")
    print(anomalies)

    plt.subplot(3, 1, 3)
    plt.plot(df)
    add_year_lines(df.first_valid_index().year, df.last_valid_index().year)

    plt.scatter(anomalies.index, anomalies[valueColumn], color='r', marker='D')
    plt.title("Data with Anomalies")
    plt.show(block=False)

    print("\n\nFollowing are estimated anomalies in this series")
    print(anomalies)
    
    print("==========================================================\n\n\n")

def add_year_lines(start_year, end_year):
    for year in range(start_year, end_year):
        plt.axvline(datetime(year, 1, 1), color='k', linestyle='--', alpha=0.5)

df = pd.read_csv('time_series_arma.csv', parse_dates=['Date'],
                skipinitialspace=True,
                usecols=['Date', 'TS_Value'], header=0, index_col=0)

analyse_timeseries(df, 'TS_Value', 'Value')