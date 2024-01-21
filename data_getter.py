import os
import urllib.request
import json
import pause
from datetime import datetime, timedelta

BUS_POS_URL = ("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e"
               + "-927d-4ad3-9500-4ab9e55deb59&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7&type=1")


# Downloading data from 'url' to file named 'tag', which is being put into directory 'storage'.
def read_new_patch(tag="1", storage="DATA", url=BUS_POS_URL):
    dicts = ''  # Dictionary with downloaded data.
    path = os.path.join(os.getcwd(), str(storage), tag + ".json")
    while not isinstance(dicts, list):
        contents = urllib.request.urlopen(url).read()
        dicts = json.loads(contents)['result']
    with open(path, 'w') as file:
        json.dump(dicts, file)


# Collecting data 'patches' times. Data is being downloaded in 'consistency' time periods measured in seconds.
# Data is being stored in file named 'tag', which is being put into 'storage' directory.
def get_pos_data(patches=60, tag='', storage="DATA", consistency=1):
    if not os.path.isdir(str(storage)):  # Making 'storage' if it doesn't exist yet.
        os.mkdir(storage)
    sleep_time = datetime.today()
    if patches > 0:  # Downloading the first patch.
        read_new_patch(tag + "_1", storage)
    for i in range(2, patches + 1):  # Downloading other patches.
        sleep_time = sleep_time + timedelta(seconds=consistency)
        pause.until(sleep_time)  # Waiting for exactly minute to pass since last downloading.
        read_new_patch(tag + "_" + str(i), storage)