from data.MC1.data import get_data, filter_data
from dash import dcc, html

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

    def run_prediction():
        return

    def update(self):
        return