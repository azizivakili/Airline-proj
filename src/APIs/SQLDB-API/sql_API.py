from fastapi import FastAPI, HTTPException, Query, Body, Depends
import mysql.connector
from datetime import datetime
from typing import List, Dict

app = FastAPI()

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="AirlineDB"
)
cursor = connection.cursor(dictionary=True)

# Define dependency to check credentials
def check_credentials(username: str, password: str):
    if username == "admin" and password == "pass":
        return True
    else:
        return False

# Define dependency to get MySQL connection
def get_db_connection(username: str = "", password: str = "", verified: bool = Depends(check_credentials)):
    if verified:
        return connection
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# SowTable: Display all flight entries
@app.get("/show-table")
def show_table():
    cursor.execute("SELECT * FROM AirlinesDelay")
    return cursor.fetchall()

# TableColumns: Display column names
@app.get("/table-columns")
def table_columns():
    cursor.execute("SHOW COLUMNS FROM AirlinesDelay")
    return [column["Field"] for column in cursor.fetchall()]

# Filter: Filter data based on column name
@app.get("/filter")
def filter_data(column_name: str = Query(..., title="Column Name")):
    cursor.execute(f"SELECT {column_name} FROM AirlinesDelay")
    return [result[column_name] for result in cursor.fetchall()]

# AddFlight: Add a new flight entry
@app.post("/add-flight")
def add_flight(flight_data: Dict[str, str], conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    columns = ', '.join(flight_data.keys())
    values_template = ', '.join(['%s'] * len(flight_data))
    query = f"INSERT INTO AirlinesDelay ({columns}) VALUES ({values_template})"
    cursor.execute(query, tuple(flight_data.values()))
    conn.commit()
    return {"message": "Flight added successfully"}

# SearchFlight: Search flight by Aircraft name
@app.get("/search-flight")
def search_flight(aircraft_name: str = Query(..., title="Aircraft Name")):
    cursor.execute("SELECT * FROM AirlinesDelay WHERE Aircraft = %s", (aircraft_name,))
    flights = cursor.fetchall()
    if not flights:
        raise HTTPException(status_code=404, detail=f"No flights found for Aircraft: {aircraft_name}")
    return flights

# DeleteFlight: Delete a flight based on Aircraft
@app.delete("/delete-flight")
def delete_flight(aircraft_name: str = Query(..., title="Aircraft Name"), conn: mysql.connector.connection.MySQLConnection = Depends(get_db_connection)):
    query = "DELETE FROM AirlinesDelay WHERE Aircraft = %s"
    cursor.execute(query, (aircraft_name,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"No flights found for Aircraft: {aircraft_name}")
    conn.commit()
    return {"message": f"{cursor.rowcount} flight(s) deleted successfully for Aircraft: {aircraft_name}"}

