import json

ISO_PATH = "../../data/parallel/isocodes_lid.json"
isocodes = json.load(open(ISO_PATH))
iso_keys = list(isocodes.keys())

isocode_values = set()
for key in isocodes:
    isocode_values.add(isocodes[key])

for k in sorted(iso_keys):
    str = f"{isocodes[k]} & {k} \\\\ "
    print(str)
