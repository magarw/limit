import json
import os

INPUT_PATH = "../../../data/parallel/multilingual/manually_verified/"
files = os.listdir(INPUT_PATH)

PARALLEL_RAW_PATH = "../../../data/parallel/raw/"
raw_files = os.listdir(PARALLEL_RAW_PATH)

MONO_PATH = "../../../data/language-id/monolingual_combined/"
mono_files = os.listdir(MONO_PATH)

PARALLEL_OUT_PATH = "../../../data/parallel/combined/"

ISOCODES = "../../../data/parallel/isocodes.json"
isocodes = json.load(open(ISOCODES))

# goal: to look through all the multlingual files, and add the stories
# in the relevant parallel text file. If a file doesn't exist, then create it.
"""
for file in files:
    print(file)
    multilingual_file = json.load(open(INPUT_PATH + file))["data"]

    l1, l2 = file.replace(".json","").split('-')
    l1_code, l2_code = isocodes[l1], isocodes[l2]
    name1 = l1_code + '-' + l2_code + ".json"
    name2 = l2_code + '-'+ l1_code + ".json"
    print(name1, name2)
    if name1 in raw_files:
        selected = json.load(open(PARALLEL_RAW_PATH + name1))
        for story_id in multilingual_file.keys():
            if story_id not in selected.keys(): # i.e. text from both languages for a particular story is not present
                selected[story_id] = {}
                selected[story_id][l1_code] = multilingual_file[story_id][l1]
                selected[story_id][l2_code] = multilingual_file[story_id][l2]
        with open(PARALLEL_OUT_PATH + name1, 'w') as fp:
            json.dump(selected, fp)
    elif name2 in raw_files:
        selected = json.load(open(PARALLEL_RAW_PATH + name2))
        for story_id in multilingual_file.keys():
            if story_id not in selected.keys(): # i.e. text from both languages for a particular story is not present
                selected[story_id] = {}
                selected[story_id][l1_code] = multilingual_file[story_id][l1]
                selected[story_id][l2_code] = multilingual_file[story_id][l2]
        with open(PARALLEL_OUT_PATH + name1, 'w') as fp:
            json.dump(selected, fp)

    else:
        # neither file is present i.e. will need to create one.
        selected = {}
        for story_id in multilingual_file.keys():
            selected[story_id] = {}
            selected[story_id][l1_code] = multilingual_file[story_id][l1]
            selected[story_id][l2_code] = multilingual_file[story_id][l2]
        with open(PARALLEL_OUT_PATH + name1, 'w') as fp:
            json.dump(selected, fp)
"""
# also, to add the individual texts into monolingual text section, if
# the file for monolingual text isn't already there.
for file in files:
    multilingual_file = json.load(open(INPUT_PATH + file))
    multilingual_file_info = multilingual_file["info"]
    multilingual_data = multilingual_file["data"]
    ref = multilingual_file_info["reference_language"]
    smp = multilingual_file_info["sample_language"]
    l1, l2 = smp.split("-")
    if ref == l1:
        interest = l2
    else:
        interest = l1

    interest_code =isocodes[interest]
    print(interest, interest_code)
    name = interest_code + ".txt"

    with open(MONO_PATH + interest_code + ".txt","a") as file_writer:
        for story_id in multilingual_data.keys():
            for e in multilingual_data[story_id][interest]:
                file_writer.write(e.strip().replace("\n", "").replace("\r", "").replace("\r\n", "") + "\n")
