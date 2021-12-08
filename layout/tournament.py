'''Displays Tournament View'''
from dash import dcc
from dash import html
from utils import *
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objects as go

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

next_round = {
    'R128':'R64',
    'R64':'R32',
    'R32':'R16',
    'R16':'QF',
    'QF':'SF',
    'SF':'F',
}

def get_data(year, tournament_id):
    filename=f'data/atp_matches_doubles_{year}.csv'
    year_df = pd.read_csv(filename,index_col=False)
    # only what is needed for the plot
    columns = ['match_num','score','round','winner1_name', 'winner1_id', 'loser1_name', 'loser1_id']
    tournament_df = year_df.loc[year_df['tourney_id'] == tournament_id, columns]
    tournament_df.columns=['match_num','score','round','winner_name', 'winner_id', 'loser_name', 'loser_id']
    # transform the data for the expected format
    indexes = list(tournament_df.match_num)
    gen_links = (x for x in tournament_df.itertuples() if x.round != 'F') # the final does not link anywhere
    source = []
    target = []
    winner_data = []
    names = [' x '.join(i) for i in zip(tournament_df["winner_name"],tournament_df["loser_name"])]
    for data in gen_links :
        current = data.match_num
        idx = indexes.index(current)
        source.append(idx)
        winner = data.winner_id
        winner_name = data.winner_name
        current_round = data.round
        score = data.score
        next_match_type = next_round[current_round]
        next_match = tournament_df.loc[
            ((tournament_df['winner_id']==winner) | (tournament_df['loser_id']==winner)) 
            & (tournament_df['round']==next_match_type)
            ,:].match_num.iloc[0]
        tgt = indexes.index(next_match)
        target.append(tgt)
        winner_data.append(f'{winner_name} <br /> {score}')
        

    return indexes, names, source, target, winner_data


def tournament_view():
    '''Displays Tournament View'''
    data = get_data(2017,'2017-M020')
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = data[1],
            customdata = data[1],
            hovertemplate='%{customdata}<extra></extra>', # <extra></extra> hides the number on the label
            color = random_palette(len(data[1])),
            ),
            link = dict(
            source = data[2], # indices correspond to labels, eg A1, A2, A2, B1, ...
            target = data[3],
            value = np.ones(len(data[2])),
            customdata = data[4],
            color = random_palette(len(data[4])),
            hovertemplate='%{customdata}<extra></extra>', # <extra></extra> hides the number on the label
        ))])



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
