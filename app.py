from src.main import app
from dash import html, ctx, dcc
from dash.dependencies import Input, Output
from src.plots.MC3 import MC3

if __name__ == '__main__':
    mc3 = MC3("mc3")


    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            html.Div(
                id="MC3",
                className="nine columns",
                children=[
                    mc3,
                    dcc.Dropdown(
                        id="mc3_image_type",
                        options=[
                            {"label": "RGB", "value": "RGB"},
                            {"label": "Plant Health", "value": "plant_health"},
                            {"label": "Floods or Fires", "value": "floods_or_burned"},
                            {"label": "Snow, Ice, Clouds", "value": "snow_ice_clouds"},
                            {"label": "Normalized Difference Vegetation Index", "value": "NDVI"}
                        ],
                        value="RGB"
                    ),
                    dcc.Slider(
                        1,12,1,
                        value=1,
                        id= "mc3_image_slider"
                    )
                ]
            )
        ],
    )

    @app.callback(
        Output(mc3.html_id, "figure"),[
            Input(mc3.html_id, "clickData"),
            Input("mc3_image_type", "value"),
            Input("mc3_image_slider", "value")
        ]
    )
    def update_test(click_data, image_type, image_number):
        return mc3.update(image_type, image_number, ctx.triggered_id)

    app.run_server(debug=True, dev_tools_ui=True)