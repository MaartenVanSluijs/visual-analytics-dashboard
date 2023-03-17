from dash import dcc
import numpy as np
from dash import html


def generate_header():
    return html.Header(
        id="title",
        children=[
            html.H1(
                children="Nature Preserve ",
                style={
                    'textAlign': 'center'
                }),
            html.Div(
                id="description",
                children="Welcome to this visualization dashboard. On this dashboard, you can find out all about the behavior of cars on the roads in the preserve",
                style={
                    'textAlign': 'center'
                }
            ),
        ],
    )

def generate_control_card(df):
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Car Type",  style={"font-weight": "bold"}),
            html.Hr(),
            dcc.Dropdown(
                id="map_var",
                options=df["car-type"],
                value="price"
            ),
        ],
    )