from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from matplotlib import image, pyplot

class MC1(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )
        
        self.image = image.imread("data\MC1\Lekagul Roadways.bmp")

        self.fig = go.Figure()

    def update(self):
        # self.fig.add_trace(go.Bar(self.df, x="car-type"))
        # print("Hello World!")

        fig = px.imshow(self.image)
        return fig