from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Cars(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.locations = pd.read_parquet("data\MC1\locations.parquet")
        # make sure the timestamps are in datetime format
        self.df['start-time'] = pd.to_datetime(self.df["start-time"])
        self.df['end-time'] = pd.to_datetime(self.df["end-time"])

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, car_type, months, car_path):
        self.fig = go.Figure()

        # Filter dataset on specific cars
        filtered_df = self.df

        if car_type != "0": 
            filtered_df = self.df.loc[self.df["car-type"] == car_type]

        # Filter dataset on specific months 
        print(months[0], months[1])

        filtered_df = filtered_df.loc[(filtered_df["start-time"].dt.month >= months[0]) & (filtered_df["start-time"].dt.month <= months[1])]
        print(filtered_df.head(10))

        # Filter dataset on specific path
        if car_path[1] is not None:
            point_1 = self.locations.loc[self.locations["location"] == car_path[0]]["coordinates"].to_list()[0]
            point_2 = self.locations.loc[self.locations["location"] == car_path[1]]["coordinates"].to_list()[0]
            
            filtered_df = filtered_df.loc[((filtered_df["start-x"] == point_1[0]) & (filtered_df["start-y"] == point_1[1]) &
                                        (filtered_df["end-x"] == point_2[0]) & (filtered_df["end-y"] == point_2[1])) |
                                        ((filtered_df["end-x"] == point_1[0]) & (filtered_df["end-y"] == point_1[1]) &
                                        (filtered_df["start-x"] == point_2[0]) & (filtered_df["start-y"] == point_2[1]))]

        # Create a pivot table to get all averages per hour
        # extract the hour from the start-time column
        filtered_df["hour"] = pd.to_datetime(filtered_df["start-time"]).dt.hour

        # group the data by hour and day, and count the number of unique car IDs
        grouped = filtered_df.groupby([pd.Grouper(key="start-time", freq="D"), "hour"])["car-id"].nunique()
        print(grouped)

        # create a pivot table from the grouped data
        pivot_table = pd.pivot_table(grouped.reset_index(), index="hour", columns="start-time", values="car-id", aggfunc="mean")

        # calculate the average number of cars per hour over all days
        average_cars = pivot_table.mean(axis=1)

        print(average_cars)
        self.fig = px.line(average_cars, average_cars.index, y=average_cars.values, markers=True)
        self.fig.update_layout(
                xaxis_title="Hours in the day",
                yaxis_title="Average amount of cars",
                hovermode="x unified"
                # yaxis_range=[0, 50]
            )

        return self.fig