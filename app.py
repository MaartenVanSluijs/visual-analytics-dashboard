from src.main import app
from dash import html, ctx, dcc
from dash.dependencies import Input, Output
from src.plots.MC1 import MC1

if __name__ == '__main__':
    mc1 = MC1("mc1")
    year_months = mc1.year_months

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="MC1",
                className="nine columns",
                children=[
                    mc1
                ]
            )
        ],
    )

    @app.callback(
        Output(mc1.html_id, "figure"),[
            Input(mc1.html_id, "clickData"),
        ]
    )

    def update_test(click_data):
        return mc1.update()

    app.run_server(debug=True, dev_tools_ui=True)