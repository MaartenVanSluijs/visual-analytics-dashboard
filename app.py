from src.main import app
from src.menu import generate_header, generate_control_card
from data.MC1 import data_cleanup
from data.MC1.data import get_data 

from src.plots.MC1 import MC1
from src.plots.entrance_plot import Entrance_plot

from dash import html, ctx, dcc
from dash.dependencies import Input, Output


if __name__ == '__main__':
    df_mc1 = get_data()
    # len_shortest_paths, shortest_paths = data_cleanup.shortest_paths()
    mc1 = MC1("mc1", df_mc1)
    entrance = Entrance_plot("entrance")

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=[
                    # Top graph
                    entrance,

                    html.Br()

                    # Bottom graph
                ]
            ),

            html.Div(
                id="center-column",
                className="nine columns",
                children=[
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
                    mc1
                ]
            )
        ],
    )

    @app.callback(
        Output(entrance.html_id, "figure"),
        Input("car_type", "value"),
        Input("month", "value")        
    )
    def update_entrance(car_type, month):
        return entrance.update(car_type, month, ctx.triggered_id)

    @app.callback(
        Output(mc1.html_id, "figure"), [
        Input(mc1.html_id, "clickData")
        ]
    )
    def update(click_data):
        return mc1.update()

    app.run_server(debug=True, dev_tools_ui=True)