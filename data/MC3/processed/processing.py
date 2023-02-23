import os
import pandas as pd
import json

def process_data():

    for file_name in os.listdir("data/MC3/raw"):
        image_index = file_name[5:7]
        date = file_name[8:18]
        file_path = "data/MC3/raw/" + file_name
        df = pd.read_csv(file_path)

        images = {"date": date}

        print("Working on image: " + image_index)

        rgb_image = []
        rgb_row = []
        health_image = []
        health_row = []
        flood_image = []
        flood_row = []
        snow_image = []
        snow_row = []
        NDVI_image = []
        NDVI_row = []


        for index, line in df.iterrows():
            rgb_row.append([int(line["B1"]), int(line["B2"]), int(line["B3"])])
            health_row.append([int(line["B4"]), int(line["B3"]), int(line["B2"])])
            flood_row.append([int(line["B5"]), int(line["B4"]), int(line["B2"])])
            snow_row.append([int(line["B1"]), int(line["B5"]), int(line["B6"])])

            # Deal with division by 0 error
            if (line["B4"] + line["B3"] == 0):
                NDVI_row.append(0)
            else:
                NDVI_row.append((int(line["B4"]) - int(line["B3"]))/(int(line["B4"]) + int(line["B3"])))

            if line["X"] == 650:
                rgb_image.append(rgb_row)
                rgb_row = []
                health_image.append(health_row)
                health_row = []
                flood_image.append(flood_row)
                flood_row = []
                snow_image.append(snow_row)
                snow_row = []
                NDVI_image.append(NDVI_row)
                NDVI_row = []

        images["RGB"] = rgb_image
        images["plant_health"] = health_image
        images["floods_or_burned"] = flood_image
        images["snow_ice_clouds"] = snow_image
        images["NDVI"] = NDVI_image

        print("Finished image: " + image_index)

        images_json = json.dumps(images)

        with open("data/MC3/processed/" + image_index + "_" + date + ".json", "w") as outfile:
            outfile.write(images_json)

process_data()