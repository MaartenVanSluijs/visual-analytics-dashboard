from dash import dcc, html
import plotly.express as px
import json
import numpy as np

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
        # Load in the raw image data
        self.data = self.get_data()

    def get_data(self):
        return
        # print("Hello World!")
    
    def update(self):
        return
        # print("Hello World!")