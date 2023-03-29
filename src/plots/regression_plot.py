from data.MC1.data import get_regression_data

import pandas as pd
from dash import dcc, html
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import plotly_express as px

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

    def update(self):
        test_data = self.run_regression(self.df).sort_values(by="day")

        fig = px.line(test_data, x="day", y="predicted_value", title='Predicted amount of cars in the park per day')

        return fig
    
    def run_regression(self, df) -> pd.DataFrame:
        X_values = pd.DataFrame(df[["day", "day-1", "day-2", "day-3", "day-4", "day-5", "day-6", "day-7", "is_weekend", "month"]])
        y_values = pd.DataFrame(df["current_day"])

        df_train, df_test = train_test_split(df, test_size=0.8, random_state=69)

        X_train = df_train[["day-1", "day-2", "day-3", "day-4", "day-5", "day-6", "day-7", "is_weekend", "month"]]
        y_train = df_train["current_day"]

        X_test = df_test[["day-1", "day-2", "day-3", "day-4", "day-5", "day-6", "day-7", "is_weekend", "month"]]

        regressor = DecisionTreeRegressor(random_state=0)
        regressor.fit(X_train, y_train)

        y_predicted = regressor.predict(X_test) 

        df_test["predicted_value"] = y_predicted

        return df_test
