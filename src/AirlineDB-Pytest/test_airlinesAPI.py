import pytest
from fastapi.testclient import TestClient
from airlinesAPI import app, Flight, get_db

client = TestClient(app)

# Define test data
test_flight_data = {
    "Aircraft": "ZZE4012",
    "FlightType": "A320",
    "Origin": "El Dorado Int'l",
    "Destination": "Jose Maria Cordova Int'l",
    "Departure_Date": "2024-04-03",
    "Departure_Time": "15:21",
    "Arrival_Date": "2024-04-03",
    "Arrival_Time": "15:59",
    "EA_Time_Minutes": "38",
    "RA_Time_Minutes": "97",
    "Delay_Time": "59"
}

# Test add-flight endpoint
def test_add_flight():
    response = client.post("/add-flight", json=test_flight_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Flight added successfully"

    # Check if the flight data is inserted into the database
    db = next(get_db())
    inserted_flight = db.query(Flight).filter(Flight.Aircraft == test_flight_data["Aircraft"]).first()
    db.close()
    assert inserted_flight is not None
    assert inserted_flight.Aircraft == test_flight_data["Aircraft"]
    assert inserted_flight.FlightType == test_flight_data["FlightType"]
    assert inserted_flight.Origin == test_flight_data["Origin"]
    assert inserted_flight.Destination == test_flight_data["Destination"]
    assert inserted_flight.Departure_Date == test_flight_data["Departure_Date"]
    assert inserted_flight.Departure_Time == test_flight_data["Departure_Time"]
    assert inserted_flight.Arrival_Date == test_flight_data["Arrival_Date"]
    assert inserted_flight.Arrival_Time == test_flight_data["Arrival_Time"]
    assert inserted_flight.EA_Time_Minutes == test_flight_data["EA_Time_Minutes"]
    assert inserted_flight.RA_Time_Minutes == test_flight_data["RA_Time_Minutes"]
    assert inserted_flight.Delay_Time == test_flight_data["Delay_Time"]

# Test show-table endpoint
def test_show_table():
    response = client.get("/show-table")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test table-columns endpoint
def test_table_columns():
    response = client.get("/table-columns")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test filter endpoint
def test_filter():
    response = client.get("/filter?column_name=Aircraft")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test search-flight endpoint
def test_search_flight():
    response = client.get("/search-flight?aircraft_name=ZZE4012")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test delete-flight endpoint
def test_delete_flight():
    response = client.delete("/delete-flight?aircraft_name=ZZE4012")
    assert response.status_code == 200
    assert response.json()["message"].startswith("1 flight(s) deleted successfully")

