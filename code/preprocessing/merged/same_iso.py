import json

INPUT_PATH = '../../../data/parallel/isocodes.json'

isocodes = json.load(open(INPUT_PATH))
values = {}
for key in isocodes.keys():
    ix = isocodes[key]
    if ix not in values.keys():
        values[ix] =[ key ]
    else:
        values[ix].append(key)
for v in values.keys():
    if len(values[v]) > 1:
        print(v, values[v])
print(len(values.keys()))
