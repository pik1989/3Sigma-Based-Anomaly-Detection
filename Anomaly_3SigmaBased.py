# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:37:05 2019

@author: 611840750
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime


df = pd.read_csv('files/export_26550776.csv') 
df = pd.DataFrame(df, columns=['CREATED_TIMESTAMP', 'METRIC_VALUE_FLOAT'])


df['time'] = df['CREATED_TIMESTAMP']

df['time'] = pd.to_datetime(pd.Series(df['time']), format="%d-%b-%y %I.%M.%S %p")
df = df.rename(columns={"METRIC_VALUE_FLOAT": "cnt"})

df.index = df.time
df.head()


df['weekday'] = df.time.dt.weekday
df.head()


df['hour'] = df.time.dt.hour
df.head()


def day_splitter(df):
    l = []
    for day in range(7):
        d = df[df['weekday']==day]
        l.append(d)
    return l

dfs = day_splitter(df)
len(dfs)


print(len(dfs[0]))
dfs[0].head()


def hour_splitter(df):
    l = []
    for hour in range(24):
        try:
            d = df[df['hour']==hour]
            l.append(d)
        except KeyError: pass
    return l


def get_dfs(dfs):
    l = []
    for df in dfs:
        l.extend(hour_splitter(df))
    return l



def anomaly_detector(df):
    m, s = df.mean()[0], df.std()[0]
    cutoff = s*3
    lower, upper = m - cutoff, m + cutoff
    anomalies = df['cnt'].apply(lambda x: x<lower or x>upper)
    idx = anomalies.values.reshape(-1)
    return idx

final_dfs = get_dfs(dfs)

len(final_dfs)

anomaly = []


for f_df in final_dfs:
    l = anomaly_detector(f_df)
    for i in range(len(l)):
        if l[i]: 
            d_time = f_df.iloc[i].time
            anomaly.append(d_time)
            
            
df['SerialNo'] = range(len(df))
df.head()


a = []
for l in df.time.tolist():
    if l in anomaly: a.append(1)
    else: a.append(0)
    
    
df['anomaly'] = a


no_anomaly_df = df[df.anomaly==0].sort_values('time')
anomaly_df = df[df.anomaly==1].sort_values('time')
len(anomaly_df), len(no_anomaly_df)


fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(no_anomaly_df['SerialNo'], no_anomaly_df['cnt'], color='blue', label='Normal')
ax.scatter(anomaly_df['SerialNo'], anomaly_df['cnt'], color='red', label='Anomaly')
plt.title('Anomalies')
plt.xlabel('Date Time integer')
plt.ylabel('Count')
plt.legend()
plt.show()

anomaly_df.to_csv('files/3SigmaAnomaly.csv')

import plotly.graph_objs as go
import plotly.offline as py
#Plot predicted and actual line graph with X=dates, Y=Outbound
actual_chart = go.Scatter(x=no_anomaly_df['SerialNo'], y=no_anomaly_df['cnt'], name= 'Data without Anomalies')
predict_chart = go.Scatter(x=anomaly_df['SerialNo'], y=anomaly_df['cnt'], name= 'Anomalies', mode='markers')
orig_chart = go.Scatter(x=df['SerialNo'], y=df['cnt'], name= 'Original Data')
py.plot([actual_chart, predict_chart, orig_chart])