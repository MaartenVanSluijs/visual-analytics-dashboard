import pandas as pd

def get_data():
    return pd.read_csv("C:/Users/20182667/Documents/Studie/Vakken/Master/Visual Analytics/visual-analytics-dashboard/data/MC1/SensorData.csv")

def filter_data(data: pd.DataFrame, varlist):
    variables = ["car_type", "month"]

    for index, value in enumerate(varlist):
        if value is not None:
            variable = variables[index]
        
            if variable == "car_type":
                data = data.loc[data["car-type"] == value]
            elif variable == "month":
                data = data.loc[(data[variable] >= value[0]) & (data[variable] <= value[1])]
            
    return data