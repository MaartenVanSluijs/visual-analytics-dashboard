from src.main import app
from src.menu import generate_header, generate_control_card
from data.MC1.data_cleanup import process_data

from src.plots.MC1 import MC1
from src.plots.entrance_plot import Entrance_plot
from src.plots.coefficient_plot import Coefficient_plot
from src.plots.speed_bar_plot import SpeedBar

from dash import html, ctx, dcc
from dash.dependencies import Input, Output
import pandas as pd


if __name__ == '__main__':
    # read in data 
    original_df = pd.read_csv("data\MC1\SensorData.csv")
    df_speed = pd.read_csv("data\MC1\speed.csv")

    # Create instances for visualizations
    mc1 = MC1("mc1")
    speedbar = SpeedBar("speedbar", df_speed)
    entrance = Entrance_plot("entrance")
    coefficient = Coefficient_plot("coefficient")

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Header(
                id="header",
                className="twelve columns", 
                children=generate_header()
            ),

            # Left column
            html.Div(
                id="left-column",
                className="seven columns",
                children=[
                    mc1
                ]
            ),

            # Right column
            html.Div(
                id="right-column",
                className="five columns",
                children=[
                    generate_control_card(original_df),
                    speedbar
                ]
            ),
        ]
    )

    # @app.callback(
    #     Output(entrance.html_id, "figure"),
    #     Input("car_type", "value"),
    #     Input("month", "value")        
    # )
    # def update_entrance(car_type, month):
    #     return entrance.update(car_type, month, ctx.triggered_id)

    @app.callback(
        Output(mc1.html_id, "figure"), [
        Input(mc1.html_id, "clickData"),
        Input("car_type", "value")
        ]
    )
    def update(click_data, car_type):
        return mc1.update(car_type)
    
    # @app.callback(Output(coefficient.html_id, "figure"),
    #               Input(coefficient.html_id, "clickData")
    # )
    # def update(click_data):
    #     return coefficient.update()

    @app.callback(
        Output(speedbar.html_id, "figure"), 
        Input("car_type", "value"), 
        Input(mc1.html_id, "clickData"),
    )
    def update(car_type, click_data):
        print(click_data)
        if click_data is not None and len(click_data["points"]) >= 2: 
            start_node = click_data["points"][0]["x"], click_data["points"][0]["y"]
            end_node = click_data["points"][1]["x"], click_data["points"][1]["y"]
            return speedbar.update(car_type, start_node, end_node)

    
    app.run_server(debug=True, dev_tools_ui=True)