import os
import urllib.request
import json

url = "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=b7bc7308-6c4e-454d-8a20-31e478fd9ee7&type=1"


def read_new_patch(tag, storage="DATA"):
    path = os.path.join(os.getcwd(), str(storage), str(tag) + ".json")
    dicts = ''
    while not isinstance(dicts, list):
        contents = urllib.request.urlopen(url).read()
        dicts = json.loads(contents)['result']

    with open(path, 'w') as file:
        json.dump(dicts, file)


read_new_patch(1)
