import pandas as pd
from dash import dcc, html
import plotly.express as px

def process_data():
    df = pd.read_csv("C:/Users/20182667/Documents/Studie/Vakken/Master/Visual Analytics/visual-analytics-dashboard/data/MC1/SensorData.csv")
    print(df.head())

    # set types
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    print(df.dtypes)

    print(len(df))
    df.dropna
    print(len(df))
    # There are no null values 

    print(df['car-type'].value_counts())
    print(df["gate-name"].value_counts())
    # There are no weird values in the columns

    print(df["car-type"].nunique())
     
    # fig = px.line(df, x="Timestamp")
    # fig.show()
    # doesn't seem to be any gaps in the data 

    df["month"] = df["Timestamp"].dt.month
    df.to_csv("C:/Users/20182667/Documents/Studie/Vakken/Master/Visual Analytics/visual-analytics-dashboard/data/MC1/SensorData.csv",
              index=False)

process_data()