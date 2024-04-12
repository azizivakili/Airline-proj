CREATE DATABASE IF NOT EXISTS AilineDelay;

-- Use the database
USE AilineDelay;

-- Create the table
CREATE TABLE IF NOT EXISTS Flights (
    Aircraft VARCHAR(50),
    FlightType VARCHAR(50),
    Origin VARCHAR(100),
    Destination VARCHAR(100),
    DepartureTime VARCHAR(20),
    ArrivalTime VARCHAR(20),
    EstimatedArrivalTime VARCHAR(20),
    RealArrivalTime VARCHAR(20),
    EA_Time_Minutes INT,
    RA_Time_Minutes INT,
    DelayTime INT
);
