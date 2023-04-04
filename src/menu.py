from dash import dcc
import numpy as np
from dash import html


def generate_header():
    return [
        html.Header(
        id="title",
        children=[
            html.H1(
                id="header_title",
                children="Nature Preserve ",
                style={
                    'textAlign': 'center'
                }),
        ],
        ),
        html.Header(
            id="text", 
            children=[
                html.H5(id="points_header", children="Currently selected points"),
            ]
        ),
        
        html.Header(
            id="filters",
            children=[
                html.Div(
                    id="selection",
                    className="header_element",
                    children=[
                        # html.H5(id="points_header", children="Currently selected points"),
                        html.Button("Analyze road", id="button", n_clicks=0),
                        html.Button("Reset selection", id="reset", n_clicks=0)
                    ]
                ),

                dcc.Dropdown(
                    id="car_type",
                    className="header_element",
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

                dcc.RangeSlider(
                    id="month",
                    min=1,
                    max=13,
                    step=None,
                    marks={
                        1: {"label": "May 2015", "style": {"transform": "rotate(45deg)"}},
                            2: {"label": "June", "style": {"transform": "rotate(45deg)"}},
                            3: {"label": "July", "style": {"transform": "rotate(45deg)"}},
                            4: {"label": "Aug", "style": {"transform": "rotate(45deg)"}},
                            5: {"label": "Sept", "style": {"transform": "rotate(45deg)"}},
                            6: {"label": "Oct", "style": {"transform": "rotate(45deg)"}},
                            7: {"label": "Nov", "style": {"transform": "rotate(45deg)"}},
                            8: {"label": "Dec", "style": {"transform": "rotate(45deg)"}},
                            9: {"label": "Jan 2016", "style": {"transform": "rotate(45deg)"}},
                            10: {"label": "Feb", "style": {"transform": "rotate(45deg)"}},
                            11: {"label": "March", "style": {"transform": "rotate(45deg)"}},
                            12: {"label": "April", "style": {"transform": "rotate(45deg)"}},
                            13: {"label": "May 2016", "style": {"transform": "rotate(45deg)"}}                        
                        },
                    value=[1, 13]                          
                ),
                
            ],
        )
    
    ]

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