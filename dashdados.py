import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# Carregar os dados do arquivo CSV
caminho_arquivo = 'dados/arquivo_auditoria.csv'
dados = pd.read_csv(caminho_arquivo)

# Inicializar o aplicativo Dash
app_dash = dash.Dash(__name__)

# Layout da aplicação Dash
app_dash.layout = html.Div([
    html.H1("Dashboard de Auditoria"),
    dcc.Dropdown(
        id='dropdown-setor',
        options=[{'label': setor, 'value': setor} for setor in dados['Setor'].unique()],
        value=dados['Setor'].unique()[0]  # Valor inicial da dropdown
    ),
])

if __name__ == '__main__':
    app_dash.run_server(debug=True)
