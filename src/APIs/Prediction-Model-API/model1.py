import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
import pickle
import joblib


# Step 1: Data Collection
# Assuming you have a dataset named 'flight_data.csv'
data = pd.read_csv('Final-data1.csv')

# Step 2: Data Preprocessing
# Convert numbers to float type. 
data['EA_Time_Minutes'] = data['EA_Time_Minutes'].replace('', np.nan).astype(float)
data['RA_Time_Minutes'] = data['RA_Time_Minutes'].replace('', np.nan).astype(float)
data['Delay_Time'] = data['Delay_Time'].replace('', np.nan).astype(float)



data['EA_Time_Minutes'].fillna(data['EA_Time_Minutes'].median(), inplace=True)
data['RA_Time_Minutes'].fillna(data['RA_Time_Minutes'].median(), inplace=True)
data['Delay_Time'].fillna(data['Delay_Time'].median(), inplace=True)


# Handle missing values, encode categorical variables, etc.

# Step 3: Feature Engineering
# Extract relevant features or create new features

# Step 4: Model Selection
#model = RandomForestRegressor()

# Step 5: Model Training


x = data[['EA_Time_Minutes', 'RA_Time_Minutes']] # feature variable 
y = data['Delay_Time']

x_train , x_test , y_train , y_test = train_test_split(x,y , test_size=0.3 , random_state=0 )


lr = LinearRegression()
lr.fit(x_train , y_train)

c = lr.intercept_

m = lr.coef_

# Step 6: Model Evaluation
to_predict_features = data[['EA_Time_Minutes', 'RA_Time_Minutes']]
predictions =  lr.predict(to_predict_features)



# Step 7: Model Saving
with open('model.pkl', 'wb') as f:
    pickle.dump(lr, f)

joblib.dump(lr, 'model.pkl')
