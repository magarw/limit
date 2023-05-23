import json
import requests
import os
from os.path import exists

cutoffs = [1, 50, 100, 500, 1000]
for cutoff in cutoffs:
    print("Cutoff: ", cutoff)
    INPUT_PATH = f"../../../data/clean/african-storybooks-initiative/eng-mismatch-removed/candidate_removals_cutoff{cutoff}.txt"
    print("Script to remove stories with excessive English in a non-English stories.")

    lines = open(INPUT_PATH).readlines()

    blacklist_names = []
    for line in lines:
        name = line.split(';')[1].strip().split("File: ")[1]
        blacklist_names.append(name)

    blacklist = set(blacklist_names)
    print(len(blacklist), " files to remove/blacklist.")
    base_files = set(os.listdir(f"../../../data/clean/african-storybooks-initiative/non-sparse/cutoff-{cutoff}"))
    filtered_files = base_files.difference(blacklist)
    print(len(filtered_files), " files filtered.")


    for file in filtered_files:
        name_json = json.load(open(f"../../../data/clean/african-storybooks-initiative/non-sparse/cutoff-{cutoff}/{file}"))
        with open(f"../../../data/clean/african-storybooks-initiative/eng-mismatch-removed/cutoff-{cutoff}/{file}", "w") as f:
            json.dump(name_json, f)
























#
