from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from matplotlib import image, pyplot
import  PIL.Image as Image
from data.MC1.data import get_data
import pandas as pd

class MC1(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )
        
        self.image = Image.open("data\MC1\Lekagul Roadways.bmp")
        self.df = get_data()
        self.df["day"] = pd.to_datetime(self.df["Timestamp"]).dt.date
        self.locations = pd.read_parquet("data\MC1\locations.parquet").sort_values(by="location")
        self.colours = {"camping": "#FF6A00", "entrance": "#4CFF00", "gate": "#FF0000", "general-gate": "#00FFFF", "ranger-bas": "#FF00DC", "ranger-stop": "#FFD800"}

        self.fig = go.Figure()
    
    def update(self, click_data):

        number_of_days = len(self.df.groupby("day", as_index=False).count().index)

        gate_count = self.df.groupby("gate-name").count().rename(columns={"Timestamp": "count"}).drop(["car-id", "car-type", "year-month", "x", "y"], axis=1)
        gate_count["avg_count"] = gate_count["count"].div(number_of_days).round(2)
        # get width and height of image PIL
        img_width, img_height = self.image.size
        scale_factor = 3

        x_values = [x[0]*scale_factor for x in self.locations['coordinates']]
        y_values = [(200-x[1])*scale_factor for x in self.locations['coordinates']]
        location_type = [location[:-1] for location in self.locations["location"]]

        df_plot = pd.DataFrame({"x": x_values, "y": y_values, "location_type": location_type, "size": gate_count["avg_count"]})
        
        fig = px.scatter(df_plot, x='x', y='y', size='size', color="location_type", color_discrete_map=self.colours) 


        fig.update_xaxes(
            visible=False,
        )

        fig.update_yaxes(
            visible=False,
        )

        # Add image
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                opacity=1.0,
                layer="below",
                sizing="stretch",
                source=self.image)
        )

        # Configure other layout
        fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        return fig
