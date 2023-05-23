import json
import time
import os

INPUT_PATH = '../../data/parallel/new_master.json'
master_json = json.load(open(INPUT_PATH))
keys = master_json.keys()
langset = set()

whitelist = ["Cebuano-Cebu", "Runyoro-Rutooro"]
for key in keys:
    for l in master_json[key].keys():
        if '-' in l and l not in whitelist:
            langset.add(l.split('-')[0])
            langset.add(l.split('-')[1])
        else:
            langset.add(l)

with open('../../data/language-id/new_languages.txt','w') as fp:
    for l in langset:
        fp.write(l + '\n')

# Note: If a '-' is present in the language name, it is a bilingual document.
# But, I will need to go through all the languages and check for bilingual names myself.
