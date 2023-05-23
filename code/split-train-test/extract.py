import json
import time
import nltk
from itertools import combinations

ISO_PATH = "../../data/parallel/isocodes.json"
isocodes = json.load(open(ISO_PATH))
isocode_values = set()
iso_keys = list(isocodes.keys())
for key in isocodes:
    isocode_values.add(isocodes[key])

INPUT_PATH = '../../data/parallel/master.json'
master_json = json.load(open(INPUT_PATH))
keys = master_json.keys()
print("Number of keys: ", len(keys))

def extract(arg, master_keys, iso_keys, isocodes):
    extracted_dict = {}
    for key in master_keys:
        story_versions = list(master_json[key].keys())
        story_versions_codes = []
        for s in story_versions:
            if s in iso_keys:
                story_versions_codes.append(isocodes[s])
            else:
                story_versions_codes.append("")

        multiway = True
        for q in arg:
            if q not in story_versions_codes:
                multiway = False

        if multiway:
            inside_json = {}
            for i in range(len(story_versions)):
                if story_versions_codes[i] in arg:
                    inside_json[story_versions_codes[i]] = master_json[key][story_versions[i]]

            extracted_dict[key] = inside_json

    return extracted_dict

# we need to run this file for all langpairs next.
# then, we run filter_unequal_stories.py on the outputs.
# for any n-tuple defined here.
with open('../../data/parallel/raw/stats.txt', 'w') as fp:
    pass

isocode_values_list = list(isocode_values)
iso_combinations = list(combinations(isocode_values_list, 2))
for queries in iso_combinations:
    extracted = extract(queries, keys, iso_keys, isocodes)
    keys_current = extracted.keys()
    num_stories = len(keys_current)
    if num_stories > 0:
        with open(f'../../data/parallel/raw/{queries[0]}-{queries[1]}.json', 'w') as f:
            json.dump(extracted, f)

        with open('../../data/parallel/raw/stats.txt', 'a') as fp:
            fp.write(str(queries))
            fp.write("\t"+ str(num_stories))
            fp.write("\n")
