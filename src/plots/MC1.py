from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from matplotlib import image, pyplot
from data.MC1.data import get_data

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
        
        self.image = image.imread("data\MC1\Lekagul Roadways.bmp")
        self.df = get_data()

        self.fig = go.Figure()

    def update(self):
        # self.fig.add_trace(go.Bar(self.df, x="car-type"))
        # print("Hello World!")

        fig = px.imshow(self.image)
        return fig