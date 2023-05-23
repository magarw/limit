import json
import time
import os
import nltk
from itertools import combinations
import sys
INPUT_PATH = '../../../data/parallel/master.json'
from collections import Counter

lang_pairs = {}

# Provides a rough estimate of number of pages per language pair.

master_json = json.load(open(INPUT_PATH))
story_keys = master_json.keys()

for key in story_keys:
    # for a particular story.
    langs = list(master_json[key].keys())
    lang_combinations = list(combinations(langs, 2))

    filtered_combinations = []
    whitelist = ['Gascon']
    for pair in lang_combinations:
        if pair[0] in whitelist or pair[1] in whitelist:
            filtered_combinations.append(pair)

    num_pages = len(master_json[key][langs[0]])
    # for pair in lang_combinations:
    for pair in filtered_combinations:

        flip_pair = (pair[1], pair[0])
        current_keys = lang_pairs.keys()
        if pair not in current_keys and flip_pair not in current_keys:
            lang_pairs[pair] = 0
            lang_pairs[pair] += num_pages
            continue

        if pair in current_keys:
            lang_pairs[pair] += num_pages
        elif flip_pair in current_keys:
            lang_pairs[flip_pair] += num_pages

# x = input("Print or exit?")
# if x == "exit":
#     sys.exit("Stopping due to admin halt.")

with open("../../../data/parallel/pair_lengths_filtered.txt", 'w') as fp:
    for key in lang_pairs:
        fp.write(str(key))
        fp.write("\t")
        fp.write(str(lang_pairs[key]))
        fp.write("\n")
