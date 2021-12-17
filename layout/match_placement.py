'''Displays Match Placement Plot'''
from dash import dcc
from dash import html
from dash import no_update
from dash import callback_context
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
from utils import get_numerical_label_values, is_not_a_node

NOT_FOUND_STRING = "DETAILED DATA NOT AVAILABLE"

#reads from the file
file = "charting-m-stats-ServeDirection.csv"
file_plus_path = "data/" + file
odf = pd.read_csv(file_plus_path,names=['match_id','row','deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t','err_net','err_wide','err_deep','err_wide_deep','err_foot','err_unknown'])

#maps the tournament id from the dropdown to the match-id format
def getTouramentFromValue(value):
    valuePairs = {
        '2018-560': 'US_Open',
        '2018-540': 'Wimbledon',
        '2018-520': 'Roland_Garros',
        '2018-580': 'Australian_Open',
        'None': 'US_Open'
    }
    return valuePairs[value]

#makes updating the graphs when selecting from the dropdown easier
def getFinalistsFromTournament(tournament_id):
    namePairs = {
        '2018-560': ['Novak_Djokovic','Juan_Martin_del_Potro'],
        '2018-540': ['Kevin_Anderson','Novak_Djokovic'],
        '2018-520': ['Rafael_Nadal','Dominic_Thiem'],
        '2018-580': ['Marin_Cilic','Roger_Federer'],
    }
    return namePairs[tournament_id]

#makes updating the graphs when selecting from the dropdown easier
def getSurfaceFromTournament(tournament_id):
    surfacePairs = {
        '2018-560': 'Hard',
        '2018-540': 'Grass',
        '2018-520': 'Clay',
        '2018-580': 'Hard',
    }
    return surfacePairs[tournament_id]

#a simple way to format the round string from the depth value of the graph
def getDepthStringFromInt(value):
    depthList = ["N/A", "QF", "SF", "F", "N/A"]
    return depthList[value]

#grabs the round of the tournament (formatted), and player names. Names will be empty if the match isn't valid
def getMatchInfo(match):
    round = getDepthStringFromInt(match['points'][0]['depth'])
    if round == "N/A":
        return round, "", ""
    customData = match['points'][0]['customdata'].split('(')[0]
    splitData = customData.split('<br>')
    splitNames = splitData[0].split(' x ')
    name1 = splitNames[0].strip().replace(' ','_')
    name2 = splitNames[1].strip().replace(' ','_')
    return round, name1, name2

#reads from the serve direction file and outputs a dataframe matching parameters
def getMatchDataFrame(matchString, playerNum):
    df = odf.loc[(odf['match_id'].str.contains(matchString,case=False, na=False)) & (odf['row'] == f'{playerNum} Total')]
    df = pd.DataFrame(df,columns=['deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t'])
    return df

#formats the parameters into a string for searching the file
def getMatchString(tournament_id, round, name1, name2):
    matchString = f'-M-{getTouramentFromValue(tournament_id)}-{round}-{name1}-{name2}'
    return matchString

