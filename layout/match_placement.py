'''Displays Match Placement Plot'''
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

def match_placement_view():
    '''Displays Match Placement Plot'''
    df_sample = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [5, 8, 4, 3, 3, 3],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df_sample, x="Fruit", y="Amount", color="City", barmode="group")
    plot = dbc.Card([
        html.Div([
            dcc.Graph(
                    id='example-graph',
                    figure=fig
                )
            ])
        ],
        body=True)
    return plot
