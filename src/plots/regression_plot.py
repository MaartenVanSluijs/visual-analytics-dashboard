from data.MC1.data import get_regression_data

import pandas as pd
from dash import dcc, html
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go

class Regression_plot(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")
    
        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(id=self.html_id)
            ],
        )

        self.df = pd.read_csv("data//MC1//regression_data.csv")

    def update(self, car_type, month, car_path):
        filtered_df = get_regression_data(car_type, month, car_path)

        if filtered_df.empty:
            print("This dataframe is empty")
            filtered_df = get_regression_data(car_type, month, [None, None])

        test_data = self.run_regression(filtered_df).sort_values(by="day")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=test_data["day"], y=test_data["predicted_value"],
                            mode='lines',
                            name='Predicted number of cars'))
        fig.add_trace(go.Scatter(x=test_data["day"], y=test_data["current_day"],
                            mode='lines',
                            name='Actual number of cars'))
        
        fig.update_layout(title="Predicted and actual amount of cars",
                          autosize=False,
                          width= 1200,
                          hovermode="x unified"
                          )

        return fig
    
    def run_regression(self, df) -> pd.DataFrame:
        df_train, df_test = train_test_split(df, test_size=0.8, random_state=69)

        X_train = df_train[["day-1", "day-2", "day-3", "day-4", "day-5", "day-6", "day-7", "is_weekend", "month"]]
        y_train = df_train["current_day"]

        X_test = df_test[["day-1", "day-2", "day-3", "day-4", "day-5", "day-6", "day-7", "is_weekend", "month"]]

        regressor = DecisionTreeRegressor(random_state=0)
        regressor.fit(X_train, y_train)

        y_predicted = regressor.predict(X_test) 

        df_test["predicted_value"] = y_predicted

        return df_test