#draws the courts. df is a dataframe and xVal is the 'center' point for the random xValue for the court drawing distribution
def drawMapGraph(df, surface_type):
    if df.empty:
        return px.scatter(title=NOT_FOUND_STRING)
    location_map = {
        "deuce_wide": [.28,.82],
        "deuce_middle": [.28,.56], 
        "deuce_t": [.28,.675],
        "ad_wide": [.28,.18],
        "ad_middle": [.28,.46],
        "ad_t": [.28,.325],
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
            npBigSize[bigIndex]=0.035#npSize[index]
            npBigRelSize[bigIndex]=npSize[index]
            bigIndex+=1
        index+=1
    npLocationX = np.zeros(npBigVals.shape[0],dtype=np.float64) #gets X position of where serve should be
    npLocationY = np.zeros(npBigVals.shape[0],dtype=np.float64) #gets Y position of where serve should be
    index = 0
    #add some random spreading to the points
    random.seed(123)
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
    image_file = 'assets/Court_' + surface_type + '.png'
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

#draws the bar graphs for player serve placement
def drawBarGraph(df, surface_type):
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
    #surface_color = 'mediumslateblue'
    #colors = [surface_color]
    formatted_df = pd.DataFrame({
        "Location": npIndex,
        "Value": npVals
    })
    fig = px.bar(
        formatted_df,
        x="Location",
        y="Value",
        #color_discrete_sequence=colors,
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

#updates the figures when the tournament plot is clicked
@app.callback(
    Output('graph-player1-placement', 'figure'),
    Output('graph-player1-placement-bar', 'figure'),
    Output('graph-player2-placement', 'figure'),
    Output('graph-player2-placement-bar', 'figure'),
    Output('player-1-name-placement', 'children'),
    Output('player-2-name-placement', 'children'),
    Input('tornament-plot', 'clickData'),
    Input('tournament-dropdown', 'value')
)
def update_graphs(match,tournamentString):
    
    #setting up some variables that will be used to generate our match-id string
    round = 'F'
    name1 = 'Novak_Djokovic'
    name2 = 'Juan_Martin_del_Potro'
    tournament_id = '2018-560'
    surface_type = 'Hard'
    #force_update is used to prevent the code from changing the variables - instead, they are set once for special conditions
    #special conditions include: initialization and dropdown selection
    #if the dropdown is selected, we manually set the names and id of the tournament once up here, and that's it!
    force_update = False
    #checking for special conditions
    if callback_context.triggered:
        which_input = callback_context.triggered[0]['prop_id'].split('.')[1]
        if which_input == 'value':
            force_update = True
            if tournamentString:
                tournament_id = tournamentString
            names = getFinalistsFromTournament(tournament_id)
            surface_type = getSurfaceFromTournament(tournament_id)
            name1, name2 = names[0], names[1]
    else: #in the event of initialization, make sure we use those default values for the variables
        force_update = True

    #check if the 'match' data is from a click on a node or a link. If a link, (lacks 'depth' key in data) then try to return the cached data as before (do nothing). Otherwise continue
    if is_not_a_node(match) and not force_update:
        return [no_update] * 6 #prevents all 6 elements from updating
    elif not force_update: #if it is a node, get parse the match string for the round and names
        round, name1, name2 = getMatchInfo(match)
    #get extra data if it exists
    match_extraData = get_numerical_label_values(match)

    #extract the needed extra data here
    if match_extraData and not force_update:
        #match_num = match_extraData[0]
        tournament_id = match_extraData[1]
        surface_type = match_extraData[2]
    
    #try to generate a string for the match id. Try to get one dataframe from it to see if it exists
    matchString = getMatchString(tournament_id, round, name1, name2)
    df1 = getMatchDataFrame(matchString,1)

    if df1.empty: #IF we couldn't find data, flip the names!
        name1, name2 = name2, name1
        matchString = getMatchString(tournament_id, round, name1, name2)
        df1 = getMatchDataFrame(matchString,1)
    
    #NOTE: IF we couldn't find data even after flipping the names, it probably just doesn't exist

    df2 = getMatchDataFrame(matchString,2)

    #generate graphs from the two dataframes
    fig1 = drawMapGraph(df1,surface_type)
    fig1Bar = drawBarGraph(df1,surface_type)

    fig2 = drawMapGraph(df2,surface_type)
    fig2Bar = drawBarGraph(df2,surface_type)

    #format player names for display (replace '_' with ' ')
    name1 = f"Player: {name1.replace('_',' ')}"
    name2 = f"Player: {name2.replace('_',' ')}"
    #return the figures/values!
    return fig1, fig1Bar, fig2, fig2Bar, name1, name2

#sets up the HTML
def match_placement_view():
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
                ], className="card_title"
            ),
        ]
    )
    player2Title = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Player: ", className="card-title", id="player-2-name-placement"),
                ], className="card_title"
            ),
        ]
    )
    group1 = dbc.CardGroup([graph1Plot,graph1BarPlot])
    group2 = dbc.CardGroup([graph2Plot,graph2BarPlot])
    plot = dbc.Card([
        dbc.Row(dbc.Col([player1Title])),
        dbc.Row(dbc.Col([group1])),
        dbc.Row(dbc.Col([player2Title])),
        dbc.Row(dbc.Col([group2]))
    ])
    return plot
