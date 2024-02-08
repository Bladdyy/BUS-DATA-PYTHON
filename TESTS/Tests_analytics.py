from datetime import datetime
from BUS_LIB.Analytics.basic import haversine_distance, haversine_velocity, create_frame
from BUS_LIB.Analytics.speed_analytics import check_velocity, count_passed
from BUS_LIB.Analytics.stop_analytics import add_late, create_bus_schedule, bus_late


def test_haversine_distance():
    # Calculates distance between Warsaw and Paris.
    row = {"Lat": 48.864716, "Lat2": 52.237049,
           "DelLat": (52.237049 - 48.864716), "DelLon": (21.017532 - 2.349014)}
    result = haversine_distance(row)
    # Measurement error.
    assert result >= 1368
    assert result <= 1370


def test_impossible_haversine_velocity():
    # Calculates velocity if traveling between Warsaw and Paris in 10 minutes.
    row = {"Lat": 48.864716, "Lat2": 52.237049,
           "DelLat": (52.237049 - 48.864716), "DelLon": (21.017532 - 2.349014),
           "DelTime": 600}
    result = haversine_velocity(row)
    assert str(result) == 'nan'


def test_haversine_velocity():
    # Calculates velocity if traveling between Warsaw and Paris in 27.4 hours.
    row = {"Lat": 48.864716, "Lat2": 52.237049,
           "DelLat": (52.237049 - 48.864716), "DelLon": (21.017532 - 2.349014),
           "DelTime": 27.4 * 3600}
    result = haversine_velocity(row)
    # Expected velocity 50 km/h.
    assert result <= 51
    assert result >= 49


def test_create_frame():
    df = create_frame(tag='create', storage="TEST_DATA")
    assert '1000' == df.index[0]
    assert '213' == df['Lines'].tolist()[0]
    assert 21.12834 == df['Lon'].tolist()[0]
    assert 52.214874 == df['Lat'].tolist()[0]
    assert '3' == df['Brigade'].tolist()[0]
    assert (datetime.strptime("2024-01-27 16:02:22", "%Y-%m-%d %H:%M:%S")
            == datetime.strptime(str(df['Time'].tolist()[0]), "%Y-%m-%d %H:%M:%S"))


def test_check_velocity():
    frame1 = create_frame('frame1', "TEST_DATA", drop_lines=True, drop_brigade=True)
    frame2 = create_frame('frame2', "TEST_DATA", drop_lines=True, drop_brigade=True)
    assert 0 == len(check_velocity(frame1, frame2, to_file=False, file_name='DATA/BUS_SPEEDING'))
    frame1 = create_frame('frame1', "TEST_DATA", drop_lines=True, drop_brigade=True)
    frame2 = create_frame('frame3', "TEST_DATA", drop_lines=True, drop_brigade=True)
    assert '1000' == check_velocity(frame1, frame2, to_file=False, file_name='DATA/BUS_SPEEDING')[0]


def test_count_passed():
    assert 1 == count_passed(tag='count', storage='TEST_DATA', length=2)


def test_add_late():
    late_dict = {}
    add_late(late_dict, '21', True)
    add_late(late_dict, '21', True)
    add_late(late_dict, '21', False)
    add_late(late_dict, '37', False)
    add_late(late_dict, '37', False)
    assert late_dict['21'][0] == 2
    assert late_dict['21'][1] == 3
    assert late_dict['37'][0] == 0
    assert late_dict['37'][1] == 2


def test_create_bus_schedule():
    bus_dict = {}
    create_bus_schedule(bus_dict, tag='small_schedule', storage='TEST_DATA', length=2)
    assert len(bus_dict['213']['3']) == 2
    assert len(bus_dict['213']) == 2
    assert bus_dict['213']['24'][0][1] == 20.926357
    assert bus_dict['96']['31'][0][2] == 52.288189


def test_bus_late():
    result = bus_late(table="TEST_DATA/FAKETABLE", tag='small_schedule', storage='TEST_DATA', length=2)
    assert result[0] == 2
    assert result[1] == 3
