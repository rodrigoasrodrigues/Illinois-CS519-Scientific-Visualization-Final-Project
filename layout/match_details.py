import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


def match_details_view():
    details = dbc.Card(
        [
            dbc.CardHeader("This is the header"),
            dbc.CardBody(
                [
                    html.H4("Match Detailed Trends", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
            dbc.CardFooter("This is the footer"),
        ]
    )
    aces = dbc.Card(
        [
            dbc.CardHeader("This is the header"),
            dbc.CardBody(
                [
                    html.H4("Aces ", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
            dbc.CardFooter("This is the footer"),
        ]
    )
    serves = dbc.Card(
        [
            dbc.CardHeader("This is the header"),
            dbc.CardBody(
                [
                    html.H4("1st serve % ", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
            dbc.CardFooter("This is the footer"),
        ]
    )
    group = dbc.CardGroup([aces,serves])
    layout = html.Div([
        dbc.Row(dbc.Col([details])),
        dbc.Row(dbc.Col([group]))
    ])
    return layout
