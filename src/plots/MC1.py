from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from matplotlib import image, pyplot
import  PIL.Image as Image
from data.MC1.data import get_data, filter_data
import pandas as pd

class MC1(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id, clear_on_unhover=True)
            ],
        )
        
        self.image = Image.open("data\MC1\Lekagul Roadways.bmp")

        # Get data and add a day column for identifying the amount of days in the df
        self.df = get_data()
        self.df["day"] = pd.to_datetime(self.df["Timestamp"]).dt.date
        
        self.locations = pd.read_parquet("data\MC1\locations.parquet").sort_values(by="location")
        # Colour codings per gate type
        self.colours = {"camping": "#FF6A00", "entrance": "#4CFF00", "gate": "#FF0000", "general-gate": "#00FFFF", "ranger-bas": "#FF00DC", "ranger-stop": "#FFD800"}

        self.fig = go.Figure()
    

    def update(self, car_type, month)->go.Figure:

        # get width and height of image PIL
        img_width, img_height = self.image.size
        scale_factor = 4

        # Filter the data on car_type and month
        filtered_df = filter_data(self.df, [car_type, month])
        if filtered_df.empty:
            print("This dataframe is empty")

        # Get the number of days in the selected data
        number_of_days = len(filtered_df.groupby("day", as_index=False).count().index)

        # Initialize a zeros df per location, to be filled later with the counts
        count_by_location = pd.DataFrame({"gate-name": self.locations["location"], "count": np.zeros((40))})
        count_by_location.set_index("gate-name", inplace=True)

        # Group the filtered data by gate name to get counts per gate
        gate_count = filtered_df.groupby("gate-name").count().rename(columns={"Timestamp": "count"}).drop(["car-id", "car-type", "year-month", "x", "y", "day"], axis=1)

        # Loop through all the gates
        for index, row in gate_count.iterrows():
            # Set the right count for each location
            count_by_location.at[index, "count"] = row["count"]
    
        # Compute the average count for each gate
        count_by_location["avg_count"] = count_by_location["count"].div(number_of_days).round(2)

        # Create the columns for x, y, and location values
        x_values = [x[0]*scale_factor for x in self.locations['coordinates']]
        y_values = [(200-x[1])*scale_factor for x in self.locations['coordinates']]
        location_type = [location[:-1] for location in self.locations["location"]]

        # Construct the dataframe
        df_plot = pd.DataFrame({"x": x_values, "y": y_values, "location_type": location_type, "size": count_by_location["avg_count"]})
        
        # Make the scatter to be overlayed on the image
        fig = px.scatter(df_plot, x='x', y='y', size='size', color="location_type", color_discrete_map=self.colours) 


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
                source=self.image)
        )

        # Configure other layout
        fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            clickmode="event"
        )

        fig.update_traces(hoverinfo="none", hovertemplate=None)

        return fig