import os.path
import plotly.graph_objects as go
import csv


# Shows where buses were speeding on the interactive map.
# Name_file is the name of file that contains the distances where buses were speeding.
def show_speed_map(name_file='DATA/BUS_SPEEDING'):
    path = os.path.join(os.getcwd(), name_file + '.csv')
    lon = []  # Longitudes of distances.
    lat = []  # Latitudes of distances.
    with open(path, "r") as file:  # Reading speeding distances.
        reader = csv.DictReader(file)
        for row in reader:
            lon.append([row['Lon'], row['Lon2']])
            lat.append([row['Lat'], row['Lat2']])
    fig = go.Figure(go.Scattermapbox())  # Map creating.

    for i in range(len(lon)):  # Adding distances to the map.
        fig.add_trace(go.Scattermapbox(
            mode="markers+lines",
            lon=lon[i],
            lat=lat[i],
            marker={'size': 10}))

    fig.update_layout(  # Updating map layout.
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 21.017532, 'lat': 52.237049},
            'style': "open-street-map",
            'zoom': 9
        })
    fig.show()
