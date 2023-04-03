from src.main import app
from src.menu import generate_header, generate_control_card
from data.MC1.data_cleanup import process_data

from src.plots.MC1 import MC1
from src.plots.entrance_plot import Entrance_plot
from src.plots.speed_plot import Speed
from src.plots.regression_plot import Regression_plot
from src.plots.hover_plot import Hover_plot
from src.plots.cars_plot import Cars


from dash import html, ctx, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd


if __name__ == '__main__':

    # read in data 
    original_df = pd.read_csv("data\MC1\SensorData.csv")
    df_speed = pd.read_csv("data\MC1\speed.csv")

    # Create instances for visualizations
    map = MC1("mc1")
    speed = Speed("speedbar", df_speed)

    entrance = Entrance_plot("entrance")
    regression = Regression_plot("regression")
    map = MC1("map")
    hover = Hover_plot("hover")
    cars = Cars("cars", df_speed)

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
                    html.H3(children="Hallo"),
                    map,
                    regression
                ]
            ),

            # Right column
            html.Div(
                id="right-column",
                className="five columns",
                children=[
                    generate_control_card(original_df),
                    speed,
                    cars, 
                    dcc.Tooltip(id="graph-tooltip")
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
    
    # Callback for the hover plot
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

    # Callback for the speed plot
    @app.callback(
        Output(speed.html_id, "figure"), 
        Input("car_type", "value"), 
        Input("month", "value")
    )
    def update(car_type, months):
        return speed.update(car_type, months)

    # Callback for the speed plot
    @app.callback(
        Output(cars.html_id, "figure"), 
        Input("car_type", "value"), 
        Input("month", "value")
    )
    def update(car_type, months):
        return cars.update(car_type, months)
    
    app.run_server(debug=True, dev_tools_ui=True)