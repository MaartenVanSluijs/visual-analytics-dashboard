from dash import dcc, html
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd

class MC2(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
        self.df_weather = self.get_weather_data()
        self.df_sensor = self.get_sensor_data()
        self.chemicals = self.get_chemicals()

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )
        # Load in the raw image data
        # self.data = self.get_data("1")

    def get_weather_data(self, url='data\\MC2\\raw\Meteorological_Data.xlsx'):
        # print current working directory
        df_weather = pd.read_excel(url)
        df_weather = df_weather.drop(df_weather.columns[[3,4]], axis=1)
        df_weather = df_weather.dropna()
        return df_weather
    
    def get_sensor_data(self, url='data\MC2\\raw\Sensor_Data.xlsx'):
        df_sensor = pd.read_excel(url)
        df_sensor = df_sensor.dropna()
        return df_sensor
    
    def get_chemicals(self):
        return self.df_sensor['Chemical'].unique()
    
    def month_nr_to_name(self, month_nr):
        return pd.to_datetime(month_nr, format='%m').strftime('%B')

    def chemical_line_plot(self, chemicals, months, colors=['red', 'blue', 'yellow', 'orange']):
        fig = make_subplots(rows=len(chemicals), cols=len(months), shared_yaxes=True, subplot_titles=[self.month_nr_to_name(month) for month in months])
        bool_legend = True

        for index_month, month in enumerate(months):
            for index_chem, chemical in enumerate(chemicals):
                color = colors[index_chem]
                df = self.df_sensor[(self.df_sensor['Chemical'] == chemical) & (self.df_sensor['Date Time '].dt.month == month)]
                fig.add_trace(go.Scatter(x=df['Date Time '], y=df['Reading'], name=f'{chemical}', line=dict(color=color, width=4), 
                                         showlegend=bool_legend), row=index_chem+1, col=index_month+1)
            bool_legend = False
        return fig

    def update(self, chemical, month, triggered_id):
        fig = self.chemical_line_plot(chemical, month)
        return fig