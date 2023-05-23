# TODO: Delete 0 and Multilingual

import json
INPUT_PATH = "../../../data/parallel/master.json"
master_json = json.load(open(INPUT_PATH))

for key in master_json.keys():
    langs = master_json[key].keys()
    if "Multilingual" in langs:
        del master_json[key]["Multilingual"]
    if "0" in langs:
        del master_json[key]["0"]

with open("../../../data/parallel/new_master.json", 'w') as fp:
    json.dump(master_json, fp)
