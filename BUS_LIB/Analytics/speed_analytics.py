from BUS_LIB.Analytics.basic import create_frame, haversine_velocity
import os
import numpy as np
import csv


# Finds buses, which exceeded the speed of 50 km/h between two timeframes.
# Frame1 and frame2 are dataframes representing those two timeframes.
# To_file allows to save the data about busses that were speeding to file named file_name.
def check_velocity(frame1, frame2, to_file=False, file_name='DATA/BUS_SPEEDING'):
    velocity = 50
    ans = np.subtract(frame2, frame1)  # Calculating change in location and time between two timeframes.
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
# Tag is the name of a file from which dataframe is going to be made of.
# Storage is the name of folder which is the directory of said file.
# Length is the amount of the timeframes to compare.
# To_file allows to save the data about busses that were speeding to file named file_name.
def count_passed(tag='', storage='DATA', length=60, to_file=False, file_name='DATA/BUS_SPEEDING'):
    busses = set()  # Set of busses that exceeded the speed.
    if length > 1:
        if to_file:  # Creating an empty file.
            path = os.path.join(os.getcwd(), file_name + ".csv")
            with open(path, "w") as file:
                writer = csv.writer(file)
                writer.writerow(['Lon', 'Lat', 'Lon2', 'Lat2'])
                file.close()
        group = 0
        frame1 = create_frame(tag + '1', storage, drop_lines=True, drop_brigade=True)
        for i in range(2, length + 1):
            frame2 = create_frame(tag + str(i), storage, drop_lines=True, drop_brigade=True)
            too_fast = check_velocity(frame1.copy(), frame2.copy(), to_file, file_name)
            frame1 = frame2
            group = group + len(too_fast)
            for el in too_fast:  # Adding new buses that exceeded the speed.
                busses.add(el)
        return len(busses)
    else:  # No period of time to compare.
        return 0
