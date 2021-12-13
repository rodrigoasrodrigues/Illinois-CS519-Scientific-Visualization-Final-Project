'''Displays Match Placement Plot'''
from dash import dcc
from dash import html
import os
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import random

def drawMapGraph(df, xVal):
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
        npLocationX[index] = location[0] + (random.random()*2 - 1)*.08#(random.random()*2 - 1)*npBigSize[index]
        npLocationY[index] = location[1] + (random.random()*2 - 1)*npBigSize[index]
        index+=1
    df_sample = pd.DataFrame({
        "Location": npBigIndex,
        "x": npLocationX,
        "y": npLocationY,
        "size": npBigSize,
        "RelativeServes": npBigRelSize,
        "Number Of Serves": npBigVals
    })
    # Plotly Express version
    fig = px.scatter(
        df_sample,
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
    npIndex = df.columns.values #grabs the names of the selected columns
    for i, loc in enumerate(npIndex):
        npIndex[i] = loc.replace("_", " ") #replace names so they are a bit more human readable (get rid of "_" and replace with " ")
    npVals = df.values[0].astype(np.int64) #grabs the values of the selected row
    df_sample = pd.DataFrame({
        "Location": npIndex,
        "Value": npVals
    })
    fig = px.bar(
        df_sample,
        x=npIndex,
        y=npVals,
    )
    #hiding axis labels
    #from: https://stackoverflow.com/questions/63386812/plotly-how-to-hide-axis-titles-in-a-plotly-express-figure-with-facets
    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''
    return fig

def match_placement_view():
    matchName = '19751219-M-Davis_Cup_World_Group_F-RR-Bjorn_Borg-Jiri_Hrebec'
    file = "charting-m-stats-ServeDirection.csv"
    file_plus_path = "data/" + file
    odf = pd.read_csv(file_plus_path,names=['match_id','row','deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t','err_net','err_wide','err_deep','err_wide_deep','err_foot','err_unknown'])
    df1 = odf.loc[(odf['match_id']==matchName) & (odf['row'] == '1 Total')]
    df1 = pd.DataFrame(df1,columns=['deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t'])
    fig1 = drawMapGraph(df1,0.4)
    fig1Bar = drawBarGraph(df1)

    df2 = odf.loc[(odf['match_id']==matchName) & (odf['row'] == '2 Total')]
    df2 = pd.DataFrame(df2,columns=['deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t'])
    fig2 = drawMapGraph(df2,0.4)
    fig2Bar = drawBarGraph(df2)

    graph1 = dcc.Graph(
        id='graph-player1-placement',
        figure=fig1
    )
    graph1Bar = dcc.Graph(
        id='graph-player1-placement-bar',
        figure=fig1Bar
    )
    graph2 = dcc.Graph(
        id='graph-player2-placement',
        figure=fig2
    )
    graph2Bar = dcc.Graph(
        id='graph-player2-placement-bar',
        figure=fig2Bar
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
                    html.H4("Player: (player1)", className="card-title"),
                ]
            ),
        ]
    )
    player2Title = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Player: (player2)", className="card-title"),
                ]
            ),
        ]
    )

    group1 = dbc.CardGroup([graph1Plot,graph1BarPlot])
    group2 = dbc.CardGroup([graph2Plot,graph2BarPlot])
    plot = dbc.Card([
        dbc.Row(dbc.Col([player1Title])),
        dbc.Row(dbc.Col([group1])),
        dbc.Row(dbc.Col([player2Title])),
        dbc.Row(dbc.Col([group2])),
    ])
    '''plot = dbc.Card([
        html.Div([
            dcc.Graph(
                    id='graph-player1-placement',
                    figure=fig
                )
            ])
        ],
        body=True)'''
    return plot
