from src.main import app
from dash import html, ctx
from dash.dependencies import Input, Output
from src.plots.MC1 import MC1


if __name__ == '__main__':
    mc1 = MC1("mc1")

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

    app.run_server(debug=True, dev_tools_ui=True)