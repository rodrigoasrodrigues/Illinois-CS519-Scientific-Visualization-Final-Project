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
    'F':None,
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
    gen_links = (x for x in tournament_df.itertuples()) # the final does not link anywhere
    source = []
    target = []
    color_data = []
    winner_data = []
    names = [' x '.join(i) for i in zip(tournament_df["winner_name"],tournament_df["loser_name"])]
    # names = ['' for i in zip(tournament_df["winner_name"],tournament_df["loser_name"])]
    players = {}
    for data in gen_links :
        current = data.match_num
        idx = indexes.index(current)
        source.append(idx)
        winner = data.winner_id
        winner_name = data.winner_name
        players[winner] = winner_name
        players[data.loser_id] = data.loser_name
        current_round = data.round
        score = data.score
        next_match_type = next_round[current_round]
        if next_match_type:
            next_match = tournament_df.loc[
                ((tournament_df['winner_id']==winner) | (tournament_df['loser_id']==winner))
                & (tournament_df['round']==next_match_type)
                ,:].match_num.iloc[0]
            tgt = indexes.index(next_match)
            
        else:
            indexes.append('F')
            names.append(winner_name)
            tgt = len(indexes)-1
        target.append(tgt)
        winner_data.append(f'{winner_name} <br /> {score}')
        color_data.append(winner)
    # player names at start
    treebase = [indexes[m] for m in source if m not in target]
    gen_treebase = (x for x in tournament_df.itertuples() if x.match_num in treebase)
    for match in gen_treebase:
        match_idx = indexes.index(match.match_num)
        for player_id, player_name in [(match.winner_id,match.winner_name),(match.loser_id,match.loser_name)]:
            indexes.append(player_id)
            player_idx = len(indexes)-1
            source.append(player_idx)
            target.append(match_idx)
            winner_data.append(player_name)
            names.append(player_name)
            color_data.append(player_id)
    color_set =list(set(color_data))
    num_colors = len(color_set)
    colors = random_palette(num_colors)
    color_data = [colors[color_set.index(c)] for c in color_data]

    return indexes, names, source, target, winner_data, color_data


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
            color = data[5],
            ),
            link = dict(
            source = data[2], # indices correspond to labels, eg A1, A2, A2, B1, ...
            target = data[3],
            value = np.ones(len(data[2])),
            customdata = data[4],
            color = data[5],
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
