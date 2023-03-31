import pandas as pd
from dash import dcc, html
import plotly.express as px
from PIL import Image
import networkx as nx
import numpy as np
import matplotlib.image as mpimg

def process_data():
    # Read in the data
    df = pd.read_csv("data\MC1\SensorData.csv")

    # Set the timestamp to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Drop the null values 
    df.dropna

    # Check if there are weird values (typos) in the columns
    # print(df['car-type'].value_counts())
    # print(df["gate-name"].value_counts())
    # There are no weird values in the columns

    # Check if there are gaps in the data
    fig = px.line(df, x="Timestamp")
    # doesn't seem to be any gaps in the data 
    del df["month"]
    df["year-month"] = df["Timestamp"].dt.strftime("%Y-%m")

    # Add columns for coordinates of the locations
    df = add_coordinates(df)

    df.to_csv("data\MC1\SensorDataProcessed.csv", index=False)

    shortest_path, _ = shortest_paths()
    df_speed = calculate_speed(df, shortest_path)  

    return df, df_speed

def add_coordinates(df):
    img = mpimg.imread('data\MC1\Lekagul Roadways.bmp')

    improved_locations = ['general-gate0', 'general-gate1', 'general-gate2', 'general-gate3', 'general-gate4', 'general-gate5', 'general-gate6', 'general-gate7', 'ranger-stop0', 'ranger-stop1', 'ranger-stop2', 'ranger-stop3', 'ranger-stop4', 'ranger-stop5', 'ranger-stop6', 'ranger-stop7', 'entrance0', 'entrance1', 'entrance2', 'entrance3', 'entrance4', 'camping0', 'camping8', 'camping1', 'camping2', 'camping3', 'camping4', 'camping5', 'camping7', 'camping6', 'gate0', 'gate1', 'gate2', 'gate3', 'gate4', 'gate5', 'gate6', 'gate7', 'gate8', 'ranger-base']
    types = {'type':['general-gate', 'ranger-stop', 'entrance', 'camping', 'gate', 'ranger-base'],
         'color':[[0,255,255], [255,216,0], [76,255,0], [255,106,0], [255,0,0], [255,0,220]]}

    width, height = img.shape[:2]
    coordinates = []
    for y in range(height):
        for x in range(width):
            rgb = img[x][y]
            if not rgb[0] == rgb[1] == rgb[2]:
                coordinates.append([x,y,rgb[:3]])

    coordinates.sort()

    names = []
    xy_coordinates = []

    for color in types['color']:
        for coordinate in coordinates:
            if (coordinate[2]== color).all():
                names.append(improved_locations[0])
                improved_locations.pop(0)
                xy_coordinates.append([coordinate[1], coordinate[0]])

    dict_coordinates = dict(zip(names, xy_coordinates))

    for row, data in df.iterrows():
        df.loc[row, 'x'] = dict_coordinates[data['gate-name']][0]
        df.loc[row, 'y'] = dict_coordinates[data['gate-name']][1]

    return df


def shortest_paths(): 
    # Open the image 
    im = Image.open("data\MC1\Lekagul Roadways.bmp").convert("RGBA")

    # Create an empty graph
    graph = nx.Graph()

    # Iterate through each pixel in the image
    for x in range(im.width):
        for y in range(im.height):

            # Get the RGBA values
            rgba = im.getpixel((x, y))
            
            # Add the white and colored pixels as a node
            r = rgba[0]
            g = rgba[1]
            b = rgba[2]
            a = rgba[3]

            # make grey nodes either white or black 
            if (r == g) and (g == b) and (r != 0) and (r != 255):
                # print(r, g, b)
                if r <= 127: 
                    r = 0
                    g = 0
                    b = 0
                else: 
                    r = 255
                    g = 255
                    b = 255

            # if not ((r == 0 or r == 255) and (g == 0 or g == 255) and (b == 0 or b == 255)):
            #     print(r, g, b)


            if not (r == 0 and b == 0 and g == 0):
                graph.add_node((x, y), r=r, g=g, b=b, a=a)

            # Add edges 
            if rgba != (0, 0, 0, 255):
                neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

                for neighbor in neighbors:
                    if 0 <= neighbor[0] < im.width and 0 <= neighbor[1] < im.height:
                        rbga_neighbor = im.getpixel((neighbor[0], neighbor[1]))
                        # if neighbor is not a black pixel
                        if rbga_neighbor != (0, 0, 0, 255):
                            graph.add_edge((x, y), neighbor)

    # Now we have a graph with all white and colored nodes 

    nodes_to_remove = []
    for node, data in graph.nodes(data=True):
        # print(data)
        if not data:
            nodes_to_remove.append(node)
    
    for node in nodes_to_remove:
        graph.remove_node(node)
        
    colored_nodes = [] 
    for node, data in graph.nodes(data=True):
        if not (list(data.items())[0][1] == 255 and list(data.items())[1][1] == 255 and list(data.items())[2][1] == 255):
            colored_nodes.append(node)

    # print(colored_nodes)

    shortest_paths = {}
    extended_shortest_paths = {}
    for source in colored_nodes:
        shortest_paths[source] = {}
        extended_shortest_paths[source] = {}
        for target in colored_nodes:
            if source != target:
                try: 
                    shortest_path = nx.shortest_path(graph, source, target)
                    extended_shortest_paths[source][target] = shortest_path
                    shortest_paths[source][target] = (len(shortest_path) - 1)*0.06

                except nx.exception.NetworkXNoPath:
                    print("no path found")
                    continue

    # print(shortest_paths)
    
    return shortest_paths, extended_shortest_paths

def calculate_speed(df, shortest_path): 
    #set timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    # get all unique car ID's
    car_ids = df["car-id"].unique()

    # create empty dataframe
    df_speed = pd.DataFrame(columns=['start-x', 'start-y', 'end-x', 'end-y', 'start-time', 'end-time', 'car-id', 'car-type', 'average-speed'])

    for car_id in car_ids:
        # Create dataset with only this car
        car_df = df[df['car-id'] == car_id]

        # Create a rolling window of 2
        car_window = car_df.rolling(window=2)

        # print(car_df.head(10))

        for i, window_df in enumerate(car_window):
        # skip the first row since it doesn't have a complete window
            if i == 0:
                continue
            
            begin = int(window_df["x"].iloc[0]), int(window_df["y"].iloc[0])
            end = int(window_df["x"].iloc[1]), int(window_df["y"].iloc[1])

            begin_time = window_df["Timestamp"].iloc[0]
            end_time = window_df["Timestamp"].iloc[1]

            id_car = window_df["car-id"].iloc[0]
            type_car = window_df["car-type"].iloc[0]

            if begin == end:
                continue

            distance = shortest_path[begin][end]
            time_diff = (end_time - begin_time) / pd.Timedelta(hours=1)
            average_speed = distance / time_diff
            # print(begin, end, id_car, type_car, average_speed)

            # print(begin, begin[0], begin[1])

            row = pd.DataFrame({'start-x': begin[0], 'start-y': begin[1], 'end-x': end[0], 'end-y': end[1], 'start-time': begin_time, 
                                'end-time': end_time, 'car-id': id_car, "car-type": type_car, "average-speed": average_speed}, index=[0])
        df_speed = pd.concat([df_speed, row], ignore_index=True)

    df_speed.to_csv("data\MC1\speed.csv", index=False)
    return df_speed

database, speed = process_data()
print(speed.head())