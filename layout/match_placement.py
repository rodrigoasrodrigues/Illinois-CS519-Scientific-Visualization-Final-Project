'''Displays Match Placement Plot'''
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import os
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import random
from server import app

NOT_FOUND_STRING = "Data Not Found"

def drawMapGraph(df, xVal):
    if df.empty:
        return px.scatter(title=NOT_FOUND_STRING)
    location_map = {
        "deuce_wide": [xVal,.75],
        "deuce_middle": [xVal,.55], 
        "deuce_t": [xVal,.65],
        "ad_wide": [xVal,.25],
        "ad_middle": [xVal,.45],
        "ad_t": [xVal,.35],
    }
    npIndex = df.columns.values #grabs the names of the selected columns
    npVals = df.values[0].astype(np.int64) #grabs the values of the selected row
    numScores = 0
    for i in npVals:
        numScores += i
    npSize = np.zeros(npIndex.shape[0],dtype=np.float64) #normalized array for magnitude of results
    index = 0
    for i in npVals:
        npSize[index] = i/numScores
        index+=1
    #goal:
    #make a larger list so that each location can have multiple points representing individual serves rather than one big point representing multiple serves
    npBigIndex = [] #stores location names such as 'deuce_wide'
    npBigVals = np.zeros(numScores,dtype=np.float64) #stores values of each location (number total, shared between individual points for display purposes)
    npBigSize = np.zeros(numScores,dtype=np.float64) #stores 'size' of each location (although this is only used for spacing purposes)
    npBigRelSize = np.zeros(numScores,dtype=np.float64) #stores a relative size of each location (0-1]
    index = 0
    bigIndex = 0
    #go through our smaller array and make a bigger one to separate individual serves
    for i in npIndex:
        num = npVals[index]
        for _ in range(0,num):
            npBigIndex.append(i)
            npBigVals[bigIndex]=npVals[index]
            npBigSize[bigIndex]=0.025#npSize[index]
            npBigRelSize[bigIndex]=npSize[index]
            bigIndex+=1
        index+=1
    npLocationX = np.zeros(npBigVals.shape[0],dtype=np.float64) #gets X position of where serve should be
    npLocationY = np.zeros(npBigVals.shape[0],dtype=np.float64) #gets Y position of where serve should be
    index = 0
    #add some random spreading to the points
    for i in npBigIndex:
        location = location_map[i]
        npLocationX[index] = location[0] + (random.random()*2 - 1)*.04#(random.random()*2 - 1)*npBigSize[index]
        npLocationY[index] = location[1] + (random.random()*2 - 1)*npBigSize[index]
        index+=1
    formatted_df = pd.DataFrame({
        "Location": npBigIndex,
        "x": npLocationX,
        "y": npLocationY,
        "size": npBigSize,
        "RelativeServes": npBigRelSize,
        "Number Of Serves": npBigVals
    })
    # Plotly Express version
    fig = px.scatter(
        formatted_df,
        x="x",
        y="y",
        color="Number Of Serves",
        range_x=[-0.05, 1.05],
        range_y=[-0.05, 1.05],
        #size="size",
        color_continuous_scale=px.colors.sequential.Inferno,
        hover_data={"size": False, "x": False, "y": False, "Location": True},
        #text="value"
    )
    # Add corner flags to prevent zoom and pitch distortion
    fig.add_scatter(
        x=[0, 0, 1, 1],
        y=[0, 1, 0, 1],
        mode="markers",
        marker=dict(size=1, color="grey"),
        name="Flags",
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis=dict(range=[-0.05, 1.05]),
        yaxis=dict(range=[-0.05, 1.05]),
        #coloraxis_showscale=False,
    )
    # Remove side color scale and hide zero and gridlines
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )
    # Disable axis ticks and labels
    fig.update_xaxes(showticklabels=False, title_text="")
    fig.update_yaxes(showticklabels=False, title_text="")
    image_file = "assets/court.jpg"
    image_path = os.path.join(os.getcwd(), image_file)
    from PIL import Image
    img = Image.open(image_path)
    fig.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=1,
            sizey=1,
            sizing="stretch",
            opacity=0.7,
            layer="below",
        )
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False),
    )
    fig.update_layout(margin=dict(l=20, r=20, b=20, t=20))
    # Make sure pitch background image shape doesn't get distorted
    fig.update_yaxes(scaleanchor="x", scaleratio=0.65)
    fig.update_layout(legend=dict(yanchor="top", y=0.95, xanchor="left", x=-0.08))
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=-0.14,
                x=-0.08,
                xanchor="left",
                yanchor="bottom",
            )
        ]
    )
    fig.update_layout(autosize=True, hovermode="closest")
    fig.update_layout(legend=dict(font=dict(family="Arial", size=10, color="grey")))
    # Hide corner flag trace in the legend
    for trace in fig["data"]:
        if trace["name"] == "Flags":
            trace["showlegend"] = False
    return fig

