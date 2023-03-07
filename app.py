from App.main import app
from dash import html, ctx
from dash.dependencies import Input, Output

if __name__ == '__main__':
    # Create the app
    app.layout = html.Div(
        id="app-container",
        children=[
            
        ],
    )

    app.run_server(debug=True, dev_tools_ui=True)