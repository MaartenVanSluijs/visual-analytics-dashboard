import numpy as np
import pandas as pd
import matplotlib.image as mpimg

class OneHotEncoding():
    def __init__(self) -> None:
        self.df = pd.read_csv("data\MC1\SensorDataProcessed.csv")

    def make_one_hot_encoding(self):
        """
        This function creates a one hot encoding of the gate-names and saves it to a csv file
        """
        x_values = self.get_x_values()
        df_x = pd.DataFrame(x_values)
        df_x.to_csv("data\MC1\one_hot_encoding.csv", index=False)
    
    def make_locations_dict(self):
        """
        This function creates a dictionary of the locations and their coordinates and saves it to a parquet file
        """
        # Get the locations
        locations = self.df["gate-name"].unique().tolist()
        locations_dict = {}
        coordinates_dict = self.add_coordinates()
    
        # Add the locations and their coordinates to a dictionary
        locations_dict['location'] = locations
        locations_dict['coordinates'] = [coordinates_dict[location] for location in locations]

        # Save the dictionary to a parquet file
        df_locations = pd.DataFrame(locations_dict)
        df_locations.to_parquet("data\MC1\locations.parquet")
    
    def add_coordinates(self):
        """
        This function adds the coordinates of the locations to a dictionary

        Returns:
        --------
        coordinates_dict (dict): A dictionary containing the coordinates of the locations
        """
        img = mpimg.imread('data\MC1\Lekagul Roadways.bmp')

        # Fill in the locations in the order of the image y axis (top to bottom)
        improved_locations = ['general-gate0', 'general-gate1', 'general-gate2', 'general-gate3', 'general-gate4', 'general-gate5', 'general-gate6', 'general-gate7', 'ranger-stop0', 'ranger-stop1', 'ranger-stop2', 'ranger-stop3', 'ranger-stop4', 'ranger-stop5', 'ranger-stop6', 'ranger-stop7', 'entrance0', 'entrance1', 'entrance2', 'entrance3', 'entrance4', 'camping0', 'camping8', 'camping1', 'camping2', 'camping3', 'camping4', 'camping5', 'camping7', 'camping6', 'gate0', 'gate1', 'gate2', 'gate3', 'gate4', 'gate5', 'gate6', 'gate7', 'gate8', 'ranger-base']
        types = {'type':['general-gate', 'ranger-stop', 'entrance', 'camping', 'gate', 'ranger-base'],
            'color':[[0,255,255], [255,216,0], [76,255,0], [255,106,0], [255,0,0], [255,0,220]]}

        # Get the coordinates of the locations 
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

        # Add the coordinates to the dictionary
        for color in types['color']:
            for coordinate in coordinates:
                if (coordinate[2]== color).all():
                    names.append(improved_locations[0])
                    improved_locations.pop(0)
                    xy_coordinates.append([coordinate[1], coordinate[0]])

        dict_coordinates = dict(zip(names, xy_coordinates))
        
        return dict_coordinates

    def get_car_paths(self):
        """
        This function creates a dictionary of the car paths

        Returns:
        --------
        car_paths (dict): A dictionary containing the car paths
        """
        car_paths = {}
    
        # Fill the dictionary
        for index, row in self.df.iterrows():
            car_id = row["car-id"]
            location = row["gate-name"]
        
            if car_id in car_paths:
                car_paths[car_id].append(location)
            else:
                car_paths[car_id] = [location]
    
        return car_paths
    
    def get_x_values(self):
        """
        This function creates a one hot encoding of the gate-names
        
        Returns:
        --------
        encodings (np.array): A one hot encoding of the gate-names
        """
        gate_names = self.df["gate-name"].unique().tolist()
    
        # Create the encodings
        encodings = np.zeros((self.df["car-id"].nunique(), self.df["gate-name"].nunique()))

        # Fill the encodings
        index = 0
        for key, value in self.get_car_paths().items():
            car_path = value
    
            for gate in set(car_path):
                encodings[index][gate_names.index(gate)] = 1
    
            index += 1
    
        return encodings