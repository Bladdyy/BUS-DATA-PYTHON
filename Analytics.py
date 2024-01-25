import json
import math
import os
import pandas as pd
import numpy as np
import csv


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
        haversine = 2 * r * np.arcsin(np.sqrt(a + b)) / row['DelTime'] * 3.6
        if haversine > 160:  # Detecting impossible data.
            return np.NAN
        else:
            return haversine


# Finds buses, which exceeded the speed of 50 km/h between two states in time.
def check_velocity(frame1, frame2, to_file=False, file_name='BUS_SPEEDING'):
    velocity = 50
    ans = np.subtract(frame2, frame1)  # Calculating change in location and time between two states.
    frame1.drop('Time', axis=1, inplace=True)  # Dropping no longer needed columns.
    frame2.drop('Time', axis=1, inplace=True)
    frame2.rename(columns={'Lon': 'Lon2', 'Lat': 'Lat2'}, inplace=True)
    ans.rename(columns={'Lon': 'DelLon', 'Lat': 'DelLat', 'Time': 'DelTime'}, inplace=True)
    frame1 = frame1.join(frame2)
    ans = ans.join(frame1)
    ans['DelTime'] = ans['DelTime'].dt.total_seconds()
    ans['Velocity'] = ans.apply(haversine_velocity, axis=1)  # Calculating average velocity.
    ans = ans.loc[ans['Velocity'] > velocity]  # Choosing only buses which passed 50 km/h
    if to_file:
        path = os.path.join(os.getcwd(), file_name + ".csv")
        distances = ans[['Lon', 'Lat', 'Lon2', 'Lat2']].values.tolist()
        with open(path, 'a') as file:
            writer = csv.writer(file)
            for dist in distances:
                writer.writerow(dist)
        file.close()

    return ans.index.tolist()


# Counts different bus numbers that exceeded the speed of 50 km/h in given period of time.
# Saves data in csv file if needed.
def count_passed(tag='', storage='DATA', length=60, to_file=False, file_name='BUS_SPEEDING'):
    busses = set()  # Set of busses that exceeded the speed.
    if length > 1:
        if to_file:  # Creating an empty file.
            path = os.path.join(os.getcwd(), file_name + ".csv")
            with open(path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(['Lon', 'Lat', 'Lon2', 'Lat2'])
                file.close()
        group = 0
        frame1 = create_frame(tag + '1', storage)
        for i in range(2, length + 1):
            frame2 = create_frame(tag + str(i), storage)
            too_fast = check_velocity(frame1.copy(), frame2.copy(), to_file, file_name)
            frame1 = frame2
            group = group + len(too_fast)
            for el in too_fast:  # Adding new buses that exceeded the speed.
                busses.add(el)
        return len(busses)
    else:  # No period of time to compare.
        return 0


print(count_passed(tag='morning_', storage='MORNING_DATA', length=100, to_file=True))
