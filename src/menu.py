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
                id="car_type",
                options=[{"label": "two-axle car", "value": "1"}, 
                            {"label": "two-axle truck", "value": "2"}, 
                            {"label": "two-axle truck (park service)", "value": "2P"}, 
                            {"label": "three-axle truck", "value": "3"}, 
                            {"label": "four-axle (and above) truck", "value": "4"}, 
                            {"label": "two-axle bus", "value": "5"},
                            {"label": "three-axle bus", "value": "6"}],
                value= "1",
                clearable=False
            ),
            html.Hr(),
            dcc.RangeSlider(
                id="month",
                min=1,
                max=12,
                step=None,
                marks={
                    1: 'January',
                    2: 'February',
                    3: 'March',
                    4: 'April',
                    5: 'May',
                    6: 'June',
                    7: 'July',
                    8: 'August',
                    9: 'September',
                    10: 'October',
                    11: 'November',
                    12: 'December'                            
                },
                value=[1, 12]
            ),
        ],
    )