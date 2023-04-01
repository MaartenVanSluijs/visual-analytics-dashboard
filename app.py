from src.main import app
from src.menu import generate_header, generate_control_card
from data.MC1.data_cleanup import process_data

from src.plots.MC1 import MC1
from src.plots.entrance_plot import Entrance_plot
from src.plots.coefficient_plot import Coefficient_plot
from src.plots.speed_bar_plot import SpeedBar
from src.plots.regression_plot import Regression_plot
from src.plots.hover_plot import Hover_plot


from dash import html, ctx, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd


if __name__ == '__main__':

    # read in data 
    original_df = pd.read_csv("data\MC1\SensorData.csv")
    df_speed = pd.read_csv("data\MC1\speed.csv")

    # Create instances for visualizations
    mc1 = MC1("mc1")
    speedbar = SpeedBar("speedbar", df_speed)

    entrance = Entrance_plot("entrance")
    regression = Regression_plot("regression")
    map = MC1("map")
    hover = Hover_plot("hover")

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
                    speedbar,
                    regression
                ]
            ),
        ]
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