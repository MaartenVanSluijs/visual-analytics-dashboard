from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

class SpeedBar(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, car_type, month, car_path):
        self.fig = go.Figure()
        # print(car_path)

        # # Filter dataset on specific path
        # df = self.df
        # df_filtered = df.loc[(df["start-x"] == start_node[0]) & (df["start-y"] == start_node[1]) & (df["end-x"] == end_node[0]) & (df["end-y"] == end_node[1])]

        # # Now we have a dataset that shows the average speed per car type for a specific road 

        # # TODO: for each hour, we want the averages of all speeds 
        
        # avg_speeds = self.df.groupby('car-type')['average-speed'].mean().reset_index()
        # print(avg_speeds)
        # self.fig.add_trace(go.Bar(x=avg_speeds['car-type'], y=avg_speeds['average-speed']))

        return self.fig