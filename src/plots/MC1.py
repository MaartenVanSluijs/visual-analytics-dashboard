from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from matplotlib import image, pyplot
import  PIL.Image as Image
from data.MC1.data import get_data
import pandas as pd
from data.MC1.train_model import model_trainer

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
        self.locations = pd.read_parquet("data\MC1\locations.parquet")

        self.fig = go.Figure()

    def make_car_bubbles(self, coefficients)->go.Figure:
    # get width and height of image PIL
        img_width, img_height = self.image.size
        scale_factor = 4

        correlation = ["Positive" if x > 0 else "Negative" for x in coefficients]

        coefficients = [abs(x) for x in coefficients]

        x_values = [x[0]*scale_factor for x in self.locations['coordinates']]
        y_values = [x[1]*scale_factor for x in self.locations['coordinates']]

        df_plot = pd.DataFrame({'x': x_values, 'y': y_values, 'size': coefficients, 'name': self.locations['location'], 'correlation': correlation})
        fig = px.scatter(df_plot, x='x', y='y', size='size', hover_name='name', color='correlation', color_discrete_map={'Positive': 'green', 'Negative': 'red'})


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

    def update(self, car_type):
        trainer = model_trainer()
        fig = self.make_car_bubbles(trainer.run_prediction(car_type))

        return fig