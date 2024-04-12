import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
import plotly.graph_objs as go

# Load the dataset
df = pd.read_csv("Final-data1.csv")

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("Flight Delay Prediction"),
    html.Div([
        dcc.Input(id='ea_time', type='number', placeholder='Enter EA Time (Minutes)'),
        dcc.Input(id='ra_time', type='number', placeholder='Enter RA Time (Minutes)'),
        html.Button(id='submit-button', n_clicks=0, children='Predict Delay'),
    ]),
    html.Div([
        html.Div(id='output-prediction'),
        dcc.Graph(id='delay-prediction-plot'),
    ]),
    html.Div([
        dcc.Graph(id='input-data-plot')
    ])
])

# Define callback to handle prediction and plot update
@app.callback(
    [Output('output-prediction', 'children'),
     Output('delay-prediction-plot', 'figure')],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('ea_time', 'value'),
     dash.dependencies.State('ra_time', 'value')]
)
def update_output(n_clicks, ea_time, ra_time):
    if n_clicks > 0:
        # Train model
        df_train = df.dropna(subset=['Delay_Time']).copy()
        imputer = SimpleImputer(strategy='mean')
        X_train = imputer.fit_transform(df_train[['EA_Time_Minutes', 'RA_Time_Minutes']])
        y_train = df_train['Delay_Time']
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predict delay time
        prediction = model.predict([[ea_time, ra_time]])

        # Generate scatter plot for actual vs predicted delay time
        actual_delay_times = df_train['Delay_Time']
        predicted_delay_times = model.predict(X_train)

        trace_actual = go.Scatter(x=actual_delay_times, y=predicted_delay_times, mode='markers', name='Actual vs Predicted')
        trace_ideal_line = go.Scatter(x=[actual_delay_times.min(), actual_delay_times.max()], 
                                      y=[actual_delay_times.min(), actual_delay_times.max()],
                                      mode='lines', name='Ideal Line')

        layout = go.Layout(title='Actual vs Predicted Delay Time',
                           xaxis=dict(title='Actual Delay Time'),
                           yaxis=dict(title='Predicted Delay Time'))

        figure = go.Figure(data=[trace_actual, trace_ideal_line], layout=layout)

        return f"Predicted delay time: {prediction[0]} minutes", figure

# Define callback to update input data plot
@app.callback(
    Output('input-data-plot', 'figure'),
    [Input('submit-button', 'n_clicks')]
)
def update_input_data_plot(n_clicks):
    # Generate scatter plot for input data
    trace_input = go.Scatter(x=df['EA_Time_Minutes'], y=df['RA_Time_Minutes'], mode='markers', name='Input Data')

    layout = go.Layout(title='Input Data Plot',
                       xaxis=dict(title='EA Time (Minutes)'),
                       yaxis=dict(title='RA Time (Minutes)'))

    figure = go.Figure(data=[trace_input], layout=layout)

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
