'''Displays Match Placement Plot'''
from dash import dcc
from dash import html
import os
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import dash_bootstrap_components as dbc

def match_placement_view():
    df_sample = pd.DataFrame({
        "serve": ["Serve 1", "Serve 2"],
        "x": [.2,.8],
        "y": [.4,.6],
        "player": ["Player 1", "Player 2"],
        "team": ["Home","Away"],
        "size": [.05,.05],
    })

    colour0 = "#009BFF"
    colour1 = "grey"
    colour_ball = "red"

    color_discrete_map = {"Home": colour0, "Away": colour1, "Ball": colour_ball}

    
    # Plotly Express version
    fig = px.scatter(
        df_sample,
        x="x",
        y="y",
        color="team",
        hover_name="player",
        range_x=[-0.05, 1.05],
        range_y=[-0.05, 1.05],
        size="size",
        size_max=10,
        opacity=0.8,
        color_discrete_map=color_discrete_map,
        text="serve",
        hover_data={
            "x": False,
            "y": False,
            "team": False,
        },
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

    pio.templates["custom_dark"] = go.layout.Template()
    pio.templates["custom_dark"]["layout"]["paper_bgcolor"] = "#282828"
    pio.templates["custom_dark"]["layout"]["plot_bgcolor"] = "#282828"

    fig.update_layout(
        template="custom_dark",
        xaxis=dict(showgrid=False, showticklabels=False),
        # plot_bgcolor='#282828',
        # paper_bgcolor='#282828'
    )

    fig.update_layout(margin=dict(l=20, r=20, b=20, t=20))

    fig.update_layout(
        legend_orientation="v", transition={"duration": 0, "ordering": "traces first"}
    )

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
