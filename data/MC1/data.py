import pandas as pd

months = {1: "2015-05", 2: "2015-06", 3: "2015-07", 4: "2015-08", 5: "2015-09", 6: "2015-10", 7: "2015-11", 8: "2015-12", 9: "2016-01", 10: "2016-02", 11: "2016-03", 12: "2016-04", 13: "2016-05", 14: "2016-06"}

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
                data = data.loc[(pd.to_datetime(data[variable]).dt.date >= pd.Timestamp(months[value[0]]).date()) & 
                                (pd.to_datetime(data[variable]).dt.date <= pd.Timestamp(months[value[1]]).date())]
            
    return data

def get_regression_data(car_type, month):
    # Read in data
    data = pd.read_csv("data\MC1\SensorDataProcessed.csv")
    # Add date column
    data["day"] = pd.to_datetime(data["Timestamp"]).dt.date

    # Filter out only the desired car type
    if car_type != "0":
        data = data.loc[data["car-type"] == car_type]

    # Group based on this date
    grouped_data = data.groupby("day", as_index=False).count().rename(columns={"Timestamp": "current_day"}).drop(["car-id", "car-type", "gate-name", "year-month", "x", "y"], axis=1)
    
    # Add history columns
    for day in range(1,8):
        grouped_data["day-"+str(day)] = grouped_data["current_day"].shift(day)

    # Filter out only the selected date range
    grouped_data = grouped_data.loc[(pd.to_datetime(grouped_data["day"]).dt.date >= pd.Timestamp(months[month[0]]).date()) & 
                                    (pd.to_datetime(grouped_data["day"]).dt.date < pd.Timestamp(months[month[1] + 1]).date())]

    # Add weekend/weekday column
    grouped_data["is_weekend"] = pd.to_datetime(grouped_data["day"]).dt.weekday > 4

    # Add month column
    grouped_data["month"] = pd.to_datetime(grouped_data["day"]).dt.month

    # Filter out first 7 rows
    if month[0] == 1:
        grouped_data = grouped_data.iloc[7:,:]

    # Store in CSV
    # grouped_data.to_csv("data//MC1//regression_data.csv", index=False)
    
    return grouped_data

# get_regression_data()