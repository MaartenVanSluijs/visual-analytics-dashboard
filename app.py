from src.main import app
from src.menu import generate_header, generate_control_card
from dash import html, ctx
from dash.dependencies import Input, Output
from src.plots.MC1 import MC1
from data.MC1 import data_cleanup


if __name__ == '__main__':
    df_mc1 = data_cleanup.process_data()
    len_shortest_paths, shortest_paths = data_cleanup.shortest_paths()
    mc1 = MC1("mc1", df_mc1)

    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Header(
                id="header",
                className="twelve columns", 
                children=generate_header()
            ), 

            html.Div(
                id="left-column",
                className="three columns",
                children=generate_control_card(df_mc1)
            ),

            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    mc1
                ]
            )
            
        ],
    )

    @app.callback(
        Output(mc1.html_id, "figure"), [
        Input(mc1.html_id, "clickData")
        ]
    )
    def update(click_data):
        return mc1.update()

    app.run_server(debug=True, dev_tools_ui=True)