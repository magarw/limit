import json
import os
from iso639 import Lang

INPUT_PATH = '../../data/language-id/monolingual_combined/'

filenames = os.listdir(INPUT_PATH)

count = []

for f in filenames:
    if ".txt" in f:
        file = open(INPUT_PATH + f)
        num_lines = len(file.readlines())
        lang_name = f.split('.')[0]
        count.append((lang_name, num_lines))
count.sort(key = lambda x: x[1], reverse=True)

for v in count:
    code = v[0]
    count_ = v[1]
    try:
        name = Lang(code).name
    except:
        name = code
    print(code, "\t", count_, "\t", name)
