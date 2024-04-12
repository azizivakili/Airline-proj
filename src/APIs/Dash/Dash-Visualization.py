import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import sqlalchemy

# Load Dataframe from Database
def retrieve_data_from_mysql(host, user, password, database, table_name):
    try:
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        engine.dispose()  # Close the database connection
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'AirlineDB'
    table_name = 'AirlinesDelayVisual'

    df = retrieve_data_from_mysql(host, user, password, database, table_name)
    if df is not None:
        return df
    else:
        print("Failed to retrieve data from MySQL.")

df = main()

# Convert numbers to float type. 
df['EA_Time_Minutes'] = df['EA_Time_Minutes'].replace('', np.nan).astype(float)
df['RA_Time_Minutes'] = df['RA_Time_Minutes'].replace('', np.nan).astype(float)
df['Delay_Time'] = df['Delay_Time'].replace('', np.nan).astype(float)

# Scatter plot of Delay_Time vs RA_Time_Minutes and Delay_Predicted vs RA_Time_Minutes
scatter_fig = {
    'data': [
        {
            'x': df['Delay_Time'],
            'y': df['RA_Time_Minutes'],
            'mode': 'markers',
            'marker': {'color': 'red'},
            'name': 'Delay_Time'
        },
        {
            'x': df['Delay_Predicted'],
            'y': df['RA_Time_Minutes'],
            'mode': 'markers',
            'marker': {'color': 'blue'},
            'name': 'Delay_Predicted'
        }
    ],
    'layout': {
        'title': 'Scatter Plot of Delay_Time and Delay_Predicted vs RA_Time_Minutes',
        'xaxis': {'title': 'Delay'},
        'yaxis': {'title': 'RA_Time_Minutes'}
    }
}

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Airline Delay Visualization Dashboard"),
    
    # Scatter plot of EA_Time_Minutes vs RA_Time_Minutes
    dcc.Graph(id='scatter-plot',
              figure={
                  'data': [{
                      'x': df['EA_Time_Minutes'],
                      'y': df['RA_Time_Minutes'],
                      'mode': 'markers',
                      'marker': {
                          'size': 15,
                          'color': df['Delay_Time'],
                          'colorscale': 'Viridis',
                          'showscale': True
                      },
                      'type': 'scatter'
                  }],
                  'layout': {
                      'title': 'Scatter Plot',
                      'xaxis': {'title': 'EA_Time_Minutes'},
                      'yaxis': {'title': 'RA_Time_Minutes'}
                  }
              }),
    
    # Histograms
    dcc.Graph(id='histograms',
              figure={
                  'data': [{
                      'x': df[col],
                      'type': 'histogram',
                      'name': col
                  } for col in ['Delay_Time', 'EA_Time_Minutes', 'RA_Time_Minutes']],
                  'layout': {
                      'title': 'Histograms'
                  }
              }),
    # Scatter plot of Delay_Time vs RA_Time_Minutes and Delay_Predicted vs RA_Time_Minutes
    dcc.Graph(id='scatter-plot-2',
              figure=scatter_fig
              ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
