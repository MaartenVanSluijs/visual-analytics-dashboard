from dash import dcc, html
import plotly.express as px
import matplotlib.image as mpimg
import numpy as np
import pandas as pd

class MC1(html.Div):
    def __init__(self, name, url_data="data\MC1\SensorData_processed.csv", url_map="data\MC1\Lekagul Roadways.bmp"):
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
        self.map = self.get_map(url_map)

    def preprocess_raw_data(self, url:str)->pd.DataFrame:
        df = pd.read_csv(url)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df
    
    def get_map(self, url_map: str)->np.ndarray:
        img = mpimg.imread(url_map)
        return img
        
    def update(self):
        fig = px.imshow(self.map)
        return fig