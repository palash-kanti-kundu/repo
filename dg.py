import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from scipy import signal

def generate_time_series(json_file):
    with open(json_file, 'r') as f:
        config = json.load(f)

    freq_map = {'daily': 'D', 'monthly': 'M', 'yearly': 'Y'}
    freq = freq_map[config['frequency']]
    periods = config['periods']

    df = pd.DataFrame()
    df['ds'] = pd.date_range(end=pd.Timestamp.today(), periods=periods, freq=freq)

    for column in config['columns']:
        col_name = column['name']
        value_range = column.get('value_range', [0, 100])
        trend = column.get('trend', None)
        seasonality = column.get('seasonality', None)
        anomaly_percent = column.get('anomaly_percent', 0)

        data = np.random.uniform(value_range[0], value_range[1], periods)

        if trend == 'upwards':
            trend_values = np.linspace(value_range[0], value_range[1], periods)
            data += trend_values
        elif trend == 'downwards':
            trend_values = np.linspace(value_range[1], value_range[0], periods)
            data += trend_values
        elif trend == None:
            pass

        if seasonality:
            season_length = seasonality['length']
            if seasonality['type'] == 'sinusoidal':
                data += np.sin(np.linspace(0, 2*np.pi*periods/season_length, periods))
            elif seasonality['type'] == 'sawtooth':
                data += signal.sawtooth(np.linspace(0, 2*np.pi*periods/season_length, periods))
            elif seasonality['type'] == 'square':
                data += signal.square(np.linspace(0, 2*np.pi*periods/season_length, periods))

        num_anomalies = int(anomaly_percent * periods / 100)
        anomaly_shift = np.random.uniform(0.4*value_range[1], 0.7*value_range[1], num_anomalies)
        anomaly_indices = np.random.choice(periods, num_anomalies, replace=False)
        data[anomaly_indices] += np.random.choice([-1, 1], num_anomalies) * anomaly_shift  # Anomalies on both sides of the value range

        df[col_name] = data
        df[col_name + '_is_anomaly'] = False
        df.loc[anomaly_indices, col_name + '_is_anomaly'] = True
    
    df['Date'] = df['ds'].dt.date
    df.to_csv('time_series_data.csv', index=False)
    
    plt.figure(figsize=(10, 6), dpi = 65)
    for column in config['columns']:
        col_name = column['name']
        plt.plot(df['ds'], df[col_name], label=col_name, color='orange')
        plt.scatter(df[df[col_name + '_is_anomaly']]['ds'], df[df[col_name + '_is_anomaly']][col_name], color='g', marker='D')
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Generated Time Series Data")
    plt.legend()
    plt.grid(True)
    plt.show()

    

generate_time_series('dg_config.json')
