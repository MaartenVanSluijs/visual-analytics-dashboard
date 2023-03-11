import pandas as pd

df = pd.read_csv("C:/Users/20182667/Documents/Studie/Vakken/Master/Visual Analytics/visual-analytics-dashboard/data/MC1/SensorData.csv")

def get_car_paths(df):
    car_paths = {}

    for index, row in df.iterrows():
        car_id = row["car-id"]
        location = row["gate-name"]
        
        if car_id in car_paths:
            car_paths[car_id].append(location)
        else:
            car_paths[car_id] = [location]

    return car_paths

def one_hot_encode(car_path, df):
    gate_names = df["gate-name"].unique().tolist()
    encoding = [0] * len(gate_names)

    for gate in car_path:
        gate_index = gate_names.index(gate)

        encoding[gate_index] = 1

    return encoding

def aggregate_encodings(car_paths, df):
    encodings = {}

    for key, item in car_paths.items():
        encodings[key] = one_hot_encode(item, df)
    
    return encodings


car_paths = get_car_paths(df)