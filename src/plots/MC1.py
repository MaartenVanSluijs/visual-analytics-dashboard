from dash import dcc, html
import plotly.express as px
import json
import numpy as np
import plotly.graph_objects as go
from matplotlib import image, pyplot
import  PIL.Image as Image
from data.MC1.data import get_data, filter_data
import pandas as pd
import pickle

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

        self.paths = self.read_pickle_paths("data/MC1/extended_shortest_paths.pickle")

        self.fig = go.Figure()

    def read_pickle_paths(self, path):
        with open(path, 'rb') as handle:
            extended_shortest_paths = pickle.load(handle)
        return extended_shortest_paths
    
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
    
    def get_path_df(self, chosen_locations, scale_factor):
        # create a 200 - 200 matrix with all zeros
        point1 = self.locations.loc[self.locations["location"] == chosen_locations[0]]["coordinates"].to_list()[0]
        point2 = self.locations.loc[self.locations["location"] == chosen_locations[1]]["coordinates"].to_list()[0]

        path_coordinates = self.paths[(point1[0], point1[1])][point2[0], point2[1]]
        df_path = pd.DataFrame(np.zeros((200*scale_factor, 200*scale_factor)))
        line_width = 2
        value = scale_factor
        last_coordinate = None
        for coordinate in path_coordinates:
            y = 200-coordinate[1]
            x = coordinate[0]
            if last_coordinate != None:
                last_y = 200-last_coordinate[1]
                last_x = last_coordinate[0]
                if y == last_y:
                    if x > last_x:
                        for i in range(1, scale_factor+1):
                            df_path.loc[y*value-2, x*value-i] = 1
                            df_path.loc[y*value-1, x*value-i] = 1
                            df_path.loc[y*value, x*value-i] = 1
                            df_path.loc[y*value+1, x*value-i] = 1        
                            df_path.loc[y*value+2, x*value-i] = 1            
    
                    else:
                        for i in range(1, scale_factor+1):    
                            df_path.loc[y*value-2, x*value+i] = 1
                            df_path.loc[y*value-1, x*value+i] = 1
                            df_path.loc[y*value, x*value+i] = 1
                            df_path.loc[y*value+1, x*value+i] = 1        
                            df_path.loc[y*value+2, x*value+i] = 1     

                elif x == last_x:
                    if y > last_y:
                        for i in range(1, scale_factor+1):    
                            df_path.loc[y*value-i, x*value-2] = 1     
                            df_path.loc[y*value-i, x*value-1] = 1
                            df_path.loc[y*value-i, x*value] = 1
                            df_path.loc[y*value-i, x*value+1] = 1 
                            df_path.loc[y*value-i, x*value+2] = 1           
                    else:
                        for i in range(1, scale_factor+1):    
                            df_path.loc[y*value+i, x*value-2] = 1     
                            df_path.loc[y*value+i, x*value-1] = 1
                            df_path.loc[y*value+i, x*value] = 1
                            df_path.loc[y*value+i, x*value+1] = 1 
                            df_path.loc[y*value+i, x*value+2] = 1
            last_coordinate = coordinate
        return df_path

    def update(self, car_type, month, car_path)->go.Figure:
        # get width and height of image PIL
        img_width, img_height = self.image.size
        scale_factor = 4

        # Filter the data on car_type and month
        filtered_df = filter_data(self.df, [car_type, month, car_path])
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
        location_type = [location.replace('ranger-bas', 'ranger-base') for location in location_type]

        # Construct the dataframe
        df_plot = pd.DataFrame({"x": x_values, "y": y_values, "location_type": location_type, "size": count_by_location["avg_count"]})
        
        # If a car_path is given
        if car_path[1] is not None:
            df_paths = self.get_path_df(car_path, scale_factor)
            heatmap = go.Heatmap(z=df_paths, colorscale=self.change_colors_heatmap(px.colors.sequential.Bluered, opacity=0.95), showscale=False)
        else:
            heatmap = go.Heatmap(z=self.locations, colorscale=self.change_colors_heatmap(px.colors.sequential.Bluered, opacity=0.95), showscale=False, visible=False)

        location_types = df_plot["location_type"].unique()
        colors = ['orange', 'green', 'red', 'blue', 'purple', 'yellow']

        # Make the scatter to be overlayed on the image
        scatters = []
        min_size = 5
        legend_size = 10
        for location_type, color in zip(location_types, colors):
            df_plot_filtered = df_plot[df_plot["location_type"] == location_type]
            scatter = go.Scatter(x=df_plot_filtered["x"], y=df_plot_filtered["y"], mode="markers", 
                                 marker=dict(size=df_plot_filtered["size"].apply(lambda x: x if x >= min_size else min_size), 
                                                     color=color, opacity=0.8), name=location_type)
            scatters.append(scatter)

        

        data = [heatmap, *scatters]
        fig = go.Figure(data=data)
        
        # place legend at top right
        fig.update_layout(legend= {'itemsizing': 'constant', 'title': {'text': 'Average count per day'}, 'yanchor': 'top', 'y': 0.99, 'xanchor': 'right', 'x': 0.99, 'font': {'size': legend_size}})

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