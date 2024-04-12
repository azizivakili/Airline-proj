#!/usr/bin/env python
# coding: utf-8
from sklearn.metrics import r2_score, mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
#from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
import pandas as pd
import datetime
import numpy as np
import sqlite3
import pymysql


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
    table_name = 'AirlinesDelay'

    df = retrieve_data_from_mysql(host, user, password, database, table_name)
    if df is not None:
        return df
    else:
        print("Failed to retrieve data from MySQL.")
df = main()

df.drop(['Origin', 'Destination'], axis=1, inplace=True)

df[['Aircraft', 'Departure_Date', 'Departure_Time', 'Arrival_Date', 'Arrival_Time']] = df[['Aircraft','Departure_Date','Departure_Time', 'Arrival_Date', 'Arrival_Time']].apply(lambda x: x.astype('category').cat.codes)

# Convert numbers to float type. 
df['EA_Time_Minutes'] = df['EA_Time_Minutes'].replace('', np.nan).astype(float)
df['RA_Time_Minutes'] = df['RA_Time_Minutes'].replace('', np.nan).astype(float)
df['Delay_Time'] = df['Delay_Time'].replace('', np.nan).astype(float)

df['EA_Time_Minutes'].fillna(df['EA_Time_Minutes'].median(), inplace=True)
df['RA_Time_Minutes'].fillna(df['RA_Time_Minutes'].median(), inplace=True)
df['Delay_Time'].fillna(df['Delay_Time'].median(), inplace=True)

# Step 1: Train a model

#  a simple linear regression model
x = df[['EA_Time_Minutes', 'RA_Time_Minutes']] # feature variable 
y = df['Delay_Time']  # Target variable

x_train , x_test , y_train , y_test = train_test_split(x,y , test_size=0.3 , random_state=0 )


# In[378]:


from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(x_train , y_train)

# now see the parameters the y intercept 

#### coefficients close to 1 or very close to 0 indicates that the feature variables
#('EA_Time_Minutes' and 'RA_Time_Minutes')are likely good predictors for the target variable ('Delay_Time').

c = lr.intercept_
c

m = lr.coef_
m

# Step 2: Make predictions on the "to_predict" DataFrame
to_predict_features = df[['EA_Time_Minutes', 'RA_Time_Minutes']]
predictions = lr.predict(to_predict_features)

predictions

# Step 3: Create a new DataFrame to store the predicted results
predicted = pd.DataFrame({
    'Flight ID': df['Aircraft'],
    'Delay Predicted': predictions,
    'Departure_Time':df['Departure_Time'],
    'Date of Prediction': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
})

# Display the "predicted" DataFrame
print(predicted)

predicted.to_csv("All_rows_predicted_table.csv")

# Save predicted table back to the SQL server. 
#%pip install sqlalchemy
#%pip install mysql-connector-python

conn_str = 'mysql+mysqlconnector://root:root@localhost/AirlineDB'
engine = create_engine(conn_str)
predicted.to_sql(name='FlightPredictions', con=engine, if_exists='replace', index=False)
engine.dispose()

import matplotlib.pyplot as plt

# Plotting the actual vs predicted values
plt.scatter(y_train, predictions[:len(y_train)], color='blue', label='Actual vs Predicted')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, color='red', label='Ideal Line')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted Values')
plt.legend()
plt.show()

# Assuming lr is your linear regression model
predictions = lr.predict(x)  # X is your feature matrix

# Calculate R-squared value
r_squared = r2_score(y, predictions)

# Calculate mean squared error
mse = mean_squared_error(y, predictions)


# Calculate variance inflation factors (VIF) to check for multicollinearity
vif = pd.DataFrame()
vif["Features"] = x.columns
vif["VIF"] = [variance_inflation_factor(x.values, i) for i in range(x.shape[1])]

print("R-squared:", r_squared)
print("Mean Squared Error:", mse)
print("Variance Inflation Factors:")
print(vif)

#                             ***  Second Part of the project  ***

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer

#Create DataFrame
data = pd.read_csv("Final-data1.csv")
df = pd.DataFrame(data)

# Split the data into two sets: one with missing "Delay_Time" for prediction and one with available "Delay_Time" for training
df_missing = df[df['Delay_Time'].isnull()].copy()
df_train = df.dropna(subset=['Delay_Time']).copy()

# Impute missing values in features
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(df_train[['EA_Time_Minutes', 'RA_Time_Minutes']])
y_train = df_train['Delay_Time']

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the "Delay_Time" for the missing values
X_missing = imputer.transform(df_missing[['EA_Time_Minutes', 'RA_Time_Minutes']])
predicted_delay_time = model.predict(X_missing)
# Combine the predicted "Delay_Time" with the relevant aircraft information
df_missing['Predicted_Delay_Time'] = predicted_delay_time

# Save the combined DataFrame to a CSV file
df_missing.to_csv('predicted_delay_MissingArrival.csv', index=False)
# Save predicted table back to the SQL server. 
#%pip install sqlalchemy
#%pip install mysql-connector-python


conn_str = 'mysql+mysqlconnector://root:root@localhost/AirlineDB'
engine = create_engine(conn_str)
df_missing.to_sql(name='predicted_delay_MissingArrival', con=engine, if_exists='replace', index=False)
engine.dispose()


# Plotting the predictions
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_train, x='EA_Time_Minutes', y='Delay_Time', label='Actual Delay_Time')
sns.scatterplot(data=df_missing, x='EA_Time_Minutes', y='Predicted_Delay_Time', label='Predicted Delay_Time')
plt.xlabel('EA_Time_Minutes')
plt.ylabel('Predicted_Delay_Time')
plt.title('Predicted vs Actual Delay_Time')
plt.legend()
plt.grid(True)
plt.show()
 
