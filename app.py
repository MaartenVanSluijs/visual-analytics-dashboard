from src.main import app
from src.menu import generate_header, generate_control_card
from data.MC1.data import get_data 

from src.plots.MC1 import MC1
from src.plots.entrance_plot import Entrance_plot
from src.plots.coefficient_plot import Coefficient_plot

from dash import html, ctx, dcc
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # len_shortest_paths, shortest_paths = data_cleanup.shortest_paths()
    mc1 = MC1("mc1")
    entrance = Entrance_plot("entrance")
    coefficient = Coefficient_plot("coefficient")

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="center-column",
                className="four columns",
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
                        value= "1",
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
                    mc1
                ]
            )
        ],
    )

    @app.callback(
        Output(mc1.html_id, "figure"), [
        Input(mc1.html_id, "clickData"),
        Input("car_type", "value")
        ]
    )
    def update(click_data, car_type):
        return mc1.update(car_type)

    app.run_server(debug=True, dev_tools_ui=True)