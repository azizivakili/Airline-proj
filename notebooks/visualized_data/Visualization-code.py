#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import numpy as np
import sqlite3
import pymysql
plt.style.use('ggplot')

# Load Dataframe from Database
def retrieve_data_from_mysql(host, user, password, database, table_name):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except pymysql.Error as e:
        print(f"Error: {e}")
        return None

def main():
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'AirlineDB'
    table_name = 'AirlinesDelayVisual'

    df = retrieve_data_from_mysql(host, user, password, database, table_name)
    if df is not None:
        return df
    else:
        print("Failed to retrieve data from MySQL.")

df = main()

# Convert numbers to float type. 
df['EA_Time_Minutes'] = df['EA_Time_Minutes'].replace('', np.nan).astype(float)
df['RA_Time_Minutes'] = df['RA_Time_Minutes'].replace('', np.nan).astype(float)
df['Delay_Time'] = df['Delay_Time'].replace('', np.nan).astype(float)

# Scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(df['EA_Time_Minutes'], df['RA_Time_Minutes'], c=df['Delay_Time'], s=30, cmap='viridis')
plt.colorbar(label='Delay Time')
plt.xlabel('EA_Time_Minutes')
plt.ylabel('RA_Time_Minutes')
plt.title('Scatter plot')
plt.show()

# Bar plot
plt.figure(figsize=(8, 6))
plt.bar(range(len(df)), df['EA_Time_Minutes'], label='EA_Time_Minutes')
plt.xlabel('Index')
plt.ylabel('EA_Time_Minutes')
plt.title('Bar plot')
plt.legend()
plt.show()

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].scatter(df['Delay_Time'], df['RA_Time_Minutes'], c='red', label="Delay_Time")
axes[0, 0].legend()

axes[0, 1].scatter(df['Delay_Predicted'], df['RA_Time_Minutes'], c='blue', label="Delay_Predicted")
axes[0, 1].legend()

axes[1, 0].hist(df['Delay_Time'], color='red', rwidth=0.8, label="Delay_Time")
axes[1, 0].legend()

axes[1, 1].hist(df['Delay_Predicted'], color='blue', rwidth=0.8, label="Delay_Predicted")
axes[1, 1].legend()

plt.show()

# Plot histograms separately
plt.figure(figsize=(10, 8))

plt.hist(df['Delay_Time'], bins=10, color='red', alpha=0.7, label="Delay_Time")
plt.hist(df['EA_Time_Minutes'], bins=10, color='blue', alpha=0.7, label="EA_Time_Minutes")
plt.hist(df['RA_Time_Minutes'], bins=10, color='green', alpha=0.7, label="RA_Time_Minutes")

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histograms')
plt.legend()
plt.show()

