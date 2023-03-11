from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import pandas as pd

class MC1(html.Div):
    def __init__(self, name, url_data="data\MC1\SensorData.csv"):
        self.html_id = name.lower().replace(" ", "-")
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )
        # Load in the raw image data
        self.df_data = self.preprocess_raw_data(url_data)

    def preprocess_raw_data(self, url):
        df = pd.read_excel(url)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df

    
    
    def update(self):
        print("Hello World!")