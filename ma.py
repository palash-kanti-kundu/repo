import matplotlib.pyplot as plt
import pandas as pd

def analyse_timeseries(df, field, name, showPlot = True):
    # disable chained assignments
    pd.options.mode.chained_assignment = None 
    
    df['6'] =  df[field].rolling(6).mean()

    df['mean6'] = df[field].rolling(6).mean()
    df['max6'] = df[field].rolling(6).max()
    df['min6'] = df[field].rolling(6).min()

    

    # Calculate Exponentially Weighted Moving Averages
    df['ewm1'] = df[field].ewm(adjust=False, alpha=1).mean()
    df['ewm0.5'] = df[field].ewm(adjust=False, alpha=0.5).mean()
    df['ewm0.3'] = df[field].ewm(adjust=False, alpha=0.3).mean()
    df['ewm0.2'] = df[field].ewm(adjust=False, alpha=0.2).mean()
    df['ewm0.1'] = df[field].ewm(adjust=False, alpha=0.5).mean()

    # Calculate Bollinger Band
    bollinger_constant = 3
    #df['bbup']      = df['mean6'] + bollinger_constant * df[field].rolling(6).std()
    #df['bbdown']    = df['mean6'] - bollinger_constant * df[field].rolling(6).std()

    df['bbup']      = df['ewm0.1'] + bollinger_constant * df['ewm0.1'].std()
    df['bbdown']    = df['ewm0.1'] - bollinger_constant * df['ewm0.1'].std()

    upcrosses = df[df[field] > df['bbup']]
    downcrosses = df[df[field] < df['bbdown']]

    anomaly = not (upcrosses.empty and downcrosses.empty)
    #print(name, anomaly)

    if showPlot and anomaly:
        fig = plt.figure(figsize=(20, 15))

        # Plot different moving averages
     

        # Plot Running Average with max and min
  
        # Plot Bollinger Band
        ax3 = fig.add_subplot(1, 1, 1)
        ax3.plot(df[[field, 'mean6', 'bbup', 'bbdown']])
        ax3.fill_between(x=df.index, y1=df['bbup'].values,
                        y2=df['bbdown'].values, alpha=0.5)
        ymax, ymin = ax3.get_ylim()
        ax3.vlines(x=upcrosses.index, ymax=ymax, ymin=ymin,
                colors='r', lw=0.2, alpha=0.4)
        ax3.vlines(x=downcrosses.index, ymax=ymax,
                ymin=ymin, colors='b', lw=0.2, alpha=0.4)
        ax3.scatter(upcrosses.index, upcrosses[field], color='r', marker='D')
        ax3.scatter(downcrosses.index, downcrosses[field], color='r', marker='D')
        ax3.legend(['Hourly', 'EWM Analysis', 'Max Limit', 'Min Limit'])
        ax3.set_title("Data with anomaly for " + name)
       
        plt.show(block=False)

    return anomaly