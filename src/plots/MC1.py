from dash import dcc, html
import plotly.express as px
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import plotly.graph_objects as go

class MC1(html.Div):
    def __init__(self, name, url_data="data\MC1\SensorData_year_month.csv", url_map="data\MC1\Lekagul Roadways.bmp"):
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
        self.year_months = self.get_unique_year_month()

    def preprocess_raw_data(self, url:str)->pd.DataFrame:
        df = pd.read_csv(url)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df
    
    def get_map(self, url_map: str)->np.ndarray:
        img = mpimg.imread(url_map)
        return img
    
    def get_unique_year_month(self)->list:
        return self.df_data['month-year'].unique()

    def update(self)->go.Figure:
        fig = px.imshow(self.map)
        fig.add_trace(
            go.Histogram2d(
                x=self.df_data.x,
                y=self.df_data.y,
                xbins=dict(start=0, end=199, size=3),
                ybins=dict(start=0, end=199, size=3),
                colorscale="Turbo", 
                opacity=0.8
            )
        ) 
        return fig