'''Main app module, dash application'''
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash

import dash_bootstrap_components as dbc
from layout.tournament import tournament_view
from layout.match_details import match_details_view
from layout.match_placement import match_placement_view
from layout.player_performance import player_performance_view
from layout.header import header
from layout.footer import footer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,"/assets/style.css"])
server = app.server

app.layout = dbc.Container([
    dbc.Row(
            [
                header(),
            ],
            align="center"
        ),
    dbc.Row(
            [
                dbc.Col(tournament_view(), sm=12, md=8, lg=6, className="mb-4"),
                dbc.Col(match_details_view(),sm=12, md=4, lg=6, className="mb-4"),
            ],
            align="center"
        ),
    dbc.Row(
        [
            dbc.Col(match_placement_view(), sm=12, md=8, lg=6, className="mb-4"),
            dbc.Col(player_performance_view(),sm=12, md=4, lg=6, className="mb-4"),
        ],
        align="center",
        className="mb-4" # margin bottom 4
    ),
    dbc.Row(
            [
                footer(),
            ],
            align="center"
        )

    ],
    fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
