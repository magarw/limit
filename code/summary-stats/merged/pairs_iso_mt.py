import json
path = "../../../data/parallel/filtered_lengths/filtered500.txt"
isopath = "../../../data/parallel/isocodes.json"

isocodes = json.load(open(isopath))
data = [eval(x.split('\t')[0]) for x in open(path).readlines()]
overall_string = ""
passed = 0
for d in data:
    try:
        overall_string += f"{isocodes[d[0]]}-{isocodes[d[1]]}\n"
    except:
        passed += 1
        pass
with open("../../../data/parallel/mt_pairs_for_comparison.txt", "w") as fp:
    fp.write(overall_string)
print(f"Passed on {passed}/{len(data)}") #671/3569
