from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from typing import List
import numpy as np
app = FastAPI()

# Load the data for imputation
data = None

class Features(BaseModel):
    EA_Time_Minutes: float
    RA_Time_Minutes: float

class PredictionResult(BaseModel):
    prediction: List[float]


@app.post('/train')
def train_model():
    global model, data
    try:
        # Load the training data from file
        data = pd.read_csv("Final-data1.csv")
        data['EA_Time_Minutes'] = data['EA_Time_Minutes'].replace('', np.nan).astype(float)
        data['RA_Time_Minutes'] = data['RA_Time_Minutes'].replace('', np.nan).astype(float)
        data['Delay_Time'] = data['Delay_Time'].replace('', np.nan).astype(float)

        data['EA_Time_Minutes'].fillna(data['EA_Time_Minutes'].median(), inplace=True)
        data['RA_Time_Minutes'].fillna(data['RA_Time_Minutes'].median(), inplace=True)
        data['Delay_Time'].fillna(data['Delay_Time'].median(), inplace=True)

        # Prepare your data for training
        X_train = data[['EA_Time_Minutes', 'RA_Time_Minutes']]
        y_train = data['Delay_Time']

        # Drop rows with missing values in the target variable
        data.dropna(subset=['Delay_Time'], inplace=True)

        # Impute missing values in features
        imputer = SimpleImputer(strategy='mean')
        X_train_imputed = imputer.fit_transform(X_train)

        # Train the model
        model = LinearRegression()
        model.fit(X_train_imputed, y_train)

        return {'message': 'Model trained successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/predict', response_model=PredictionResult)
def predict(features: Features):
    global model, data
    if model is None:
        raise HTTPException(status_code=500, detail='Model not trained yet')

    try:
        # Prepare the data for prediction
        X = pd.DataFrame([features.dict()])
        
        # Impute missing values
        imputer = SimpleImputer(strategy='mean')
        X_imputed = imputer.fit_transform(X)
        
        # Make predictions
        prediction = model.predict(X_imputed)
        
        return {'prediction': prediction.tolist()}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
