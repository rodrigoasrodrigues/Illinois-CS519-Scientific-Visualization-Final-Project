'''Displays Header'''
from dash import html

def header():
    '''Displays Header'''
    head = html.Header([

        html.H1(children='Tennis Analytics Dashboard'),

        
    ])
    return head
