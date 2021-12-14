'''Displays Tournament View'''
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from utils import *
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objects as go
from server import app

def drop_down_tournament():
    '''Displays Tournament Selection Drop Down'''
    ddl = dcc.Dropdown(
            id='tournament-dropdown',
            options=[
                {'label': '2018 - US Open', 'value': '2018-560'},
                {'label': '2018 - Wimbledon', 'value': '2018-540'},
                {'label': '2018 - Roland Garros', 'value': '2018-520'},
                {'label': '2018 - Australian Open', 'value': '2018-580'}
            ],
            value='2018-560'
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



def get_data(tournament_id):
    year = tournament_id.split('-')[0]
    filename=f'data/atp_matches_{year}.csv'
    year_df = pd.read_csv(filename,index_col=False)
    # only what is needed for the plot
    columns = ['match_num','score','round','winner_name', 'winner_id', 'loser_name', 'loser_id']
    tournament_df = year_df.loc[year_df['tourney_id'] == tournament_id, columns]
    # transform the data for the expected format
    indexes = list(tournament_df.match_num)
    color_data_node = list(tournament_df.winner_id)
    gen_links = (x for x in tournament_df.itertuples() if x.round in ['F','SF','QF','R16']) 
    source = []
    target = []
    color_data_link=[]
    winner_data = []
    hover_data = [f' {i[0]} x {i[1]} <br> {i[2]}' for i in zip(tournament_df["winner_name"],tournament_df["loser_name"],tournament_df["score"])]
    names = ['' for i in zip(tournament_df["winner_name"],tournament_df["loser_name"])]
    players = {}
    # LINKS
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
            
        else: # winner name
            indexes.append('F')
            names.append(last_name_and_initials(winner_name))
            hover_data.append(winner_name)
            tgt = len(indexes)-1
            color_data_node.append(winner)
        target.append(tgt)
        winner_data.append(f'{winner_name} <br /> {score}')
        color_data_link.append(winner)
    # player names at start
    treebase = [indexes[m] for m in source if m not in target]
    gen_treebase = (x for x in tournament_df.itertuples() if x.match_num in treebase)
    for match in gen_treebase:
        match_idx = indexes.index(match.match_num)
        for player_id, player_name in [[match.winner_id,match.winner_name], [match.loser_id,match.loser_name]]:
            indexes.append(player_id)
            player_idx = len(indexes)-1
            source.append(player_idx)
            target.append(match_idx)
            winner_data.append(player_name)
            names.append(last_name_and_initials(player_name))
            hover_data.append(player_name)
            color_data_node.append(player_id)
            color_data_link.append(player_id)
    color_set = list(set(color_data_node))
    num_colors = len(color_data_node)
    colors = random_palette(num_colors)
    color_data_node = [colors[color_set.index(c)] for c in color_data_node]
    color_data_link = [colors[color_set.index(c)] for c in color_data_link]

    return indexes, names, hover_data, source, target, winner_data, color_data_node, color_data_link

@app.callback(
    Output('tornament-plot', 'figure'),
    Input('tournament-dropdown', 'value')
)
def tournament_view(tournament= '2018-560'):
    '''Displays Tournament View'''
    print(f'Selected {tournament}')
    indexes, names, hover_data, source, target, winner_data, color_data_node, color_data_link = get_data(tournament)
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = names,
            customdata = hover_data,
            hovertemplate='%{customdata}<extra></extra>', # <extra></extra> hides the number on the label
            color = color_data_node,
            ),
            link = dict(
            source = source, # indices correspond to labels, eg A1, A2, A2, B1, ...
            target = target,
            value = np.ones(len(source)),
            customdata = winner_data,
            color = color_data_link,
            hovertemplate='%{customdata}<extra></extra>', # <extra></extra> hides the number on the label
        ))])

    return fig
