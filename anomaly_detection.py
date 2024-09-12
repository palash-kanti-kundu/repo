import pandas as pd
from adtk.data import validate_series
from adtk.visualization import plot
from adtk.detector import SeasonalAD

def analyse_timeseries(df, name, column):
    print(df)
    s_train = validate_series(df)
    seasonal_ad = SeasonalAD()
    anomalies = seasonal_ad.fit_detect(s_train)
    print("Anomalies")
    print(anomalies)
