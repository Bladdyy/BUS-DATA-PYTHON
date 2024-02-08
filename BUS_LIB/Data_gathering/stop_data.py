import json
import os

import requests


# Creates list with time and location
def create_brigade(time, lon, lat):
    return [(time, lon, lat)]


# Creates a node in bus dictionary.
def create_bus(brig_id, time, lon, lat):
    return {brig_id: create_brigade(time, lon, lat)}


# Creates a global timetable for all buses. Saves it in a 'json' file.
def get_bus_data(file_name="DATA/BUS_STOP_TIMETABLE"):
    bus_dict = {}  # Global timetable.
    stop_url = ("https://api.um.warszawa.pl/api/action/dbstore_get?"
                + "id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7")
    stops = requests.get(stop_url).json()['result']  # Downloading all bus stops.
    stop_dicts = []
    for stop in stops:  # Parsing data about bus stops.
        stop_dicts.append({'packID': stop['values'][0]['value'],
                           'stopID': stop['values'][1]['value'],
                           'lon': stop['values'][4]['value'],
                           'lat': stop['values'][5]['value']})
    index_len = len(stop_dicts)  # Number of all bus stops.
    index = 0  # Number of bus stops parsed.
    for stop in stop_dicts:  # Downloading all bus lines for every bus stop.
        bus_url = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-'
                   + '66c479ad5942&busstopId=' + stop['packID'] + '&busstopNr=' + stop['stopID']
                   + '&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')
        bus_data = requests.get(bus_url).json()['result']
        for line_data in bus_data:  # Downloading the times at which bus should arrive at the bus stop.
            line_id = line_data['values'][0]['value']  # Line ID.
            if len(line_id) > 2:  # Skipping trams.
                stop_url = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-'
                            + '43f9-ae6e-60518c9f3238&busstopId=' + stop['packID'] + '&busstopNr=' + stop['stopID']
                            + '&line=' + line_id + '&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')
                stop_data = requests.get(stop_url).json()['result']
                for time in stop_data:  # Saving brigade number with time and location
                    brig_id = time['values'][2]['value']  # Brigade ID.
                    time_id = time['values'][5]['value']  # Time of arrival.
                    brigades = bus_dict.get(line_id)
                    if brigades is None:  # Line ID does not exist yet.
                        bus_dict.update({line_id: create_bus(brig_id, time_id, stop['lon'], stop['lat'])})
                    else:
                        brigade = brigades.get(brig_id)
                        if brigade is None:  # Brigade ID does not exist yet.
                            brigades.update({brig_id: create_brigade(time_id, stop['lon'], stop['lat'])})
                        else:
                            brigade.append((time_id, stop['lon'], stop['lat']))
        index = index + 1  # One more bus stop done.
        print("Progress: " + str(index) + "/" + str(index_len))
    with open(str(os.getcwd()) + file_name + ".json", 'w') as file:
        json.dump(bus_dict, file)
