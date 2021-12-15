'''Displays Tournament View'''
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

def drop_down_tournament():
    '''Displays Tournament Selection Drop Down'''
    ddl = dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='NYC'
        )
    return ddl

def tournament_view():
    '''Displays Tournament View'''
    df_sample = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df_sample, x="Fruit", y="Amount", color="City", barmode="group")
    plot = dbc.Card([
        html.Div([
            dcc.Graph(
                    id='tornament-plot',
                    figure=fig
                )
            ])
        ],
        body=True)
    layout = html.Div([
        drop_down_tournament(),
        plot
    ])
    return layout
