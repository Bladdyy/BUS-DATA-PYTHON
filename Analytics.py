import json
import math
import os
import pandas as pd
import numpy as np


# Creating new data frame made from a file named 'tag' in 'storage' directory.
def create_frame(tag='1', storage="DATA"):
    path = os.path.join(os.getcwd(), storage, tag + ".json")
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = json.load(file)
            new_frame = pd.json_normalize(data)  # Converting json file into a data frame.
        new_frame.set_index("VehicleNumber", inplace=True)  # Setting 'VehicleNumber' as an index in dataframe.
        new_frame.drop(['Lines', 'Brigade'], axis=1, inplace=True)  # Dropping useless columns.
        new_frame['Lon'] = pd.to_numeric(new_frame['Lon'])  # Converting values of useful columns.
        new_frame['Lat'] = pd.to_numeric(new_frame['Lat'])
        new_frame['Time'] = pd.to_datetime(new_frame['Time'])
        return new_frame
    else:
        print("Given path does not exist.")
        return None


# Calculates haversine formula. Creating velocity measured in km/h using calculated formula.
def haversine_velocity(row):
    if row['DelTime'] == 0:
        return np.NAN
    else:
        r = 6378000
        a = pow(np.sin(row['DelLat'] * math.pi / 360), 2)
        b = (np.cos(row['Lat'] * math.pi / 180)
             * np.cos(row['Lat2'] * math.pi / 180)
             * pow((np.sin(row['DelLon'] * math.pi / 360)), 2))
        haversine = 2 * r * np.arcsin(np.sqrt(a + b))
        return haversine / row['DelTime'] * 3.6


# Finds buses, which exceeded the speed of 50 km/h between two states in time.
def check_velocity(frame1, frame2):
    ans = np.subtract(frame2, frame1)  # Calculating change in location and time between two states.
    frame1.drop('Time', axis=1, inplace=True)  # Dropping no longer needed columns.
    frame2.drop('Time', axis=1, inplace=True)
    frame2.rename(columns={'Lon': 'Lon2', 'Lat': 'Lat2'}, inplace=True)
    ans.rename(columns={'Lon': 'DelLon', 'Lat': 'DelLat', 'Time': 'DelTime'}, inplace=True)
    frame1 = frame1.join(frame2)
    ans = ans.join(frame1)
    ans['DelTime'] = ans['DelTime'].dt.total_seconds()
    ans['Velocity'] = ans.apply(haversine_velocity, axis=1)  # Calculating average velocity.
    ans = ans.loc[ans['Velocity'] > 50]  # Choosing only buses which passed 50 km/h
    return ans.index.tolist()


# Counts buses that exceeded the speed of 50 km/h in given period of time.
def count_passed(tag='', storage='DATA', length=60):
    busses = set()  # Set of busses that exceeded the speed.
    if length > 1:
        frame1 = create_frame(tag + '1', storage)
        for i in range(2, length + 1):
            frame2 = create_frame(tag + str(i), storage)
            too_fast = check_velocity(frame1.copy(), frame2.copy())
            frame1 = frame2
            for el in too_fast:  # Adding new buses that exceeded the speed.
                busses.add(el)
        return len(busses)
    else:  # No period of time to compare.
        return 0


print(count_passed(storage='SUNDAY_TEST_DATA', length=20))
