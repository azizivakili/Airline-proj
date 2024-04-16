import pytest
from fastapi.testclient import TestClient
from model1 import app  # assuming your FastAPI app instance is named 'app'
from model1 import Features

client = TestClient(app)

@pytest.fixture(scope="module")
def trained_model():
    client.post("/train")
    yield
    # Clean up after the tests if necessary

def test_train_model():
    response = client.post("/train")
    assert response.status_code == 200
    assert response.json() == {"message": "Model trained successfully"}

@pytest.mark.usefixtures("trained_model")
def test_predict():
    # Assuming your model predicts a delay, test prediction endpoint with some sample data
    features = Features(EA_Time_Minutes=10.0, RA_Time_Minutes=20.0)
    response = client.post("/predict", json=features.dict())
    assert response.status_code == 200
    assert "prediction" in response.json()
    # You can add more specific assertion for prediction result based on your expectation
