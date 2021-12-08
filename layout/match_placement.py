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

def match_placement_view():
    matchName = '19751219-M-Davis_Cup_World_Group_F-RR-Bjorn_Borg-Jiri_Hrebec'
    file = "charting-m-stats-ServeDirection.csv"
    file_plus_path = "data/" + file
    df = pd.read_csv(file_plus_path,names=['match_id','row','deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t','err_net','err_wide','err_deep','err_wide_deep','err_foot','err_unknown'])
    df = df.loc[(df['match_id']==matchName) & (df['row'] == '1 Total')]
    df = pd.DataFrame(df,columns=['deuce_wide','deuce_middle','deuce_t','ad_wide','ad_middle','ad_t'])
    location_map = {
        "deuce_wide": [.8,.2], #todo: accuracy
        "deuce_middle": [.8,.5], #todo: accuracy
        "deuce_t": [.8,.8], #todo: accuracy
        "ad_wide": [.2,.2], #todo: accuracy
        "ad_middle": [.2,.5], #todo: accuracy
        "ad_t": [.2,.8], #todo: accuracy
    }
    #https://tennishold.com/wp-content/uploads/2018/09/Deuce-Tennis-Court-Diagram.jpg
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
    npLocationX = np.zeros(npIndex.shape[0],dtype=np.float64) #gets X position of where serve should be
    npLocationY = np.zeros(npIndex.shape[0],dtype=np.float64) #gets Y position of where serve should be
    index = 0
    for i in npIndex:
        location = location_map[i]
        npLocationX[index] = location[0]
        npLocationY[index] = location[1]
        index+=1
    
    df_sample = pd.DataFrame({
        "location": npIndex,
        "x": npLocationX,
        "y": npLocationY,
        "size": npSize,
        "value": npVals
    })
    
    # Plotly Express version
    fig = px.scatter(
        df_sample,
        x="x",
        y="y",
        color="size",
        range_x=[-0.05, 1.05],
        range_y=[-0.05, 1.05],
        size="size",
        color_continuous_scale=px.colors.sequential.Rainbow,
        hover_data={"value": True},
        text="value"
    )

    # Add corner flags to prevent zoom and pitch distortion
    fig.add_scatter(
        x=[0, 0, 1, 1],
        y=[0, 1, 0, 1],
        mode="markers",
        marker=dict(size=1, color="grey"),
        name="Flags",
    )

    # Make jersey number really small inside markers
    fig.update_traces(
        textfont_size=7, textfont_color="white", hovertemplate=None, hoverinfo="none"
    )
    fig.update_yaxes(autorange="reversed")

    fig.update_layout(
        xaxis=dict(range=[-0.05, 1.05]),
        yaxis=dict(range=[-0.05, 1.05]),
        coloraxis_showscale=False,
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

    #pio.templates["custom_dark"] = go.layout.Template()
    #pio.templates["custom_dark"]["layout"]["paper_bgcolor"] = "#282828"
    #pio.templates["custom_dark"]["layout"]["plot_bgcolor"] = "#282828"

    fig.update_layout(
        #template="custom_dark",
        xaxis=dict(showgrid=False, showticklabels=False),
        # plot_bgcolor='#282828',
        # paper_bgcolor='#282828'
    )

    fig.update_layout(margin=dict(l=20, r=20, b=20, t=20))

    #fig.update_layout(
    #    legend_orientation="v", transition={"duration": 0, "ordering": "traces first"}
    #)

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
    # fig.update_layout(showlegend=False)
    fig.update_layout(legend=dict(font=dict(family="Arial", size=10, color="grey")))

    # Hide corner flag trace in the legend
    for trace in fig["data"]:
        if trace["name"] == "Flags":
            trace["showlegend"] = False


    plot = dbc.Card([
        html.Div([
            dcc.Graph(
                    id='example-graph',
                    figure=fig
                )
            ])
        ],
        body=True)
    return plot
