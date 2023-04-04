from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Speed(html.Div):
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

        filtered_df = self.df

        # Filter dataset on specific months 
        filtered_df = filtered_df.loc[(filtered_df["start-time"].dt.month >= months[0]) & (filtered_df["start-time"].dt.month <= months[1])]

        # Filter dataset on specific path
        if car_path[1] is not None:
            point_1 = self.locations.loc[self.locations["location"] == car_path[0]]["coordinates"].to_list()[0]
            point_2 = self.locations.loc[self.locations["location"] == car_path[1]]["coordinates"].to_list()[0]
            
            filtered_df = filtered_df.loc[((filtered_df["start-x"] == point_1[0]) & (filtered_df["start-y"] == point_1[1]) &
                                        (filtered_df["end-x"] == point_2[0]) & (filtered_df["end-y"] == point_2[1])) |
                                        ((filtered_df["end-x"] == point_1[0]) & (filtered_df["end-y"] == point_1[1]) &
                                        (filtered_df["start-x"] == point_2[0]) & (filtered_df["start-y"] == point_2[1]))]

        # Filter dataset on specific cars
        if car_type != "0": 
            extra_df = filtered_df.loc[self.df["car-type"] == car_type]

            # Create a pivot table to get all averages per hour
            pivot_table_cars_extra = extra_df.pivot_table(index=extra_df["start-time"].dt.hour, columns=extra_df["car-id"], values="average-speed")

            average_speed_extra = pivot_table_cars_extra.mean(axis=1)

            df_average_speed_extra = pd.DataFrame({'hour': average_speed_extra.index, 'speed': average_speed_extra.values})

        # Create a pivot table to get all averages per hour
        pivot_table_cars = filtered_df.pivot_table(index=filtered_df["start-time"].dt.hour, columns=filtered_df["car-id"], values="average-speed")

        average_speed = pivot_table_cars.mean(axis=1)
        
        df_average_speed = pd.DataFrame({'hour': average_speed.index, 'speed': average_speed.values})

        self.fig = px.line(df_average_speed, x='hour', y='speed', markers=True)
        if car_type != "0":
            self.fig.add_trace(go.Scatter(x=df_average_speed_extra['hour'], y=df_average_speed_extra['speed'], mode="lines+markers", name="Car type"))
        self.fig.update_layout(
                title="Average speed during the day",
                xaxis_title="Hours in the day",
                yaxis_title="Average speed",
                yaxis_range=[20, 40],
                hovermode="x unified"
            )

        return self.fig