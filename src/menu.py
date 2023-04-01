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
                options=[{"label": "All cars", "value": "0"},
                                 {"label": "Two-axle car", "value": "1"}, 
                                 {"label": "Two-axle truck", "value": "2"}, 
                                 {"label": "Two-axle truck (park service)", "value": "2P"}, 
                                 {"label": "Three-axle truck", "value": "3"}, 
                                 {"label": "Four-axle (and above) truck", "value": "4"}, 
                                 {"label": "Two-axle bus", "value": "5"},
                                 {"label": "Three-axle bus", "value": "6"}],
                value= "0",
                clearable=False
            ),
            html.Hr(),
            dcc.RangeSlider(
                id="month",
                min=1,
                max=13,
                step=None,
                marks={
                    1: "May 2015",
                        2: 'June',
                        3: 'July',
                        4: 'August',
                        5: 'September',
                        6: 'October',
                        7: 'November',
                        8: 'December',
                        9: 'January 2016',
                        10: 'February',
                        11: 'March',
                        12: 'April',
                        13: "May 2016"                         
                    },
                value=[1, 13]                          
            ),
        ],
    )