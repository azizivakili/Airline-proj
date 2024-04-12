#!/usr/bin/env python
# coding: utf-8

import pandas as pd
#pd.set_option('max_columns', 200)

data = pd.read_csv("Airline_Fr320-Mar04-Mar09-2024.csv")
df = pd.DataFrame(data) 

# Columns info
df.count()

# show the rows and columns
df.shape

df.describe()

df.dtypes


#show null or missing values 
#df.isna()
df.isna().sum()


#df.loc[df.duplicated()]
df.duplicated(subset = ['Destination'])


# Data cleaning  /                       checked for no duplicate
df = df.drop_duplicates()
df


# delete the following row  
df = df[df['Aircraft'] != 'XLE903']
#show null values 
df[df.isnull().any(axis=1)]

#df.reset_index(drop = True).copy()

days_to_dates = {
    "Mon": "04.03.2024",
    "Tue": "05.03.2024", 
    "Wed": "06.03.2024",
    "Thu": "07.03.2024",
    "Fri": "08.03.2024",
    "Sat": "09.03.2024", 
    "Sun": "10.03.2024"
}

# Process "Departure Time" and "Arrival Time" columns
df['Departure Date'] = df['Departure Time'].apply(lambda x: days_to_dates[x.split()[0]] if x.split()[0] in days_to_dates else x)
df


def convert_day_to_date(day):
    if day == 'Mon':
        return '04.03.2024'
    elif day == 'Tue':
        return '05.03.2024'
    elif day == 'Wed':
        return '06.03.2024'
    elif day == 'Thu':
        return '07.03.2024'
    elif day == 'Fri':
        return '08.03.2024'
    elif day == 'Sat':
        return '09.03.2024'
    elif day == 'Sun':
        return '10.03.2024'
    
df['Arrival Date'] = df['Arrival Time'].str.split().str[0].apply(convert_day_to_date)
df.to_csv("extract_dates.csv")
df

df = df[['Aircraft','Flight Type','Origin',
'Destination', 'Departure Date', 'Departure Time', 'Arrival Date', 'Arrival Time', 'Estimated Arrival Time', 'RealArrivalTime']]
df

df['Departure_Time'] = df['Departure Time'].str.extract(r'(\d+:\d+[APMapm]+)')
df.head(3)



#Regex 
df['Arrival_Time'] = df['Arrival Time'].str.extract(r'(\d+:\d+[APMapm]+)')
df.head(3)


df = df.drop(columns=['Departure Time', 'Arrival Time'])
df


df = df[['Aircraft','Flight Type','Origin',
'Destination', 'Departure Date', 'Departure_Time', 'Arrival Date', 'Arrival_Time', 'Estimated Arrival Time', 'RealArrivalTime']]
df


df.shape

# Convert "Estimated Arrival Time" to minutes
df['Estimated Arrival Time'] = pd.to_timedelta(df['Estimated Arrival Time'])
df['EA_Time_Minutes'] = df['Estimated Arrival Time'].dt.total_seconds() / 60
# Print the result DataFrame


# Convert "RealArrivalTime" to minutes
df['RA_Time_Minutes'] = df['RealArrivalTime'].apply(lambda x: sum(int(i[:-1]) * (60 if i.endswith('h') else 1) for i in x.split()))

# Display the DataFrame

df['Delay_Time'] = df['RA_Time_Minutes'] - df['EA_Time_Minutes']


df.to_csv("Final-data.csv")




