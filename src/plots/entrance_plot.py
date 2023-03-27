from dash import dcc, html
from data.MC1.data import get_data, filter_data
import plotly.express as px

class Entrance_plot(html.Div):
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

    def update(self, car_type, month, triggered_id):

        filtered_df = filter_data(self.df, [car_type, month])

        grouped_data = filtered_df.groupby("gate-name", as_index=False).count()

        data_per_entrance = grouped_data[grouped_data["gate-name"].str.contains("entrance")][["gate-name", "Timestamp"]]
        data_per_entrance = data_per_entrance.rename(columns={"Timestamp": "count"})
        
        total_count = data_per_entrance["count"].sum()

        data_per_entrance["percentage"] = round((data_per_entrance["count"] / total_count) * 100, 2)

        fig = px.bar(data_per_entrance, x="gate-name", y="percentage", hover_data=["percentage", "count"], width=400, height= 300)

        return fig