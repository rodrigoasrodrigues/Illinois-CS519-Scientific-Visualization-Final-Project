'''Main app module, dash application'''
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from server import app
from dash.dependencies import Input, Output
from dash import no_update
from dash import callback_context
from layout.tournament import drop_down_tournament
from layout.match_details import match_details_view, aces_serves_view
from layout.match_placement import match_placement_view
from layout.header import header
from layout.footer import footer
from utils import is_not_a_node

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
        dbc.Col(
            dbc.Row([
                html.Div([
                    drop_down_tournament(),
                    dbc.Card([
                    html.Div([
                        dcc.Graph(
                                id='tornament-plot'
                            )])
                    ],
                    body=True),
                ])
            ])
            , lg=12, xl=6, className="mb-4"
        ),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H2("Novak Djokovic x Juan Martin del Potro (F)", id="match_title"),
                            html.P("6-3 7-6(4) 6-3", id="match_score"),
                        ]
                    ),
                ], className="mb-4"
            ),
            match_details_view(),
        ], lg=12, xl=6),
    ]),
    dbc.Row(
            [
                dbc.Col(
                    dbc.Row([
                        html.Div([
                            match_placement_view()
                        ])
                    ])
                    , lg=12, xl=6, className="mb-4"
                )
                ,
                dbc.Col(
                    dbc.Row([
                        html.Div([
                            aces_serves_view()
                        ])
                    ])
                    , lg=12, xl=6, className="mb-4"
                )
                
            ],
            align="center"
        ),
    dbc.Row(
            [
                footer(),
            ],
            align="center"
        )

    ],
    fluid=True)
    
default_titles = {
    '2018-560': ['Novak Djokovic x Juan Martin del Potro (F)','6-3 7-6(4) 6-3'],
    '2018-540': ['Novak Djokovic x Kevin Anderson (F)','6-2 6-2 7-6(3)'],
    '2018-520': ['Rafael Nadal x Dominic Thiem (F)','6-4 6-3 6-2'],
    '2018-580': ['Roger Federer x Marin Cilic (F)','6-2 6-7(5) 6-3 3-6 6-1'],
}
@app.callback(
    Output('match_title', 'children'),
    Output('match_score', 'children'),
    Input('tournament-dropdown', 'value'),
    Input('tornament-plot', 'clickData')
)
def update_match_texts(tournament, data):
    if callback_context.triggered:
        print(callback_context.triggered)
        which_input = callback_context.triggered[0]['prop_id'].split('.')[1]
        if which_input == 'value': # drop down
            print('VALUEEEEEE')
            return default_titles[tournament]
        elif which_input == 'clickData':
            print('Click Data')
            if is_not_a_node(data):
                return [no_update] * 2
            title, score = data['points'][0]['customdata'].split('<br>')
            score = score.split('<')[0]
            return title, score
        else:
            print('Else')
            return [no_update] * 2
    else:
        print('No context')
        return [no_update] * 2

if __name__ == '__main__':
    app.run_server(debug=True)
