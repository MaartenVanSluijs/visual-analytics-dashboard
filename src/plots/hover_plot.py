from data.MC1.data import get_data, filter_data

from dash import dcc, html
import plotly.express as px
import pandas as pd

class Hover_plot(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

        self.df = get_data()
        self.locations = pd.read_parquet("data\MC1\locations.parquet").sort_values(by="location")

    def get_plot(self, point, month, car_type):
        # Find which gate is being hovered on
        gate = ""
        for index, value in self.locations.iterrows():
            if value["coordinates"][0] * 4 == point[0] and (200 - value["coordinates"][1]) * 4 == point[1]:
                gate = value["location"]
        

        # Filter on gate
        filtered_df = self.df.loc[self.df["gate-name"] == gate]

        # Filter on month
        filtered_df = filter_data(filtered_df, [None, month])

        grouped_data = filtered_df.groupby("car-type", as_index=False).count()

        data_per_type = grouped_data.rename(columns={"Timestamp": "count"})
        
        total_count = data_per_type["count"].sum()

        data_per_type["percentage"] = round((data_per_type["count"] / total_count) * 100, 2)

        if car_type != '0':
            data_one_car = data_per_type.loc[data_per_type["car-type"] == car_type]
            if data_one_car.empty:
                total_count = 0
            else:
                total_count = data_one_car["count"].values[0]

        data_per_type.replace({"car-type": {"1": "Two-axle car", 
                                            "2": "Two-axle truck",
                                            "2P": "Two-axle truck (Park service)",
                                            "3": "Three-axle truck",
                                            "4": "Four-axle (and above) truck",
                                            "5": "Two-axle bus",
                                            "6": "Three-axle bus"}}, inplace=True)
        # print(data_per_type)

        fig = px.bar(data_per_type, x="car-type", y="percentage", hover_data=["percentage", "count"], 
                     width=400, height=400, title="Gate: " + gate + "| Total count:" + str(total_count))

        return fig