import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import math
from dash.dependencies import Input, Output


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], className="table")

selected_tourneyid = "2018-580"
selected_matchnum = 701

selected_matchid = "20180128-M-Australian_Open-F-Marin_Cilic-Roger_Federer"
atp_matches2018df = pd.read_csv("data/atp_matches_2018.csv")
charting_mstatsdf = pd.read_csv("data/charting-m-stats-Overview.csv")
#atp_playersdf = pd.read_csv("data/atp_players.csv")

selected_year = selected_tourneyid.split("-")[0]

bad_data = False
player_details = "Player Details"
data_unavailable = "DETAILED DATA NOT AVAILABLE"


selected_atpmatchdf = atp_matches2018df[(atp_matches2018df["tourney_id"] == selected_tourneyid) & (atp_matches2018df["match_num"] == selected_matchnum)]

if (selected_atpmatchdf.shape[0] != 1):
    bad_data = True
else:


    winner_firstname = selected_atpmatchdf["winner_name"].item().split()[0]
    winner_lastname = selected_atpmatchdf["winner_name"].item().split()[-1]
    loser_firstname = selected_atpmatchdf["loser_name"].item().split()[0]
    loser_lastname = selected_atpmatchdf["loser_name"].item().split()[-1]

    match_round = selected_atpmatchdf["round"].item()
    match_roundhyphen = "-"+match_round+"-"
    tourney_name = selected_atpmatchdf["tourney_name"].item().replace(" ", "_")

    charting_matchdf = charting_mstatsdf[(charting_mstatsdf["match_id"].str.contains(selected_year))
        & (charting_mstatsdf["match_id"].str.contains(winner_firstname)) 
        & (charting_mstatsdf["match_id"].str.contains(winner_lastname))
        & (charting_mstatsdf["match_id"].str.contains(loser_firstname)) 
        & (charting_mstatsdf["match_id"].str.contains(loser_lastname)) 
        & (charting_mstatsdf["match_id"].str.contains(tourney_name))
        & (charting_mstatsdf["match_id"].str.contains(match_roundhyphen))]


    if (charting_matchdf.shape[0] < 4 or charting_matchdf.shape[0] > 12):
        bad_data = True
    else:

        #print("charting selected", charting_matchdf)

        charting_matchid = charting_mstatsdf["match_id"][0]
        if (winner_lastname in charting_matchid.split("-")[-2]) and (loser_lastname in charting_matchid.split("-")[-1]):
            player1df = selected_atpmatchdf[["winner_name", "winner_hand", "winner_ht", "winner_ioc", "winner_age"]]
            Player2df = selected_atpmatchdf[["loser_name", "loser_hand", "loser_ht", "loser_ioc", "loser_age"]]
            player1df = player1df.rename(columns = {"winner_name": "name", "winner_hand": "hand", "winner_ht": "height(cm)", "winner_ioc": "country", "winner_age": "age"})
            player2df = player2df.rename(columns = {"loser_name": "name", "loser_hand": "hand", "loser_ht": "height(cm)", "loser_ioc": "country", "loser_age": "age"})
            player1df.insert(loc=1, column='outcome', value="winner")
            player2df.insert(loc=1, column='outcome', value="loser")
        else:
            player1df = selected_atpmatchdf[["loser_name", "loser_hand", "loser_ht", "loser_ioc", "loser_age"]]
            player2df = selected_atpmatchdf[["winner_name", "winner_hand", "winner_ht", "winner_ioc", "winner_age"]]
            player1df = player1df.rename(columns = {"loser_name": "name", "loser_hand": "hand", "loser_ht": "height(cm)", "loser_ioc": "country", "loser_age": "age"})
            player2df = player2df.rename(columns = {"winner_name": "name", "winner_hand": "hand", "winner_ht": "height(cm)", "winner_ioc": "country", "winner_age": "age"})
            player1df.insert(loc=1, column='outcome', value="loser")
            player2df.insert(loc=1, column='outcome', value="winner")
        
        player1df.insert(loc=0,column='player', value="Player1" )
        player2df.insert(loc=0,column='player', value="Player2" )

        both_playersdf = pd.concat([player1df,player2df])
        both_playersdf["age"] = both_playersdf["age"].apply(math.floor)
        
        #print(both_playersdf)

        player1acesdf = charting_matchdf[(charting_matchdf["player"]==1) & (charting_matchdf["set"] != "Total")][["set", "aces"]].sort_values(by=["set"])
        player2acesdf = charting_matchdf[(charting_matchdf["player"]==2) & (charting_matchdf["set"] != "Total")][["set", "aces"]].sort_values(by=["set"])

        player1servedf = charting_matchdf[(charting_matchdf["player"]==1) & (charting_matchdf["set"] != "Total")][["set", "first_in", "serve_pts"]].sort_values(by=["set"])
        player2servedf = charting_matchdf[(charting_matchdf["player"]==2) & (charting_matchdf["set"] != "Total")][["set", "first_in", "serve_pts"]].sort_values(by=["set"])
        player1servedf["fstsrv_percent"]= player1servedf["first_in"]/player1servedf["serve_pts"]*100
        player2servedf["fstsrv_percent"]= player2servedf["first_in"]/player2servedf["serve_pts"]*100


        #print(player1servedf)

        acesfig1 = px.bar(player1acesdf, x="set", y="aces", title="Player 1's aces")
        acesfig2 = px.bar(player2acesdf, x="set", y="aces", title = "Player 2's aces")

        fstsrvfig1 = px.line(player1servedf, x="set", y="fstsrv_percent", title="Player 1's first serve percentage", labels = {"fstsrv_percent" : "first serve %"})
        fstsrvfig2 = px.line(player2servedf, x="set", y="fstsrv_percent", title="Player 2's first serve percentage", labels = {"fstsrv_percent" : "first serve %"})

