import json
import requests
import os
from os.path import exists
import matplotlib.pyplot as plt

#
CUTOFF = 50 # > CUTOFF characters
# About half the stories have more than 1000 characters.

# paths and constants
INPUT_PATH = "../../../data/clean/african-storybooks-initiative/verified/"
OUTPUT_PATH = "../../../data/clean/african-storybooks-initiative/non-sparse/"
CONTENT_PATH = "../../../data/clean/african-storybooks-initiative/content_length.json"

verified_file_names = [x for x in os.listdir(INPUT_PATH) if '.json' in x]
print(len(verified_file_names), "stories to start with.")

# saves book lengths if not there already.
if not exists(CONTENT_PATH):
    content_length = {}
    for file_name in verified_file_names:
        file_json = json.load(open(INPUT_PATH + file_name))
        file_text = "".join([x["text"].strip() for x in file_json["pages"]])
        content_length[file_name.split(".json")[0]] = len(file_text)

    with open(CONTENT_PATH, "w") as f:
        json.dump(content_length, f)
else:
    content_length = json.load(open(CONTENT_PATH))

# Plotting some visual of length (# of words  per book) distribution
plt.plot(sorted(content_length.values()))
plt.savefig("../../../data/clean/african-storybooks-initiative/content_length_distribution.png")
plt.clf()

plt.hist(content_length.values(), bins='auto', color='#0504aa')
plt.savefig("../../../data/clean/african-storybooks-initiative/content_length_histogram.png")
plt.clf()

# Filtering Code
i = 0
for key in content_length.keys():
    if content_length[key] > CUTOFF:
        i = i + 1
        data = json.load(open(INPUT_PATH + key + ".json"))
        if not exists(f"{OUTPUT_PATH}cutoff-{CUTOFF}/"):
            os.mkdir( f"{OUTPUT_PATH}cutoff-{CUTOFF}/")
        with open(f"{OUTPUT_PATH}cutoff-{CUTOFF}/{key}.json", "w") as f:
            json.dump(data, f)

print(i, f"stories remain at cutoff {CUTOFF}. {len(verified_file_names) - i} files didn't qualify")





#
