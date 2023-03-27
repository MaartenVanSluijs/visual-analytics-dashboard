from data.MC1.data import get_data, filter_data

from dash import dcc, html
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

class Coefficient_plot(html.Div):
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

        self.car_type = "1"

    def run_prediction(self):
        x_values = self.get_x_values()
        y_values = self.get_y_values(self.car_type)
        x_train, x_test, y_train, y_test = train_test_split(x_values, y_values, test_size=0.20, random_state=69)

        logistic_model = LogisticRegression(random_state=0).fit(x_train, y_train)
        return logistic_model._coef

    
    def get_car_paths(self):
        car_paths = {}
    
        for index, row in self.df.iterrows():
            car_id = row["car-id"]
            location = row["gate-name"]
        
            if car_id in car_paths:
                car_paths[car_id].append(location)
            else:
                car_paths[car_id] = [location]
    
        return car_paths
    
    def get_x_values(self):
        gate_names = self.df["gate-name"].unique().tolist()
    
        encodings = np.zeros((self.df["car-id"].nunique(), self.df["gate-name"].nunique()))

        index = 0
        for key, value in self.get_car_paths().items():
            car_path = value
    
            for gate in set(car_path):
                encodings[index][gate_names.index(gate)] = 1
    
            index += 1
    
        return encodings
    
    def get_y_values(self, car_type):
        
        def is_car_type(type):
            return "1" if type == car_type else "0"

        cars = self.df.groupby(by="car-id").first()
        encoded_cars = cars.replace({"car-type": {"1": is_car_type("1"),
                                                  "2": is_car_type("2"),
                                                  "2P": is_car_type("2P"),
                                                  "3": is_car_type("3"),
                                                  "4": is_car_type("4"),
                                                  "5": is_car_type("5"),
                                                  "6": is_car_type("6")}})

        return encoded_cars.sort_values(by="Timestamp")

    def update(self):
        print(self.run_prediction())