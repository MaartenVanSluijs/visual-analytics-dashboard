import pandas as pd

def get_data():
    return pd.read_csv("data\MC1\SensorDataProcessed.csv")

def filter_data(data: pd.DataFrame, varlist):
    variables = ["car_type", "year-month"]

    for index, value in enumerate(varlist):
        if value is not None:
            variable = variables[index]
        
            if variable == "car_type":
                data = data.loc[data["car-type"] == value]
            elif variable == "year-month":
                months = {1: "2015-05", 2: "2015-06", 3: "2015-07", 4: "2015-08", 5: "2015-09", 6: "2015-10", 7: "2015-11", 8: "2015-12", 9: "2016-01", 10: "2016-02", 11: "2016-03", 12: "2016-04", 13: "2016-05"}
                data = data.loc[(pd.to_datetime(data[variable]).dt.date >= pd.Timestamp(months[value[0]]).date()) & 
                                (pd.to_datetime(data[variable]).dt.date <= pd.Timestamp(months[value[1]]).date())]
            
    return data