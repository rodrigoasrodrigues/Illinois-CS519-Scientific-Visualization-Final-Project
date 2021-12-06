'''Displays Player Performance'''
from dash import html
import dash_bootstrap_components as dbc


def player_performance_view():
    '''Displays Player Performance'''
    player_performance = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Player performance in tournament", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
        ]
    )
    player_info_box = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Player Information Box", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
        ]
    )
    aces = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Aces ", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
        ]
    )
    serves = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("1st serve % ", className="card-title"),
                    html.P("This is some card text", className="card-text"),
                ]
            ),
        ]
    )
    group = dbc.CardGroup([player_info_box,aces,serves])
    layout = html.Div([
        dbc.Row(dbc.Col([player_performance])),
        dbc.Row(dbc.Col([group]))
    ])
    return layout
