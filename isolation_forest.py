from sklearn.ensemble import IsolationForest
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json

def add_year_lines(start_year, end_year):
    for year in range(start_year, end_year):
        plt.axvline(datetime(year, 1, 1), color='k', linestyle='--', alpha=0.5)

def analyse_timeseries(df, valueColumn, contamination_estimate, name, showPlot=True):

    model = IsolationForest(n_estimators=100, max_samples='auto', contamination=contamination_estimate, max_features=1.0)
    model.fit(df[[valueColumn]])

    df['model_anomaly_score'] =  model.decision_function(df[[valueColumn]])
    df['anomaly'] = model.predict(df[[valueColumn]])<0

    print("Anomalies for", name)
    #print(df)

    df_a = df[df['anomaly']]
    
    anomaly_exists = not df_a[df_a.anomaly == True].empty
    
    #print(df_a, anomaly_exists)

    if showPlot and anomaly_exists:
        plt.figure(figsize=(8, 6), dpi=65)

        plt.plot(df[valueColumn])
        add_year_lines(df.first_valid_index().year, df.last_valid_index().year)

        plt.scatter(df_a.index, df_a[valueColumn], color='r', marker='D')
        plt.title("Data with Anomalies for " + name)
        plt.show(block=False)

    if anomaly_exists:
        pass #df_a.to_csv('Isolation_Forest_anomaly_'+ name +'.csv')

    return anomaly_exists

