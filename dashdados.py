import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd


# Inicializar o aplicativo Dash
app_dash = dash.Dash(__name__)



if __name__ == '__main__':
    app_dash.run_server(debug=True)
