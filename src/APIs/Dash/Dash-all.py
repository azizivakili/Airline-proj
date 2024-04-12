import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout of the first page with navigation links
app.layout = html.Div([
    html.H1("Flight Delay Prediction Dashboard"),
    html.Div([
        dcc.Link('VDash-ML-Predict.py', href='/VDash-ML-Predict.py'),
        html.Br(),
        dcc.Link('Dash-ML-Predict.py', href='/visualization2'),
        html.Br(),
        dcc.Link('Dash-Dataset-dropbox.py', href='/visualization3'),
    ]),
    # Placeholder for displaying other Dash applications
    html.Div(id='app-container')
])

# Define callback to load different Dash applications based on navigation links
@app.callback(
    Output('app-container', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/visualization1':
        return dcc.Iframe(src='/visualization1', width='100%', height='600')
    elif pathname == '/visualization2':
        return dcc.Iframe(src='/visualization2', width='100%', height='600')
    elif pathname == '/visualization3':
        return dcc.Iframe(src='/visualization3', width='100%', height='600')
    else:
        return "404 - Page not found"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

