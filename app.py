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
    locations = pd.read_parquet("data\MC1\locations.parquet").sort_values(by="location")

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
            dcc.Store("selected_points"),
            dcc.ConfirmDialog(id="more_than_2", message="You can only select two points, you can clear the selection to select other points"),
            dcc.ConfirmDialog(id='popup', message='Too few cars have driven between these points, or the are not direct neighbours'),
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
                    html.H3(id="points_header", children="Hallo"),
                    html.Button("Analyze road", id="button", n_clicks=0),
                    html.Button("Reset selection", id="reset", n_clicks=0),
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

    # Callback for more than 2 popup
    @app.callback(
        Output('more_than_2', 'displayed'),
        Input(map.html_id, 'clickData'),
        State("selected_points", "data")
        )
    def display_more_than_two(click_data, data):
        if data != None:
            # The case where more than 2 points are selected
            if data[1] != None:
                return True
        return False
    
    # Callback for the popup
    @app.callback(
        Output('popup', 'displayed'),
        Input(map.html_id, 'clickData'),
        State("selected_points", "data")
        )
    def display_popup(click_data, data):
        if data != None:
            # The case where the points are not neighbours
            if data[0] != None and data[1] == None:
                x = click_data["points"][0]["x"]
                y = click_data["points"][0]["y"]
                if not is_neighbour(data[0], [x, y]):
                    return True
        return False

    # Callback for the store
    @app.callback(
        Output("selected_points", "data"),
        Input(map.html_id, "clickData"),
        Input("button", "n_clicks"),
        Input("reset", "n_clicks"),
        State("selected_points", "data"),
        State("month", "value"),
        State("car_type", "value")
    )
    def update_store(click_data, n_clicks_button, n_clicks_reset, data, month, car_type):
        # In case either of the buttons is pressed
        if ctx.triggered_id == "reset":
            return [None, None]
        
        if ctx.triggered_id == "button":
            return data

        # In case the map updates the store
        if data == None:
            store_data = [None, None]
        else:
            store_data = data

        if store_data[1] != None:
            return store_data

        if click_data != None:

            x = click_data["points"][0]["x"]
            y = click_data["points"][0]["y"]

            neighbour = True
            if store_data[0] != None:
                neighbour = is_neighbour(store_data[0], [x,y])
                if not neighbour:
                    return store_data

            # Find which gate is being clicked on
            gate = ""
            for index, value in locations.iterrows():
                if value["coordinates"][0] * 4 == x and (200 - value["coordinates"][1]) * 4 == y:
                    gate = value["location"]

            if store_data[0] == None:
                store_data[0] = gate
            else:
                store_data[1] = gate

        return store_data
        

    # Callback for the header
    @app.callback(
        Output("points_header", "children"),
        Input("selected_points", "data")
    )
    def update_header(data):
        header_text = "Currently selected points: "
        
        for gate in data:
            if gate != None:
                header_text += (gate + ", ")

        return header_text[:-2]

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
        print(hover_data)
        if hover_data is None:
            return False, None, None
        
        if hover_data["points"][0]["curveNumber"] != 0:
            
            pt = hover_data["points"][0]
            bbox = pt["bbox"]
            x = pt["x"]
            y = pt["y"]

            point = [x,y]
            
            children = [
                dcc.Graph(figure=hover.get_plot(point, month))
            ]

            return True, bbox, children
        
        else:
            return False, None, None

    # Callback for the regression plot
    @app.callback(
        Output(regression.html_id, "figure"), [
        Input("car_type", "value"),
        Input("month", "value"),
        Input("button", "n_clicks"),
        Input("reset", "n_clicks"),
        State("selected_points", "data")
        ]
    )
    def update_regression(car_type, month, n_clicks_1, n_clicks_2, car_path):
        if ctx.triggered_id == "reset":
            return regression.update(car_type, month, [None, None])
        return regression.update(car_type, month, car_path)

    # Callback for the speed plot
    @app.callback(
        Output(speed.html_id, "figure"), 
        Input("car_type", "value"), 
        Input("month", "value")
    )
    def update(car_type, months):
        return speed.update(car_type, months)
        
    # Callback for the car plot
    @app.callback(
        Output(cars.html_id, "figure"), 
        Input("car_type", "value"), 
        Input("month", "value")
    )
    def update(car_type, months):
        return cars.update(car_type, months)
        
    def is_neighbour(gate, point):
        neighbour = True
        new_point = [int(point[0] / 4), int(200 - (point[1] / 4))]
        current_point = locations.loc[locations["location"] == gate]["coordinates"].to_list()[0]
        
        speed_filtered = df_speed.loc[((df_speed["start-x"] == current_point[0]) & (df_speed["start-y"] == current_point[1]) &
                                       (df_speed["end-x"] == new_point[0]) & (df_speed["end-y"] == new_point[1])) |
                                      ((df_speed["end-x"] == current_point[0]) & (df_speed["end-y"] == current_point[1]) &
                                       (df_speed["start-x"] == new_point[0]) & (df_speed["start-y"] == new_point[1]))]
        
        speed_filtered["day"] = pd.to_datetime(speed_filtered["start-time"]).dt.date
        if len(speed_filtered.groupby("day")) < 15:
            neighbour = False

        return neighbour
    
    app.run_server(debug=True, dev_tools_ui=True)