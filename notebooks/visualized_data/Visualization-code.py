#!/usr/bin/env python
# coding: utf-8

# In[3]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import numpy as np
import sqlite3
import pymysql
plt.style.use('ggplot')


# In[4]:


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


# In[5]:


# Convert numbers to float type. 
df['EA_Time_Minutes'] = df['EA_Time_Minutes'].replace('', np.nan).astype(float)
df['RA_Time_Minutes'] = df['RA_Time_Minutes'].replace('', np.nan).astype(float)
df['Delay_Time'] = df['Delay_Time'].replace('', np.nan).astype(float)


# In[6]:


fig = plt.figure(figsize=(10,10))

plt.subplot(221)
plt.bar(range(len(df)), df.EA_Time_Minutes, label = 'RA_Time_Minutes')
plt.legend()

plt.subplot(222)
plt.scatter(df.Delay_Time , df.RA_Time_Minutes, c = 'red', label = "Delay_Time")
plt.legend()

plt.subplot(222)
plt.scatter(df.Delay_Predicted , df.RA_Time_Minutes, c = 'blue', label = "Delay_Predicted")
plt.legend()

plt.subplot(224)
plt.hist(df.Delay_Predicted, color='blue', rwidth = 0.8, label = "Delay_Predicted");
plt.legend();

plt.subplot(224)
plt.hist(df.Delay_Time, color='red', rwidth = 0.8, label = "Delay_Time");
plt.legend();


# In[13]:


plt.hist([df.EA_Time_Minutes, df.RA_Time_Minutes , df.Delay_Time], bins = 6, color = ['#f27750', '#f7bf59', '#f7bf94'],
         label = ['EA_Time_Minutes', 'RA_Time_Minutes' , 'Delay_Predicted'])
plt.ylabel('Frequency')
plt.xlabel('Time')
plt.title('Delay Estimation')
plt.legend();


# In[14]:


df.plot.hist(y=['EA_Time_Minutes', 'Delay_Predicted'], bins = 7, rwidth = 0.8 , color= ['#0c4c83', '#830c4c'], alpha=0.5);

df.plot.hist(y=['RA_Time_Minutes', 'Delay_Predicted'], bins = 7, rwidth = 0.8 , color= ['#0c4c83', '#830c4c'], alpha=0.5);

df.plot.hist(y=['EA_Time_Minutes', 'RA_Time_Minutes'], bins = 7, rwidth = 0.8 , color= ['#0c4c83', '#830c4c'], alpha=0.5);