if (bad_data == True):
    both_playersdf = pd.DataFrame()
    player_details = data_unavailable
    acesfig1 = px.bar(pd.DataFrame(),  title=data_unavailable)
    acesfig2 = px.bar(pd.DataFrame(),  title =data_unavailable)

    fstsrvfig1 = px.line(pd.DataFrame(), title=data_unavailable)
    fstsrvfig2 = px.line(pd.DataFrame(), title=data_unavailable)

def match_details_view():
    details = dbc.Card(
        [
            dbc.CardHeader(""),
            dbc.CardBody(
                [
                    html.H4(player_details, className="card-title"),
                    html.P("Player Information", className="card-text"),
                    generate_table(both_playersdf)
                    # generate_table(player1df),
                    # generate_table(player2df)
                ]
            ),
            dbc.CardFooter(""),
        ]
    )
    aces = dbc.Card(
        [
            dbc.CardHeader(""),
            dbc.CardBody(
                [
                    html.H4("Aces ", className="card-title"),
                    html.P("Trend of Aces in match", className="card-text"),
                ]
            ),
            dcc.Graph(id='example-graph-1',figure=acesfig1),
            dcc.Graph(id='example-graph-2',figure=acesfig2),
            dbc.CardFooter(""),
        ]
        
        
    )
    serves = dbc.Card(
        [
            dbc.CardHeader(""),
            dbc.CardBody(
                [
                    html.H4("First serve % ", className="card-title"),
                    html.P("Trend of first serve in the match", className="card-text"),
                ]
            ),
            dcc.Graph(figure=fstsrvfig1),
            dcc.Graph(figure=fstsrvfig2),
            dbc.CardFooter(""),
        ]
    )
    group = dbc.CardGroup([aces,serves])
    layout = html.Div([
        dbc.Row(dbc.Col([details])),
        dbc.Row(dbc.Col([group]))
    ])
    return layout
