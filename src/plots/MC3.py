from dash import dcc, html
import plotly.express as px
import json
import numpy as np

class MC3(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
        self.files = {"1":"data/MC3/processed/01_2014_03_17.json",
                      "2":"data/MC3/processed/02_2014_08_24.json",
                      "3":"data/MC3/processed/03_2014_11_28.json",
                      "4":"data/MC3/processed/04_2014_12_30.json",
                      "5":"data/MC3/processed/05_2015_02_15.json",
                      "6":"data/MC3/processed/06_2015_06_24.json",
                      "7":"data/MC3/processed/07_2015_09_12.json",
                      "8":"data/MC3/processed/08_2015_11_15.json",
                      "9":"data/MC3/processed/09_2016_03_06.json",
                      "10":"data/MC3/processed/10_2016_06_26.json",
                      "11":"data/MC3/processed/11_2016_09_06.json",
                      "12":"data/MC3/processed/12_2016_12_19.json"}
        self.date = ""

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )
        # Load in the raw image data
        self.data = self.get_data("1")
    
    def get_data(self, image_number):
        file = open(self.files[str(image_number)])
        self.date = self.files[str(image_number)][-15:-5]
        image_json = json.load(file)
        return image_json

    def update(self, image_type, image_number, triggered_id):

        if triggered_id == "mc3_image_slider":
            # Load in the new image data
            self.data = self.get_data(image_number)

        dtype = np.uint8 if image_type != "NDVI" else None 
        image = np.array(self.data[image_type], dtype=dtype)
        fig = px.imshow(image, title="Preserve on " + self.date)
        return fig