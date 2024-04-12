import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
import pymysql

# Connect to MySQL database and retrieve data
def retrieve_data_from_mysql(host, user, password, database, table_name):
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except pymysql.Error as e:
        print(f"Error: {e}")
        return None

# Load trained linear regression model
def load_model():
    # Assuming you have already trained the model and stored it
    lr = LinearRegression()  # Create an instance of LinearRegression
    # Train the model using your data (omitted for brevity)
    return lr  # Return the trained model object

# Sample DataFrame (to be replaced with data from MySQL)
df_train = retrieve_data_from_mysql('localhost', 'root', 'root', 'AirlineDB', 'AirlinesDelayVisual')

# Create Dash app
app = dash.Dash(__name__)

# Define layout of the Dash app
app.layout = html.Div([
    html.H1("Flight Delay Prediction Dashboard"),
    dcc.Graph(id='scatter-plot'),
    html.Div([
        html.Label("Select a feature to visualize:"),
        dcc.Dropdown(
            id='dropdown-feature',
            options=[{'label': col, 'value': col} for col in df_train.columns],
            value='EA_Time_Minutes'
        ),
        html.Label("Predicted Delay Time:"),
        dcc.Input(
            id='predicted-delay',
            type='number',
            value=0,
            disabled=True
        )
    ])
])

# Define callback to update scatter plot based on dropdown selection
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('dropdown-feature', 'value')]
)
def update_scatter_plot(selected_feature):
    fig = px.scatter(df_train, x=selected_feature, y='Delay_Predicted', title=f"Scatter plot of {selected_feature} vs Delay Time")
    return fig

# Define callback to update predicted delay time based on user input
@app.callback(
    Output('predicted-delay', 'value'),
    [Input('dropdown-feature', 'value')]
)
def update_predicted_delay(selected_feature):
    if selected_feature:
        # Assume x contains the selected feature's values for the prediction
        x = df_train[[selected_feature]]
        # Load the model
        lr = load_model()
        # Predict delay time using the trained model
        predicted_delay = lr.predict(x)[0]
        return predicted_delay
    else:
        return 0

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
