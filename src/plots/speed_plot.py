from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Speed(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
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

    def update(self, car_type, months):
        self.fig = go.Figure()

        filtered_df = self.df

        # Filter dataset on specific months 
        filtered_df = filtered_df.loc[(filtered_df["start-time"].dt.month >= months[0]) & (filtered_df["start-time"].dt.month <= months[1])]

        # Filter dataset on specific path
        # TODOs

        # Filter dataset on specific cars
        if car_type != "0": 
            extra_df = filtered_df.loc[self.df["car-type"] == car_type]

            # Create a pivot table to get all averages per hour
            pivot_table_cars_extra = extra_df.pivot_table(index=extra_df["start-time"].dt.hour, columns=extra_df["car-id"], values="average-speed")

            average_speed_extra = pivot_table_cars_extra.mean(axis=1)

        # Create a pivot table to get all averages per hour
        pivot_table_cars = filtered_df.pivot_table(index=filtered_df["start-time"].dt.hour, columns=filtered_df["car-id"], values="average-speed")

        average_speed = pivot_table_cars.mean(axis=1)

        self.fig = px.line(average_speed, average_speed.index, y=average_speed.values, markers=True)
        if car_type != "0":
            self.fig.add_trace(go.Scatter(x=average_speed_extra.index, y=average_speed_extra.values, mode="lines+markers", name="Selected car type"))

        self.fig.update_layout(
                xaxis_title="Hours in the day",
                yaxis_title="Average speed",
                yaxis_range=[0, 50]
            )

        return self.fig