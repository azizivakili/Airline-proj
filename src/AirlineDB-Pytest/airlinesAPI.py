from fastapi import FastAPI, HTTPException, Query, Body, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Dict

app = FastAPI()

# Connect to MySQL database
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/AirlineDB"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class for declarative class definitions
Base = declarative_base()

# Define Flight table
class Flight(Base):
    __tablename__ = "AirelinesDelay"

    id = Column(Integer, primary_key=True, index=True)
    Aircraft = Column(String(100))  # Specify the maximum length for the VARCHAR column
    FlightType = Column(String(30))
    Origin = Column(String(100))
    Destination = Column(String(100))
    Departure_Date = Column(String(50))
    Departure_Time = Column(String(50))
    Arrival_Date = Column(String(50))
    Arrival_Time = Column(String(50))
    EA_Time_Minutes = Column(String(50))
    RA_Time_Minutes = Column(String(50))
    Delay_Time = Column(String(50))

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Access the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define endpoint to add a new flight entry
@app.post("/add-flight")
def add_flight(flight_data: Dict[str, str], db: Session = Depends(get_db)):
    try:
        flight = Flight(**flight_data)
        db.add(flight)
        db.commit()
        db.refresh(flight)
        return {"message": "Flight added successfully", "flight_id": flight.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

