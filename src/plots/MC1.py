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
                html.Abbr("\u003F", title="After performing association rule mining on the data, two main routes where revealed in the data.\n\n route 1: Entrance 1 - General gate 7 - General gate 4 - General gate 1* - General gate 5\n\n route 2: Entrance 2 - General gate 1* - Entrance 3\n\n * (General gate 1 - Ranger stop 2 - Ranger stop 0 - General gate 2) are viewed as one place in the analysis due to going through one means going through all of them "),
                dcc.Graph(id=self.html_id, clear_on_unhover=True)
            ],
        )
        
        # Load the image of the map
        self.image = Image.open("data\MC1\Lekagul Roadways.bmp")

        # Get data and add a day column for identifying the amount of days in the df
        self.df = get_data()
        self.df["day"] = pd.to_datetime(self.df["Timestamp"]).dt.date

        # read in the locations parquet
        self.locations = pd.read_parquet("data\MC1\locations.parquet").sort_values(by="location")

        # Create a dictionary for paths between locations
        self.paths = self.read_pickle_paths("data/MC1/extended_shortest_paths.pickle")

    def read_pickle_paths(self, path):
        '''
        Read in the pickle file with the paths between locations

        path: path to the pickle file
        '''
        with open(path, 'rb') as handle:
            extended_shortest_paths = pickle.load(handle)
        return extended_shortest_paths
    
    def change_colors_heatmap(self, plotly_color, opacity=1.0):
        """
        function to change the colors of a heatmap to make all zeros transparent

        Parameters:
        ----------
        plotly_color: list of colors in plotly format
        opacity: opacity of the colors not 0

        Returns:
        -------
        chgd_plotly_color: list of colors in plotly format with changed opacities
        """
        # set empty list
        chgd_plotly_color=[]

        # loop over colors in list and change opacities
        for index, color in enumerate(plotly_color):
                color_string = color.replace('rgb', 'rgba')

                # change opacity of first color to 0
                if index == 0:
                    color_string = color_string.replace(')',f', {str(0)})')

                # change opacity of other colors to opacity
                else:
                    color_string = color_string.replace(')',f', {str(opacity)})')
                chgd_plotly_color.append(color_string)
        return chgd_plotly_color
    
    def get_path_df(self, chosen_locations, scale_factor)->pd.DataFrame:
        '''
        Get a dataframe with the pixel locations of the path between two locations for the heatmap

        Parameters:
        ----------
        chosen_locations: list of two locations (str)
        scale_factor: scale factor of the heatmap (int)

        Returns:
        -------
        df_path: dataframe with the path between the two locations
        '''
        # Get the coordinates of the two locations
        point1 = self.locations.loc[self.locations["location"] == chosen_locations[0]]["coordinates"].to_list()[0]
        point2 = self.locations.loc[self.locations["location"] == chosen_locations[1]]["coordinates"].to_list()[0]

        # Get the path between the two locations
        path_coordinates = self.paths[(point1[0], point1[1])][point2[0], point2[1]]

        # create a 200 - 200 scaled matrix with all zeros
        df_path = pd.DataFrame(np.zeros((200*scale_factor, 200*scale_factor)))
        line_width = 2
        last_coordinate = None
        for coordinate in path_coordinates:
            x, y = coordinate
            y = 200 - y  # flip y-coordinate to match df_path
            if last_coordinate is not None:
                last_x, last_y = last_coordinate
                last_y = 200 - last_y  # flip y-coordinate to match df_path
                if y == last_y:
                    # draw a horizontal line
                    start, end = min(x, last_x), max(x, last_x)
                    for i in range(start, end + 1):
                        df_path.loc[y*scale_factor - line_width:y*scale_factor + line_width + 1,
                                    i*scale_factor - line_width:i*scale_factor + line_width + 1] = 1
                elif x == last_x:
                    # draw a vertical line
                    start, end = min(y, last_y), max(y, last_y)
                    for i in range(start, end + 1):
                        df_path.loc[i*scale_factor - line_width:i*scale_factor + line_width + 1,
                                    x*scale_factor - line_width:x*scale_factor + line_width + 1] = 1
            last_coordinate = coordinate
        return df_path

    def update(self, car_type, month, car_path)->go.Figure:
        # get width and height of image PIL
        img_width, img_height = self.image.size
        scale_factor = 4

        # Filter the data on car_type and month
        filtered_df = filter_data(self.df, [car_type, month, [None, None]])
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
        
        # If a car_path is given make a heatmap of the path
        if car_path[1] is not None:
            df_paths = self.get_path_df(car_path, scale_factor)
            heatmap = go.Heatmap(z=df_paths, colorscale=self.change_colors_heatmap(px.colors.sequential.Bluered, opacity=0.95), showscale=False)
        # if no car_path is given make an invisible heatmap
        else:
            heatmap = go.Heatmap(z=self.locations, colorscale=self.change_colors_heatmap(px.colors.sequential.Bluered, opacity=0.95), showscale=False, visible=False)

        location_types = df_plot["location_type"].unique()
        colors = ['orange', 'green', 'red', 'blue', 'purple', 'yellow']

        # Make the scatter to be overlayed on the image
        scatters = []
        # min_size = 5
        small_list = ['4', '5', '6']
        if car_type == '0':
            max_size = 35
        elif car_type == '1':
            max_size = 30
        elif car_type in small_list:
            max_size = 13
        else:
            max_size = 20
        legend_size = 10
        sizeref = df_plot["size"].max() / max_size ** 2

        # rescale df_plot['size'] so the highest value is increased to 60 and the rest of the values are scaled accordingly
        df_plot['size'] = df_plot['size'].apply(lambda x: x * (max_size / df_plot['size'].max()))

        # Loop through all the location types and make a scatter for each
        for location_type, color in zip(location_types, colors):
            df_plot_filtered = df_plot[df_plot["location_type"] == location_type]
            scatter = go.Scatter(x=df_plot_filtered["x"], y=df_plot_filtered["y"], mode="markers", 
                                 marker=dict(size=df_plot_filtered["size"], sizeref=sizeref, sizemode='area', 
                                                     color=color, opacity=0.8), name=location_type)
            
            scatters.append(scatter)

        # Make the figure 
        fig = go.Figure(data=[heatmap, *scatters])
        
        # place legend at top right
        fig.update_layout(legend= {'itemsizing': 'constant', 'title': {'text': 'Average count per day'}, 
                                   'yanchor': 'top', 'y': 0.99, 'xanchor': 'right', 'x': 0.99, 'font': {'size': legend_size}})

        # Make the figure invisible
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

        # Make the hovertemplate invisible
        fig.update_traces(hoverinfo="none", hovertemplate=None)

        return fig