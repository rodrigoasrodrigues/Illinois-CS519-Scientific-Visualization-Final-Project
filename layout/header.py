'''Displays Header'''
from dash import html

def header():
    '''Displays Header'''
    head = html.Header([

        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        ''')
    ])
    return head
