import json
import os
import nltk

INPUT_PATH = "../../../data/parallel/raw/"
files = os.listdir(INPUT_PATH)
total = len(files) - 1
with open("../../../data/parallel/uneq-pgs-removed/stats.txt", "w") as fp:
    pass

progress = 0
for f in files:
    if 'json' in f:
        progress += 1

        if progress % 100 == 0:
            print(f"{progress*100/total:.2f}%")

        pair_json = json.load(open(INPUT_PATH + f))
        keys = pair_json.keys()
        total_stories = len(keys)
        unequal_stories = 0
        saved = 0

        new_json = {}
        for key in keys:
            langs = pair_json[key].keys() # to get languages
            lengths = []
            for l in langs:
                lengths.append(len(pair_json[key][l]))
            if lengths.count(lengths[0]) != len(lengths):
                unequal_stories += 1
                continue
            else:
                new_json[key] = pair_json[key]
                saved +=1
        if len(new_json.keys()) != 0:
            with open("../../../data/parallel/uneq-pgs-removed/" + f, 'w') as fp:
                json.dump(new_json, fp)

        with open("../../../data/parallel/uneq-pgs-removed/stats.txt", "a") as fp:
            fp.write(f"{f}\t{total_stories}\t{saved}\t{unequal_stories}\t{unequal_stories*100/total_stories:.2f}%\n")

        # print(f"File: {f}, Initial: {total_stories}, Remain: {saved}, Removed: {unequal_stories} ({unequal_stories*100/total_stories:.2f}%)")





















#
