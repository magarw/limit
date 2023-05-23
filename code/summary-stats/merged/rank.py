import json
import os

# INPUT_PATH = "../../../data/parallel/uneq-pgs-removed/"
INPUT_PATH = "../../../data/parallel/wmt-pairs/all/"
files = os.listdir(INPUT_PATH)

# OUTPUT_PATH = "../../../data/parallel/stats_uneq_pgs_removed.txt"

SAVE_PATH = "../../../data/parallel/wmt-pairs/filtered-500/"

counts = []
focus = ["eng", "fra"]
whitelist = ["afr", "lin", "amh", "lug", "ssw", "nya", "luo", "umb", "fuv", "nso",
            "wol", "hau", "orm", "xho", "ibo", "tso", "kam", "som", "yor", "kin",
             "swh","swa", "zul", "eng", "fra"]
# whitelist = ["afr", "ssw", "nso", "xho",  "tso",  "tsn", "zul"]
# whitelist = [ "amh",  "luo", "orm", "som","swa"]
# whitelist = [ "ful",  "hau", "ibo", "yor"]
# whitelist = [ "nya",  "kin", "lin", "lug", "swa"]

total = len(files)
progress = 0
for f in files:
    if 'json' in f:
        progress += 1
        if progress % 100 == 0:
            print(f"{progress*100/total}%", end="\r")
        cur_json = json.load(open(INPUT_PATH + f))
        l1, l2 = f.replace(".json", "").split("-")
        if l1 in whitelist and l2 in whitelist:
            story_ids = cur_json.keys()
            count = [f, 0]
            for story_id in story_ids:
                count[1] += len(cur_json[story_id][l1])
            counts.append(count)

            if count[1] > 500:
                with open(SAVE_PATH + f, 'w') as fp:
                    json.dump(cur_json, fp)


print("\n")
# counts.sort(key = lambda x: x[1], reverse=True)
# with open(OUTPUT_PATH, 'w') as fp:
#     for x in counts:
#         fp.write( str(x[0].replace(".json", "")) + "\t" + str(x[1]) + "\n")
#
# #
