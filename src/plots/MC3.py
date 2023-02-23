from dash import dcc, html
import plotly.express as px
import json
import numpy as np

class MC3(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

        # Load in the raw image data
        self.data = self.get_data()
    
    def get_data(self):
        file = open("data/MC3/processed/01_2014_03_17.json")
        image_json = json.load(file)
        return image_json

    def update(self):
        image = np.array(self.data["RGB"], dtype=np.uint8)
        fig = px.imshow(image)
        return fig