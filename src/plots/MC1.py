from dash import dcc, html
import plotly.express as px
from PIL import Image
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
        return Image.open(url_map)
    
    def get_unique_year_month(self)->list:
        return self.df_data['month-year'].unique()
    
    def change_colors_heatmap(self, plotly_color, opacity=1.0):
        # set empty list
        chgd_plotly_color=[]

        # loop over colors in list
        for index, color in enumerate(plotly_color):
                color_string = color.replace('rgb', 'rgba')
                if index == 0:
                    pass
                    color_string = color_string.replace(')',f', {str(0)})')
                else:
                    color_string = color_string.replace(')',f', {str(opacity)})')
                chgd_plotly_color.append(color_string)
        return chgd_plotly_color
    
    def make_car_heatmap(self)->go.Figure:
        img_width, img_height = self.map.size
        scale_factor = 3
        heat_max = 100

        df_data_scaled = self.df_data.copy()
        df_data_scaled['x'] = df_data_scaled['x'] * scale_factor
        df_data_scaled['y_flipped'] = df_data_scaled['y_flipped'] * scale_factor

        fig = px.density_heatmap(df_data_scaled, x='x', y='y_flipped', animation_frame='day-month-year', animation_group='day-month-year', 
                                width=img_width * scale_factor, height=img_height * scale_factor, nbinsx=100, nbinsy=100, 
                                range_color=[0, heat_max], range_x=[0, img_width * scale_factor], range_y=[0, img_height * scale_factor], 
                                color_continuous_scale=self.change_colors_heatmap(px.colors.sequential.Jet, opacity=0.95)
                                )


        # Configure axes
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
                source=self.map)
        )

        # Configure other layout
        fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )

        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5

        return fig

    def update(self)->go.Figure:
        fig = self.make_car_heatmap()
        return fig