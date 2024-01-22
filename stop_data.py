import json
import requests


# Creates list with time and location
def create_brigade(time, lon, lat):
    return [(time, lon, lat)]


# Creates a node in bus dictionary.
def create_bus(brig_id, time, lon, lat):
    return {brig_id: create_brigade(time, lon, lat)}


# Creates a global timetable for all buses. Saves it in a 'json' file.
def get_bus_data():
    bus_dict = {}
    stop_url = ("https://api.um.warszawa.pl/api/action/dbstore_get?"
                + "id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7")
    stops = requests.get(stop_url).json()['result']
    stop_dicts = []
    for stop in stops:
        stop_dicts.append({'packID': stop['values'][0]['value'], 'stopID': stop['values'][1]['value'], 'lon': stop['values'][4]['value'], 'lat': stop['values'][5]['value']})
    index_len = len(stop_dicts)
    index = 1
    for stop in stop_dicts:
        bus_url = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-'
                   + '66c479ad5942&busstopId=' + stop['packID'] + '&busstopNr=' + stop['stopID']
                   + '&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')
        bus_data = requests.get(bus_url).json()['result']
        for line_data in bus_data:
            line_id = line_data['values'][0]['value']
            if len(line_id) > 2:
                stop_url = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238'
                            + '&busstopId=' + stop['packID'] + '&busstopNr=' + stop['stopID']
                            + '&line=' + line_id + '&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')
                stop_data = requests.get(stop_url).json()['result']
                for time in stop_data:
                    brig_id = time['values'][2]['value']
                    time_id = time['values'][5]['value']
                    brigades = bus_dict.get(line_id)
                    if brigades is None:
                        bus_dict.update({line_id: create_bus(brig_id, time_id, stop['lon'], stop['lat'])})
                    else:
                        brigade = brigades.get(brig_id)
                        if brigade is None:
                            brigades.update({brig_id: create_brigade(time_id, stop['lon'], stop['lat'])})
                        else:
                            brigade.append((time_id, stop['lon'], stop['lat']))
        print("Progress: " + str(index) + "/" + str(index_len))
        index = index + 1
    with open('BUS_STOP_TIMETABLE.json', 'w') as file:
        json.dump(bus_dict, file)

get_bus_data()