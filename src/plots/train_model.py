import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

class model_trainer():
    def __init__(self, name):
        self.car_type = "2P"

        self.df = pd.read_csv("data\MC1\SensorDataProcessed.csv")

    def run_prediction(self):
        # read df from csv
        df_x = pd.read_csv("data\MC1\one_hot_encoding.csv")
        y_values = self.get_y_values(self.car_type)
        x_train, x_test, y_train, y_test = train_test_split(df_x, y_values, test_size=0.20, random_state=69)

        logistic_model = LogisticRegression(random_state=0).fit(x_train, y_train)
        # return the coefficients of the model
        return logistic_model.coef_[0]
    
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

        return encoded_cars.sort_values(by="Timestamp")['car-type']

trainer = model_trainer('test')
print(len(trainer.run_prediction()))