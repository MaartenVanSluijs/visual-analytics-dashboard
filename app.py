from src.main import app
from src.menu import generate_header, generate_control_card
from data.MC1.data import get_data 

from src.plots.MC1 import MC1
from src.plots.entrance_plot import Entrance_plot
from src.plots.regression_plot import Regression_plot
from src.plots.hover_plot import Hover_plot

from dash import html, ctx, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State


if __name__ == '__main__':
    # len_shortest_paths, shortest_paths = data_cleanup.shortest_paths()
    entrance = Entrance_plot("entrance")
    regression = Regression_plot("regression")
    map = MC1("map")
    hover = Hover_plot("hover")

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="center-column",
                className="twelve columns",
                children=[
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
                    regression,
                    map,
                    dcc.Tooltip(id="graph-tooltip")
                ]
            )
        ],
    )

    # Callback for the map plot
    @app.callback(
        Output(map.html_id, "figure"), [
        Input("car_type", "value"),
        Input("month", "value")
        ]
    )
    def update_map(car_type, month):
        return map.update(car_type, month)
    
    @app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input(map.html_id, "hoverData"),
    State("month", "value")
    )
    def display_hover(hover_data, month):
        if hover_data is None:
            return False, None, None
        
        pt = hover_data["points"][0]
        bbox = pt["bbox"]
        x = pt["x"]
        y = pt["y"]

        point = [x,y]
        
        children = [
            dcc.Graph(figure=hover.get_plot(point, month))
        ]

        return True, bbox, children

    # Callback for the regression plot
    @app.callback(
        Output(regression.html_id, "figure"), [
        Input("car_type", "value"),
        Input("month", "value")
        ]
    )
    def update_regression(car_type, month):
        return regression.update(car_type, month)

    app.run_server(debug=True, dev_tools_ui=True)