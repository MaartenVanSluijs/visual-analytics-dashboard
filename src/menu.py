from dash import dcc
import numpy as np
from dash import html


def generate_header():
    '''
    Generates the header with text and the filters for visualizations
    '''
    
    return [
        # Title
        html.Header(
            id="title",
            children=[
                html.H1(
                    id="header_title",
                    children="WildWheelsTracker",
                    style={
                        'textAlign': 'center'
                    }),
            ],
        ),

        # Text for point selector
        html.Header(
            id="text", 
            children=[
                html.H5(id="points_header", children="Currently selected points"),
            ]
        ),
        
        # Filters
        html.Header(
            id="filters",
            children=[
                html.Div(
                    id="selection",
                    className="header_element",
                    children=[
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