def drawBarGraph(df):
    if df.empty:
        return px.bar(title=NOT_FOUND_STRING)
    npIndex = df.columns.values #grabs the names of the selected columns
    for i, loc in enumerate(npIndex):
        npIndex[i] = loc.replace("_", " ") #replace names so they are a bit more human readable (get rid of "_" and replace with " ")
        words = npIndex[i].split(" ") #capitalizes each letter of every word
        finalWords = []
        for j, word in enumerate(words):
            finalWords.append(word.capitalize())
        npIndex[i] = ' '.join(finalWords)
    npVals = df.values[0].astype(np.int64) #grabs the values of the selected row
    formatted_df = pd.DataFrame({
        "Location": npIndex,
        "Value": npVals,
    })
    fig = px.bar(
        formatted_df,
        x="Location",
        y="Value",
        hover_data={"Location": False, "Value": True},
    )
    #changing axis labels
    #from: https://stackoverflow.com/questions/63386812/plotly-how-to-hide-axis-titles-in-a-plotly-express-figure-with-facets
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = 'Number Of Serves'
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = 'Location'
    return fig

graph_player1_cache=None
graph_player2_cache=None
graph_player1_bar_cache=None
graph_player2_bar_cache=None
name_player1_cache=None
name_player2_cache=None
match_cache=None
current_tournament=None

#wish this could be done better but it works!
def getTouramentFromValue(value):
    valuePairs = {
        '2018-560': 'US_Open',
        '2018-540': 'Wimbledon',
        '2018-520': 'Roland_Garros',
        '2018-580': 'Australian_Open'
    }
    return valuePairs[value]

#a simple way to format the round string from the depth value of the graph
def getDepthStringFromInt(value):
    depthList = ["N/A", "RR", "QF", "SF", "F", "N/A"]
    return depthList[value]

#grabs the round of the tournament (formatted), and player names. Names will be empty if the match isn't valid
def getMatchInfo(match):
    round = getDepthStringFromInt(match['points'][0]['depth'])
    if round == "N/A":
        return round, "", ""
    customData = match['points'][0]['customdata']
    splitData = customData.split('<br>')
    splitNames = splitData[0].split('x')
    name1 = splitNames[0].strip().replace(' ','_')
    name2 = splitNames[1].strip().replace(' ','_')
    return round, name1, name2

#reads from the serve direction file and outputs a dataframe matching parameters
def getMatchDataFrame(matchString, playerNum):
    file = "charting-m-stats-ServeDirection.csv"
    file_plus_path = "data/" + file
    odf = pd.read_csv(file_plus_path,names=['match_id','row','deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t','err_net','err_wide','err_deep','err_wide_deep','err_foot','err_unknown'])
    df = odf.loc[(odf['match_id'].str.contains(matchString,case=False, na=False)) & (odf['row'] == f'{playerNum} Total')]
    df = pd.DataFrame(df,columns=['deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t'])
    return df

#ugly hack to get a callback from the dropdown value and store it here for reference
@app.callback(
    Output('hidden-div', 'children'),
    Input('tournament-dropdown', 'value')
)
def updateGlobalTournament(info):
    global current_tournament
    current_tournament = getTouramentFromValue(info)
    return info

