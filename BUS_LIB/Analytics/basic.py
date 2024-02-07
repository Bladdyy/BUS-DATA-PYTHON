import json
import math
import os
import numpy as np
import pandas as pd


# Creating new data frame made from a file named 'tag' in 'storage' directory.
# Tag is the name of a file from which dataframe is going to be made of.
# Storage is the name of folder which is the directory of said file.
# Drop arguments allow to drop certain columns in dataframe.
def create_frame(tag='1', storage="DATA", drop_lines=False, drop_brigade=False, drop_vehicle=False):
    path = os.path.join(os.getcwd(), storage, tag + ".json")
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)
            new_frame = pd.json_normalize(data)  # Converting json file into a data frame.
        if not drop_vehicle:
            new_frame.set_index("VehicleNumber", inplace=True)  # Setting 'VehicleNumber' as an index in dataframe.
        else:
            new_frame.drop(["VehicleNumber"], axis=1, inplace=True)  # Dropping useless columns.
        if drop_brigade:
            new_frame.drop(['Brigade'], axis=1, inplace=True)  # Dropping useless columns.
        if drop_lines:
            new_frame.drop(['Lines'], axis=1, inplace=True)  # Dropping useless columns.
        new_frame['Lon'] = pd.to_numeric(new_frame['Lon'])  # Converting values of useful columns.
        new_frame['Lat'] = pd.to_numeric(new_frame['Lat'])
        new_frame['Time'] = pd.to_datetime(new_frame['Time'])

        return new_frame
    else:
        print(path)
        print("Given path does not exist.")
        return None


# Creating velocity measured in km/h between two points using calculated formula.
# Row is a dictionary or row from dataframe consisting of needed values.
def haversine_velocity(row):
    impossible_data = 90  # Buses in warsaw can only reach 90 km/h.
    if row['DelTime'] == 0:
        return np.NAN
    else:
        haversine = haversine_distance(row) / row['DelTime'] * 3600
        if haversine > impossible_data:  # Detecting impossible data.
            return np.NAN
        else:
            return haversine


# Calculating the distance between two points in kilometers.
# Row is a dictionary or row from dataframe consisting of needed values.
def haversine_distance(row):
    r = 6378
    a = pow(np.sin(row['DelLat'] * math.pi / 360), 2)
    b = (np.cos(row['Lat'] * math.pi / 180)
         * np.cos(row['Lat2'] * math.pi / 180)
         * pow((np.sin(row['DelLon'] * math.pi / 360)), 2))
    haversine = 2 * r * np.arcsin(np.sqrt(a + b))
    return haversine
