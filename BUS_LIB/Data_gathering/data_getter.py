import os
import json
import pause
import requests
from datetime import datetime, timedelta


BUS_POS_URL = ("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e"
               + "-927d-4ad3-9500-4ab9e55deb59&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7&type=1")


# Downloading data from 'url' to file named 'tag', which is being put into directory 'storage'.
# Tag is the name of a file from which dataframe is going to be made of.
# Storage is the name of folder which is the directory of said file.
def read_new_batch(tag="1", storage="DATA", url=BUS_POS_URL):
    dicts = ''  # Dictionary with downloaded data.
    path = os.path.join(os.getcwd(), str(storage), tag + ".json")
    while not isinstance(dicts, list):
        dicts = requests.get(url).json()['result']
    with open(path, 'w') as file:
        json.dump(dicts, file)


# Collecting data 'batches' times.
# Tag is the name of a file from which dataframe is going to be made of.
# Storage is the name of folder which is the directory of said file.
# Data is being downloaded in 'consistency' time periods measured in seconds.
def get_pos_data(batches=60, tag='', storage="DATA", consistency=60):
    if not os.path.isdir(str(storage)):  # Making 'storage' if it doesn't exist yet.
        os.mkdir(storage)
    sleep_time = datetime.today()
    if batches > 0:  # Downloading the first batch.
        read_new_batch(tag + "_1", storage)
    for i in range(2, batches + 1):  # Downloading other batches.
        print("Progress:" + str(i - 1) + "/" + str(batches))
        sleep_time = sleep_time + timedelta(seconds=consistency)
        pause.until(sleep_time)  # Waiting for exactly minute to pass since last downloading.
        read_new_batch(tag + "_" + str(i), storage)
