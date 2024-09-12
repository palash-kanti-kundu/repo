import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf

np.random.seed(42)

# A generic Time Series yt = C + α1yt–1 + ϵt
def generate_series(C, alpha, first_value = 0):
    n = 100
    y = [0]*n
    y[0] =  first_value
    e = np.random.standard_normal(n)

    for i in range(n - 1):
        y[i + 1] = C + alpha * y[i] + e[i + 1]
    
    return y

def mean_over_time(process: np.array) -> np.array:
    mean_func = []
    
    for i in range(len(process)):
        mean_func.append(np.mean(process[:i]))
    
    return mean_func

def adf_acf(series, name):
    print("ADF statistics for", name)
    ADF_result = adfuller(series)

    print(f'ADF Statistic: {ADF_result[0]}')
    print(f'p-value: {ADF_result[1]}')
    plot_acf(series, lags=20, title = "ACF of " + name)
    print("\n")

non_stat_series = generate_series(0, 1, 100)
stat_series = generate_series(0, 0.5, 100)
diff_non_stat_series = np.diff(non_stat_series, n = 2)

adf_acf(stat_series, "Generated Stationary Series") 
adf_acf(non_stat_series, "Generated Non-Stationary Series") 
adf_acf(diff_non_stat_series, "Difference of Non-Stationary Series") 

fig, ax = plt.subplots()
 
ax.plot(stat_series, label = "Non-Stationary")
ax.plot(non_stat_series, label = "Stationary")
ax.plot(diff_non_stat_series, label = "Non Stationary Diff")
ax.set_xlabel('Timesteps')
ax.set_ylabel('Value')
ax.legend(loc=2)
 
plt.tight_layout()
plt.show()
