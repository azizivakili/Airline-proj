# Airline Delay Prediction Data Engineering Project

This project aims to predict airline delays using historical flight data. The predictive modeling is performed using linear regression techniques.
The data set is taken from the following website live data:  
[FlightAware](https://www.flightaware.com/live/cancelled)

Specifically, data is collected from this [sourece link](https://www.flightaware.com/live/aircrafttype/A320). 
The website provides real-time information about flights, including aircraft types, flight numbers, departure, and arrival times. 
Also real arrival time of each flight is stored in its specific [aircraft page](https://www.flightaware.com/live/flight/ANA312/history/20240403/2215Z/RJNT/RJTT)   
By clicking on any flight from the table in the first link provided, you can find the actual arrival time in the subsequent link.

**Objective:**
- Predict airline delays to improve passenger experience and operational efficiency. The project seeks to address the critical challenges associated with flight delays by developing predictive models for both missing arrival flight delay prediction and total arrival flight delay prediction.
## Project Overview

Airline delays can significantly impact travel schedules and passenger satisfaction. Predicting these delays can help airlines and passengers better plan their journeys. This project focuses on building predictive models to forecast airline delays based on various factors such as expected arrival time, actual arrival time, and aircraft type.

## Project Structure

The project is structured as follows:

1. **Data Extraction**:
   - Data is taken from above mentioned website using ETL techniques
   - Web scraping techniques is used to extract relevant flight information(eg: Flight number, departure time, Arrival time and others)
   - Handling different HTML structures and potential changes on dataset website
   - See sample [Selenium file](https://github.com/azizivakili/airline-proj/blob/main/notebooks/Retrieved_Data_Selenioum/aircraft-A320.ipynb)

2. **Data Integration**:
   - Different extracted live Airline data of various dates are integrated to create unified dataset
   - Dataset is created after joining and unifying differnt data of various dates
   - Raw Dataset before cleaning is given in file [Raw-Data](https://github.com/azizivakili/airline-proj/blob/main/data/datasets/AirlinesDelay-Raw-Dataset.csv)

3. **Data Cleaninga and Preprocessing**: 
   - Unnecessary columns (eg: 'Origin' and 'Destination') are dropped.
   - Categorical variables are encoded into numerical codes.
   - Missing values in numerical columns are handled by replacing them with the median.
   - Featue engineering is applied on dataset and data formats are changed based on requrements.
   - Final dataset after extraction and cleaning process is given in file [Dataset](https://github.com/azizivakili/airline-proj/blob/main/data/datasets/AirlinesDelay-Dataset.csv)


4. **Data manipulation**:
   - Creation of SQL Database and Data Import:
An SQL database named "AirlineDB" is created either through a command line interface or a graphical interface like phpldapadmin. All database includeing tables can be imported using [AirlineDB](https://github.com/azizivakili/airline-proj/blob/main/data/Database/SQL-Ailrline-DB/AirlineDB.sql)
A cleaned and pre-processed dataset is imported into the "AirlineDB" database 
This process results in the creation of tables and the population of data within those tables.

   - Exporting Database as JSON:
The complete database along with related tables is exported as a sql file named "AirlineDB.sql".

   - Database Tables:
The database contains four tables: "AirlinesDelay", "FlightPredictions", "AirlinesDelayVisual", and "predicted_delay_MissingArrival".

   - Connecting to the Database using Python:
Connection to the "AirlineDB" database is established using Python modules such as pymysql, sqlalchemy, and sqlite3. These modules facilitate communication between Python code and the SQL database.
Data from the database can be retrieved and manipulated using Python data structures, such as dataframes.

   - Exporting Database and importing into MongoDB:
The [JSON file](https://github.com/azizivakili/airline-proj/blob/main/data/Database/MongoDB/AirlineDB.json) containing the exported data from the SQL server (i.e., "AirlineDB.json") is imported into MongoDB.
This process involves parsing the JSON file and inserting its contents into MongoDB collections, thus migrating the data from the SQL database to MongoDB. Bellow, the command to import inside MongoDB Docker image is given:
   ```
   * docker exec -it my_mongo bash
   * mongoimport -d AirlineDB -c AirlinesDelay --authenticationDatabase admin --username admin --password pass --jsonArray --file data/db/AirlineDB.json
   ```

5. **Data Modeling**:
   - The prediciton model is based on linear and multi-linear regression using scikit-learn library
   - All flights delay predection: For all flight delay predictions, a Linear Regression model is utilized. The dataset is extracted from MySQL, specifically from the "AirlinesDelay" file. Subsequently, the data is separated into x_train and y_train dataframes. Simple linear regression is then applied to predict all flight delays based on estimated arrival time and actual arrival times. The predicted results are stored back into MySQL under the filename "FlightPredictions.
   - Predicted delay for missing flights arrival time: Predicted delays for missing flight arrival times are calculated using SimpleImputer with a mean strategy. The dataset utilized for this prediction is also extracted from MySQL,from the "AirlinesDelay" table. Subsequently, the predicted delays for flights with missing arrival times are stored in the "predicted_delay_MissingArrival" dataframe in MySQL.
   - Above proccess is coded in [Prediction code](https://github.com/azizivakili/airline-proj/blob/main/notebooks/Prediction_notebooks/Predicteding_code.ipynb) file. 
   
## APIs
- The structure for APIs in this project is based on the FastAPI framework, incorporating CRUD operations. Additionally, it extends to integrate a machine learning model for predicting flight delays. APIs can be accessed in [APIs](https://github.com/azizivakili/airline-proj/tree/main/src/APIs)
  - [Dash](https://github.com/azizivakili/airline-proj/tree/main/src/APIs/Dash) dashboard APIs are presenting visualization results
  - [MongoDB-API](https://github.com/azizivakili/airline-proj/tree/main/src/APIs/MongoDB-API) presents CRUD operations on MogoDB and Mongo Express.
  - [Prediction-Model-API](https://github.com/azizivakili/airline-proj/tree/main/src/APIs/Prediction-Model-API) presents prediction API.
  - [SQLDB-API](https://github.com/azizivakili/airline-proj/tree/main/src/APIs/SQLDB-API) presents CRUD operations on SQL Database. 

## Pytest
- In order to test and assert our CRUD operations via API, Airlines [API pytest](https://github.com/azizivakili/airline-proj/tree/main/src/AirlineDB-Pytest) is provided.
- The pytest for Prediction model is located in [ML-Pytest](https://github.com/azizivakili/airline-proj/tree/main/src/APIs/Prediction-Model-API/ML-Model-pytest)
  
## Visualization
   - [Dataframe](https://github.com/azizivakili/airline-proj/blob/main/data/datasets/AirlinesDelay-Visualized.csv) will be loaded from Database
   - Dealy_Time vs. predicted delay values are plotted to visualize model performance.
   - Scatterplot is created to compare actual delay time with predicted delay time.
   - Predicted delay values are combined with relevant aircraft information and stored in a CSV file 
   - Resulted Dataframes will be saved back to MySQL server database table named 'predicted_delay_MissingArrival'.
   - Visulization is presented using python and Dash framework.
   - [Visualization code](https://github.com/azizivakili/airline-proj/blob/main/notebooks/visualized_data/Visualization-code.ipynb)
     
## Tools and Technologies
   - Used Python for Coding
   - Web scraping with Selenium and BeautifulSoup for data acquisition
      - We employ web scraping techniques to extract relevant data from the FlightAware website. Python libraries such as BeautifulSoup and requests are used for this purpose. The scraping process involves retrieving HTML content from the designated URL and parsing it to extract the desired information, such as aircraft type, flight details, and timestamps.
   - Pandas for Data Integration ,cleaning , preprocessing and Feature Engineering
   - UML diagram to present structure the data
   - Integration of data from MySQL (using PHPMyAdmin) and MongoDB
   - FastAPI for API development and manipulation of data.
   - Prediction modeling using scikit-learn library.
   - Matplotlib for data visualization
     
## Requirements

- Python 3.x
- Libraries: pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn, sqlalchemy, pymysql, mysql-connector-python

## Usage

1. Clone this repository to your local machine.
2. Install the required libraries using `pip install -r requirements.txt`.
3. Set up a MySQL database with historical flight data and update the connection parameters in the script.
4. Run the main script `airline_delay_prediction.py`.
5. Check the generated CSV files for predicted delay values and visualization plots.
6. Verify the data stored in the MySQL database tables.

## References
- https://learn.datascientest.com/
- https://www.selenium.dev/
- https://pypi.org/project/pysql/
- https://www.sqlalchemy.org/
- https://www.docker.com/

## Contributors

- [Latifa Azizi Vakili]
