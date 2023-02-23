from src.main import app
from dash import html, ctx
from dash.dependencies import Input, Output
from src.plots.MC3 import MC3

if __name__ == '__main__':
    test = MC3("test")


    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="test",
                className="nine columns",
                children=[
                    test
                ]
            )
        ],
    )

    @app.callback(
        Output(test.html_id, "figure"),[
            Input(test.html_id, "clickData")
        ]
    )
    def update_test(click_data):
        return test.update()

    app.run_server(debug=True, dev_tools_ui=True)