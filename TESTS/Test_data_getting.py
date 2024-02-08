import json
import os.path


from BUS_LIB.Data_gathering.data_getter import read_new_batch
import responses

from BUS_LIB.Data_gathering.stop_data import get_bus_data

BUS_POS_URL = ("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e"
               + "-927d-4ad3-9500-4ab9e55deb59&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7&type=1")


@responses.activate
def test_read_new_batch():
    responses.add(responses.GET, BUS_POS_URL,
                  json={'result': [{"Lines": "213",
                                    "Lon": 21.138384,
                                    "VehicleNumber": "1000",
                                    "Time": "2024-01-25 16:04:03",
                                    "Lat": 52.214403,
                                    "Brigade": "3"}]})
    read_new_batch(tag='temp_data', storage='TEST_DATA')
    path = os.path.join(os.getcwd(), 'TEST_DATA/temp_data.json')
    with open(path, 'r') as file:
        data = json.load(file)
    assert data[0]['Lines'] == '213'
    assert data[0]['Lon'] == 21.138384
    assert data[0]['VehicleNumber'] == '1000'
    assert len(data[0]) == 6
    assert len(data) == 1


@responses.activate
def test_get_bus_data():
    stop_url = ("https://api.um.warszawa.pl/api/action/dbstore_get?"
                + "id=ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7")
    bus_url = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=88cd555f-6f31-43ca-9de4-'
               + '66c479ad5942&busstopId=4020&busstopNr=01&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')
    bus124 = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-'
              + '43f9-ae6e-60518c9f3238&busstopId=4020&busstopNr=01&line=124'
              + '&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')
    busn88 = ('https://api.um.warszawa.pl/api/action/dbtimetable_get?id=e923fa0e-d96c-'
              + '43f9-ae6e-60518c9f3238&busstopId=4020&busstopNr=01&line=N88'
              + '&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7')

    responses.add(responses.GET, stop_url,
                  json={'result': [{'values': [{'value': '4020', 'key': 'zespol'},
                                               {'value': '01', 'key': 'slupek'},
                                               {'value': 'Olszowa', 'key': 'nazwa_zespolu'},
                                               {'value': '1609', 'key': 'id_ulicy'},
                                               {'value': '52.160570', 'key': 'szer_geo'},
                                               {'value': '20.936780', 'key': 'dlug_geo'},
                                               {'value': 'al.Krakowska', 'key': 'kierunek'},
                                               {'value': '2023-10-07 00:00:00.0', 'key': 'obowiazuje_od'}]},]})

    responses.add(responses.GET, bus_url,
                  json={'result': [{'values': [{'value': '124', 'key': 'linia'}]},
                                   {'values': [{'value': 'N88', 'key': 'linia'}]}]})
    responses.add(responses.GET, bus124,
                  json={'result': [{'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'null', 'key': 'symbol_1'},
                                               {'value': '1', 'key': 'brygada'},
                                               {'value': 'P+R Al.Krakowska', 'key': 'kierunek'},
                                               {'value': 'TP-OKE', 'key': 'trasa'},
                                               {'value': '04:45:00', 'key': 'czas'}]},
                                   {'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'null', 'key': 'symbol_1'},
                                               {'value': '1', 'key': 'brygada'},
                                               {'value': 'P+R Al.Krakowska', 'key': 'kierunek'},
                                               {'value': 'TP-OKE', 'key': 'trasa'},
                                               {'value': '05:12:00', 'key': 'czas'}]},
                                   {'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'null', 'key': 'symbol_1'},
                                               {'value': '2', 'key': 'brygada'},
                                               {'value': 'P+R Al.Krakowska', 'key': 'kierunek'},
                                               {'value': 'TP-OKE', 'key': 'trasa'},
                                               {'value': '05:27:00', 'key': 'czas'}]}]})
    responses.add(responses.GET, busn88,
                  json={'result': [{'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'j', 'key': 'symbol_1'},
                                               {'value': '206', 'key': 'brygada'},
                                               {'value': 'pl.Szwedzki', 'key': 'kierunek'},
                                               {'value': 'TP-JAN-P', 'key': 'trasa'},
                                               {'value': '24:19:00', 'key': 'czas'}]},
                                   {'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'j', 'key': 'symbol_1'},
                                               {'value': '205', 'key': 'brygada'},
                                               {'value': 'pl.Szwedzki', 'key': 'kierunek'},
                                               {'value': 'TP-JAN-P', 'key': 'trasa'},
                                               {'value': '25:18:00', 'key': 'czas'}]},
                                   {'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'j', 'key': 'symbol_1'},
                                               {'value': '206', 'key': 'brygada'},
                                               {'value': 'pl.Szwedzki', 'key': 'kierunek'},
                                               {'value': 'TP-JAN-P', 'key': 'trasa'},
                                               {'value': '26:18:00', 'key': 'czas'}]},
                                   {'values': [{'value': 'null', 'key': 'symbol_2'},
                                               {'value': 'p', 'key': 'symbol_1'},
                                               {'value': '206', 'key': 'brygada'},
                                               {'value': 'Centrum', 'key': 'kierunek'},
                                               {'value': 'TP-CEN-P', 'key': 'trasa'},
                                               {'value': '27:08:00', 'key': 'czas'}]}]})
    get_bus_data(file_name='/TEST_DATA/SMALL_SCHEDULE')
    path = os.path.join(os.getcwd(), 'TEST_DATA/SMALL_SCHEDULE.json')
    with open(path, 'r') as file:
        data = json.load(file)
    assert len(data) == 2
    assert len(data['124']) == 2
    assert data['124']['1'][1][2] == "20.936780"
    assert data['N88']['206'][2][0] == "27:08:00"
