import os
from os.path import exists
import json
import pandas as pd

INPUT_PATH = '../../data/merged/cutoff-1/'
file_names = [x for x in os.listdir(INPUT_PATH) if '.json' in x]

print("Total: ", len(file_names), "stories")

def create_monolingual_data():
    i = 0
    for file_name in file_names:
        file_json = json.load(open(INPUT_PATH + file_name))
        if len(file_json['related_versions']) == 0:
            i = i + 1
            with open('../../data/monolingual/' + file_json['language'] + '.json', 'a') as f:
                for p in file_json['pages']:
                    f.write(p.replace('\n', ' ') + '\n')
    return i

num_monolingual_stories = create_monolingual_data()
print("Extracted monolingual data from ", num_monolingual_stories, " stories out of ", len(file_names))
