import json
import time
import os
import nltk
from itertools import combinations
import sys
INPUT_PATH = '../../../data/parallel/master.json'
from collections import Counter

lang_dashed = {}

# Provides a rough estimate of number of pages per language pair.

master_json = json.load(open(INPUT_PATH))
story_keys = master_json.keys()

for key in story_keys:
    # for a particular story.
    flag = False
    langs = list(master_json[key].keys())
    story_length = len(master_json[key][langs[0]])
    for l in langs:
        if '-' in l:
            flag = True
            if str(l) in lang_dashed.keys():
                lang_dashed[str(l)] += story_length
            else:
                lang_dashed[str(l)] = story_length

lang_dashed_list = sorted(lang_dashed.items(), key=lambda x:x[1])

# Now, we need to know how many of these have parallel translation in either language available.
# If both are available, then we will delete this entry, because we have a better translation direction.
total_either = 0
total_both = 0
total = 0
for l_dashed in lang_dashed_list:
    lang = l_dashed[0]
    count = l_dashed[1]

    L1 = lang.split('-')[0]
    L2 = lang.split('-')[1]

    #print(lang)
    #print(count)
    yes_l1 = 0
    yes_l2 = 0
    yes_either = 0
    yes_both = 0

    for key in story_keys:
        langs = list(master_json[key].keys())
        story_length = len(master_json[key][langs[0]])
        if lang in langs:
            total += story_length
            # if L1 in langs:
            #     yes_l1 += story_length
            #
            # if L2 in langs:
            #     yes_l2 += story_length

            if (L1 in langs and L2 not in langs) or (L2 in langs and L1 not in langs):
                total_either += story_length
                yes_either += story_length

            if L1 in langs and L2 in langs:
                yes_both += story_length
                total_both += story_length

        else:
            continue

    print(lang, count, yes_either, yes_both)

print("TOTALS")
print(f"total: {total}, total_either: {total_either}, total_both: {total_both}")

with open("../../../data/parallel/multilingual.txt", 'w') as fp:
    for entry in lang_dashed_list:
        fp.write(str(entry))
        # fp.write("\t")
        # fp.write(str(lang_dashed[key]))
        fp.write("\n")
