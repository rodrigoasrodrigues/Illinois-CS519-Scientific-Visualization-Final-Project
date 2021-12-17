'''Displays Footer'''
from dash import html
import dash_bootstrap_components as dbc

def footer():
    '''Displays Footer'''
    f = html.Footer([
        dbc.Row([
            html.Div(children=['This project is part of course CS519 - Scientific Visualization for ',
                html.A('MCS-DS',href='https://cs.illinois.edu/academics/graduate/professional-mcs/online-master-computer-science-data-science', target='_blank'),
                ' program at ',
                html.A('UIUC',href='https://cs.illinois.edu', target='_blank')]
            )
        ], className="text-center mb-4"),
        dbc.Container(
            [
                dbc.Row([
                    dbc.Col([
                        html.H5('Evan Pickett'),
                        html.P('University of Illinois at Urbana-Champaign'),
                        html.A('evandp3@illinois.edu ', href='mailto:evandp3@illinois.edu ')
                    ], className="text-center"),
                    dbc.Col([
                        html.H5('Rodrigo Rodrigues'),
                        html.P('University of Illinois at Urbana-Champaign'),
                        html.A('rar5@illinois.edu', href='mailto:rar5@illinois.edu')
                    ], className="text-center"),
                    dbc.Col([
                        html.H5('Raj Datta'),
                        html.P('University of Illinois at Urbana-Champaign'),
                        html.A('datta7@illinois.edu', href='mailto:datta7@illinois.edu')
                    ], className="text-center")
                ])
            ]
        )
        
    ])
    return f
