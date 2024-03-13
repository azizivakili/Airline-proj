CREATE TABLE `AirFrance_Airline` (
  `Aircraft` VARCHAR(10) PRIMARY KEY,
  `Flight_Type` VARCHAR(20),
  `Origin` VARCHAR(100),
  `Destination` VARCHAR(100),
  `Departure_Date` date,
  `Departure_Time` time,
  `Arrival_Date` date,
  `Arrival_Time` time,
  `EstimatedArrivalTime` time,
  `RealArrivalTime` time,
  `EA_Time_Minutes` time,
  `RA_Time_Minutes` time,
  `Delay_Time` time
);
