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

    def make_car_bubbles(self)->go.Figure:
        img_width, img_height = self.map.size
        scale_factor = 3
        heat_max = 100

        df_data_scaled = self.df_data.copy()
        df_data_scaled['x'] = df_data_scaled['x'] * scale_factor
        df_data_scaled['y'] = df_data_scaled['y'] * scale_factor

        fig = px.scatter(df_data_scaled.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country", 
                         log_x=True, size_max=60)


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

    def update(self):
        # self.fig.add_trace(go.Bar(self.df, x="car-type"))
        # print("Hello World!")

        fig = self.make_car_bubbles()

        return fig