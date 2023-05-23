import json
import time
import os
import nltk

INPUT_PATH = '../../../data/parallel/uneq-pgs-removed/'

filenames = os.listdir(INPUT_PATH)
lang_pairs = {}

for file in filenames:
    if 'json' in file and 'master' not in file:
        master_json = json.load(open(INPUT_PATH + file))
        keys = master_json.keys()
        #print(f"Found { len(keys)} stories in {file}")
        # sent_count = {}
        entry_count = {}
        for key in keys:
            for lang in master_json[key].keys():
                if lang not in sent_count.keys():
                    sent_count[lang] = 0
                if lang not in entry_count.keys():
                    entry_count[lang] = 0

                entries = master_json[key][lang]
                entry_count[lang] += len(entries)

                # for entry in entries:
                #     sent_count[lang] += len(nltk.sent_tokenize(entry))

        # x = ""
        # for key in sent_count:
        #     x += f"{key}: {sent_count[key]}, "
        # if len(x) > 1:
        #     print(x[:-2] + " (sentences)")
        x = ""
        for key in entry_count:
            x += f"{key}: {entry_count[key]}, "
        if len(x) > 1:
            print(x[:-2] + " (entries)\n")