@app.callback(
    Output('graph-player1-placement', 'figure'),
    Output('graph-player1-placement-bar', 'figure'),
    Output('graph-player2-placement', 'figure'),
    Output('graph-player2-placement-bar', 'figure'),
    Output('player-1-name-placement', 'children'),
    Output('player-2-name-placement', 'children'),
    Input('tornament-plot', 'clickData')
)
def update_graphs(match):
    global match_cache
    global graph_player1_cache
    global graph_player1_bar_cache
    global graph_player2_cache
    global graph_player2_bar_cache
    global name_player1_cache
    global name_player2_cache
    global current_tournament
    if match == match_cache:
        if graph_player1_cache and graph_player1_bar_cache and graph_player2_cache and graph_player2_bar_cache and name_player1_cache and name_player2_cache:
            return graph_player1_cache, graph_player1_bar_cache, graph_player2_cache, graph_player2_bar_cache, name_player1_cache, name_player2_cache
    round = None
    name1 = None
    name2 = None
    if 'depth' not in str(match):
        if graph_player1_cache and graph_player1_bar_cache and graph_player2_cache and graph_player2_bar_cache and name_player1_cache and name_player2_cache:
            return graph_player1_cache, graph_player1_bar_cache, graph_player2_cache, graph_player2_bar_cache, name_player1_cache, name_player2_cache
    else:
        round, name1, name2 = getMatchInfo(match)

    matchString = f'-M-{current_tournament}-{round}-{name1}-{name2}'
    df1 = getMatchDataFrame(matchString,1)
    df2 = getMatchDataFrame(matchString,2)

    fig1 = drawMapGraph(df1,0.34)
    fig1Bar = drawBarGraph(df1)

    fig2 = drawMapGraph(df2,0.34)
    fig2Bar = drawBarGraph(df2)

    name1 = f"Player: {name1.replace('_',' ')}"
    name2 = f"Player: {name2.replace('_',' ')}"
    graph_player1_cache = fig1
    graph_player1_bar_cache = fig1Bar
    graph_player2_cache = fig2
    graph_player2_bar_cache = fig2Bar
    name_player1_cache = name1
    name_player2_cache = name2
    match_cache = match #only occurs here (prevents redrawing graphs if the match is the same)
    return fig1, fig1Bar, fig2, fig2Bar, name1, name2

def match_placement_view():
    #html/formatting stuff below >_<
    graph1 = dcc.Graph(
        id='graph-player1-placement'
    )
    graph1Bar = dcc.Graph(
        id='graph-player1-placement-bar',
    )
    graph2 = dcc.Graph(
        id='graph-player2-placement',
    )
    graph2Bar = dcc.Graph(
        id='graph-player2-placement-bar',
    )
    graph1Plot = dbc.Card(
        [
            html.Div([
                graph1
            ]),
        ],
        body=True)
    graph1BarPlot = dbc.Card(
        [
            html.Div([
                graph1Bar
            ]),
        ],
        body=True)
    graph2Plot = dbc.Card(
        [
            html.Div([
                graph2
            ]),
        ],
        body=True)
    graph2BarPlot = dbc.Card(
        [
            html.Div([
                graph2Bar
            ]),
        ],
        body=True)

    player1Title = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Player: ", className="card-title", id="player-1-name-placement"),
                ]
            ),
        ]
    )
    player2Title = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Player: ", className="card-title", id="player-2-name-placement"),
                ]
            ),
        ]
    )
    hiddenStateDiv = html.Div(id='hidden-div', style={'display':'none'})
    group1 = dbc.CardGroup([graph1Plot,graph1BarPlot])
    group2 = dbc.CardGroup([graph2Plot,graph2BarPlot])
    plot = dbc.Card([
        dbc.Row(dbc.Col([player1Title])),
        dbc.Row(dbc.Col([group1])),
        dbc.Row(dbc.Col([player2Title])),
        dbc.Row(dbc.Col([group2])),
        hiddenStateDiv
    ])
    return plot
