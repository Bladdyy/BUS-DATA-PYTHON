from datetime import datetime, date
from operator import itemgetter
import plotly.express as px
import json
import os
import pandas as pd
from . import basic


# Creates a graph of buses being late from late_dict and displays it.
def show_late(late_dict):
    items = late_dict.items()
    temp_list = []
    for item in items:  # Creates a list of tuples (bus line, how many late stops, (how many late stops / all stops))
        temp_list.append([item[0], item[1][0], (item[1][0] / item[1][1])])
    df = pd.DataFrame(temp_list)  # Creates dataframe from list.
    df.rename(columns={0: 'BUS LINE', 1: 'LATE STOPS', 2: 'PERCENTAGE'}, inplace=True)
    fig = px.scatter(df, x="LATE STOPS", y="PERCENTAGE", color="BUS LINE")  # Creates a graph.
    fig.show()  # Displays graph.


# Adds a position to 'late_dict' where key equals to 'bus'.
# If late equals True then the 'bus' is late.
def add_late(late_dict, bus, late):
    val = late_dict.get(bus)
    if val is None:
        if late:
            late_dict.update({bus: [1, 1]})
        else:
            late_dict.update({bus: [0, 1]})
    else:
        if late:
            late_dict.update({bus: [val[0] + 1, val[1] + 1]})
        else:
            late_dict.update({bus: [val[0], val[1] + 1]})


# Creates a dictionary of bus ('bus_dict') locations between first and last timeframe.
# Tag is the name of a file from which dataframe is going to be made of.
# Storage is the name of folder which is the directory of said file.
# Length is the amount of the timeframes to compare.
def create_bus_schedule(bus_dict, tag='', storage='DATA', length=60):
    for i in range(1, length + 1):
        main_frame = basic.create_frame(tag=tag + str(i), storage=storage, drop_vehicle=True)
        for index, row in main_frame.iterrows():  # Inserting one timeframe to dictionary.
            line = bus_dict.get(row['Lines'])
            if line is None:
                bus_dict.update({row['Lines']: {row['Brigade']: [[row['Time'], row['Lon'], row['Lat']]]}})
            else:
                brigade = line.get(row['Brigade'])
                if brigade is None:
                    line.update({row['Brigade']: [[row['Time'], row['Lon'], row['Lat']]]})
                else:
                    brigade.append([row['Time'], row['Lon'], row['Lat']])


# Counts bus stops where buses arrived on time.
# Returns the said amount with the amount of all stops, where buses were supposed to arrive in a list.
# Table is a global schedule for all buses in Warsaw.
# Tag is the name of a file from which dataframe is going to be made of.
# Storage is the name of folder which is the directory of said file.
# Length is the amount of the timeframes to compare.
# If visualize is set to True, displays a graph showing percentage of being late.
def bus_late(table="/DATA/BUS_STOP_TIMETABLE", tag='', storage='DATA', length=60, visualize=False):
    path = os.path.join(os.getcwd(), table + ".json")
    bus_dict = {}
    if os.path.exists(path) and length >= 2:  # If there are more than two timeframes to compare.
        with open(path, "r") as file:
            timetable = json.load(file)  # Global schedule of Warsaw buses.
        create_bus_schedule(bus_dict, tag, storage, length)  # Creates a bus location schedule.
        on_time = 0  # How many buses arrived on time.
        all_stops = 0  # How many stops were analyzed.
        late = {}  # Dictionary keeping track of number of stops, which buses weren't on time on.
        measurement_error = 1.2
        impossible_data = 120  # Max time between two timeframes next to each other.
        for bus in bus_dict.keys():  # Iterates over bus lines.
            line = bus_dict.get(bus)
            for brig in line.keys():  # Iterates over brigades of each line.
                brigade = line.get(brig)
                arrivals = timetable.get(bus)
                if arrivals is not None:
                    arrivals = arrivals.get(brig)
                if arrivals is not None:
                    brigade = sorted(brigade, key=itemgetter(0))  # Sorts locations of buses by time.
                    mintime = str(brigade[0][0].time())  # First appearance of the bus.
                    maxtime = str(brigade[-1][0].time())  # Last appearance of the bus.
                    sorted_arrivals = []  # List of stops which bus should appear on between 'mintime' and 'maxtime'.
                    for loc in arrivals:
                        if loc is not None and loc[0] is not None and maxtime >= loc[0] >= mintime:
                            sorted_arrivals.append(loc)
                    sorted_arrivals = sorted(sorted_arrivals, key=itemgetter(0))  # Sorts stops.
                    stop_index = 0  # Index of currently analyzed stop.
                    bus_index = 0  # Index of currently analyzed bus location.
                    while stop_index < len(sorted_arrivals):  # Checks all bus stops.
                        # If both last bus timeframes are from earlier than analyzed stop.
                        if str(brigade[bus_index][0].time()) < sorted_arrivals[stop_index][0]:
                            bus_index = bus_index + 1
                        # If time of currently analyzed stop is between two last timeframes.
                        else:
                            bus1 = brigade[bus_index - 1]  # Timeframe data before last timeframe data.
                            bus2 = brigade[bus_index]  # Last timeframe data.
                            stop = sorted_arrivals[stop_index]  # Stop data.
                            # Velocity of bus between those two timeframes.
                            velocity = (basic.haversine_velocity({'Lat': float(bus1[2]), 'Lat2': float(bus2[2]),
                                                                  'DelLat': abs(float(bus1[2]) - float(bus2[2])),
                                                                  'DelLon': abs(float(bus1[1]) - float(bus2[1])),
                                                                  'DelTime': (bus2[0] - bus1[0]).total_seconds()})
                                        / 3600)
                            # Distance from 'bus1' timeframe to 'stop'.
                            distance = basic.haversine_distance({'Lat': float(bus1[2]), 'Lat2': float(stop[1]),
                                                                 'DelLat': abs(float(bus1[2]) - float(stop[1])),
                                                                 'DelLon': abs(float(bus1[1]) - float(stop[2]))}
                                                                )
                            # Time in which bus should arrive from 'bus1' to 'stop'.
                            arrival_time = (datetime.combine(date.today(),
                                            datetime.strptime(stop[0], '%H:%M:%S').time())
                                            - datetime.combine(date.today(), bus1[0].time())).total_seconds()
                            if arrival_time < impossible_data:
                                all_stops = all_stops + 1
                                if velocity * arrival_time * measurement_error >= distance:  # Bus arrived on time.
                                    add_late(late, bus, False)
                                    on_time = on_time + 1
                                else:  # Bus is late.
                                    add_late(late, bus, True)
                            stop_index = stop_index + 1
        # Visualization of lateness.
        if visualize:
            show_late(late)
        return [on_time, all_stops]
    elif length < 2:
        print("Not enough timeframes to analyze.")
    else:
        print("Given path does not exist.", path)

