from src.main import app
from dash import html, ctx, dcc
from dash.dependencies import Input, Output
from src.plots.MC2 import MC2

if __name__ == '__main__':
    mc2 = MC2("mc2")

    chemicals = mc2.get_chemicals()

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="MC2",
                className="nine columns",
                children=[
                    mc2,
                    dcc.Dropdown(
                        id="mc2_chemical",
                        options=[
                            {"label": chemicals[0], "value": chemicals[0]},
                            {"label": chemicals[1], "value": chemicals[1]},
                            {"label": chemicals[2], "value": chemicals[2]},
                            {"label": chemicals[3], "value": chemicals[3]},
                        ],
                        value=[chemicals[0]],
                        multi=True
                    ),
                    dcc.Dropdown(
                        id="mc2_month",
                        options=[
                            {"label": 'April', "value": 4},
                            {"label": 'August', "value": 8},
                            {"label": 'December', "value": 12},
                        ],
                        value=[4,8,12],
                        multi=True
                    )
                ]
            )
        ],
    )

    @app.callback(
        Output(mc2.html_id, "figure"),[
            Input(mc2.html_id, "clickData"),
            Input("mc2_chemical", "value"),
            Input("mc2_month", "value")
        ]
    )

    def update_test(click_data, chemical, month):
        return mc2.update(chemical, month, ctx.triggered_id)

    app.run_server(debug=True, dev_tools_ui=True)