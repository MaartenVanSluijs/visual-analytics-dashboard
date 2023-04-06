import pandas as pd
from typing import List

# Define a dictionary to map month numbers to year-month strings
months = {1: "2015-05", 2: "2015-06", 3: "2015-07", 4: "2015-08", 5: "2015-09", 6: "2015-10",
          7: "2015-11", 8: "2015-12", 9: "2016-01", 10: "2016-02", 11: "2016-03", 12: "2016-04",
          13: "2016-05", 14: "2016-06"}

# Load the 'locations' and 'df_speed' dataframes from parquet and CSV files respectively
locations = pd.read_parquet("data\MC1\locations.parquet")
df_speed = pd.read_csv("data\MC1\speed.csv")

def get_data():
    '''
    Helper function to load data from 'SensorDataProcessed.csv' file

    Returns:
    --------
    data : pd.DataFrame
        A pandas dataframe containing the loaded data
    '''
    return pd.read_csv("data\MC1\SensorDataProcessed.csv")

def filter_data(data: pd.DataFrame, varlist):
    '''
    Filters the input dataframe 'data' based on the specified variables in 'varlist'

    Parameters:
    -----------
    data : pd.DataFrame
        A pandas dataframe containing the data to be filtered
    varlist : list of variables to filter on
        A list of 3 items, containing the values to filter on for the variables 'car_type',
        'year-month', and 'carpath', respectively. If a variable is None, it will not be filtered.

    Returns:
    --------
    data : pd.DataFrame
        A pandas dataframe containing the filtered data
    '''
    variables = ["car_type", "year-month", "carpath"]

    for index, value in enumerate(varlist):
        if value is not None:
            variable = variables[index]
        
            if variable == "car_type":
                if value != "0":
                    data = data.loc[data["car-type"] == value]
            elif variable == "year-month":
                # Filter based on the start and end months
                data = data.loc[(pd.to_datetime(data[variable]).dt.date >= pd.Timestamp(months[value[0]]).date()) & 
                                (pd.to_datetime(data[variable]).dt.date <= pd.Timestamp(months[value[1]]).date())]
            elif variable == "carpath":
                if value[1] is not None:
                    # Get the car IDs that traveled between the selected locations
                    car_ids = get_car_id_path(value)
                    data = data.loc[data["car-id"].isin(car_ids)]
    return data

def get_car_id_path(selected_locations):
    """
    get the car ids that traveled between the selected locations

    Parameters:
    -----------
    selected_locations : list of locations
        A list of 2 items containing strings of the selected locations
    
    Returns:
    --------
    car_ids_path : list of car ids
        A list of car ids that traveled between the selected locations
    """ 
    # Get the coordinates of the selected locations
    coordinates = []
    for i in selected_locations:
        coordinates.append(locations.loc[locations['location'] == i, 'coordinates'].values[0])

    # Filter out the speed data based on the selected locations
    speed_filtered = df_speed.loc[((df_speed["start-x"] == coordinates[0][0]) & (df_speed["start-y"] == coordinates[0][1]) &
                                       (df_speed["end-x"] == coordinates[1][0]) & (df_speed["end-y"] == coordinates[1][1])) |
                                      ((df_speed["end-x"] == coordinates[0][0]) & (df_speed["end-y"] == coordinates[0][1]) &
                                       (df_speed["start-x"] == coordinates[1][0]) & (df_speed["start-y"] == coordinates[1][1]))]
    
    car_ids_path = speed_filtered['car-id'].unique()
    return car_ids_path

def get_regression_data(car_type, month, car_path):
    """
    This function returns the data for the regression model

    Parameters:
    -----------
    car_type (str): The car type to filter on
    month (list): The start and end month to filter on
    car_path (list): The start and end location to filter on

    Returns:
    --------
    grouped_data (pd.DataFrame): The data for the regression model
    """
    # Read in data
    data = pd.read_csv("data\MC1\SensorDataProcessed.csv")
    # Add date column
    data["day"] = pd.to_datetime(data["Timestamp"]).dt.date

    # Filter out only the desired car type
    if car_type != "0":
        data = data.loc[data["car-type"] == car_type]

    if car_path != None:
        if car_path[1] is not None and car_path[0] is not None:
            car_ids = get_car_id_path(car_path)
            data = data.loc[(data["car-id"].isin(car_ids)) & (data["gate-name"] == car_path[0])]

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