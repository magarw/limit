import os
from os.path import exists
import json
import pandas as pd

INPUT_PATH = '../../data/merged/cutoff-1/'
file_names = [x for x in os.listdir(INPUT_PATH) if '.json' in x]

print("Total: ", len(file_names), "stories")

# Take a story (input). Produce a parallel text database (from all of its related-versions)
def get_parallel_text(BASE_STORY):
    #print("Base story: ", BASE_STORY)

    base_story_json = json.load(open(INPUT_PATH + BASE_STORY))
    base_lang = base_story_json['language']
    data_feed = {base_lang: base_story_json['pages']}

    seen = []

    for version in base_story_json['related_versions']:
        if exists(INPUT_PATH + version['id'] + ".json"):
            seen.append(version['id'])
            side_story_json = json.load(open(INPUT_PATH + version['id'] + ".json"))
            side_text = side_story_json['pages']
            side_lang = side_story_json['language']
            data_feed[side_lang] = side_text

    return data_feed, seen

def check(num):
    i = 0
    for file_name in file_names:
        file_json = json.load(open(INPUT_PATH + file_name))
        if len(file_json['related_versions']) == num:
            i = i + 1
    return i

def check_all():
    count = {}
    for file_name in file_names:
        file_json = json.load(open(INPUT_PATH + file_name))
        try:
            count[len(file_json['related_versions'])] += 1
        except:
            count[len(file_json['related_versions'])] = 1

    return count

def langs():
    lang_set = set()
    for file_name in file_names:
        file_json = json.load(open(INPUT_PATH + file_name))
        lang_set.add(file_json['language'])
    return lang_set

# I think we need to make a master dataset, from which we can then filter out different datasets based on need
# i.e. for a subset of languages (ex. parallel texts, 3 langs etc.)
# For this, we would need to know the master set of languages first.

#languages = langs()
#print(len(languages), " total languages found (might contain repeats. pre-filtering)")

def create_master_json():
    master_json = {}
    i = 0
    j = 0
    master_seen = set()
    for name in file_names:
        print(i, '/', j)
        j = j + 1
        if name not in master_seen:
            json_parallel, seen = get_parallel_text(name)
            master_json[i] = json_parallel
            i = i + 1

            for s in seen:
                master_seen.add(s + '.json')

    with open('../../data/parallel/master.json', 'w') as fp:
        json.dump(master_json, fp)

create_master_json()


"""
            English       French     Hindi
Pg 1        sjkfbsjbf        -       main hoon na
Pg 2
Pg 3        fsrwfvbre     rfwergh      -
.
.
"""

# count_dict = check_all()

# for k in sorted(list(count_dict.keys())):
#     ans = count_dict[k]
#     if k != 0:
#         print(k, "-parallel: ", ans//k, " unique stories with ", ans, " total files/version")
#     else:
#         print(k, "-parallel: ", ans, " unique stories with ", ans, " total files/version")

# for entry in data_feed:
#     with open('../../data/aligned/' + entry[0] + '.dev', 'w') as f:
#         for item in entry[1:]:
#             f.write(item.replace("\n", " ") + "\n")
