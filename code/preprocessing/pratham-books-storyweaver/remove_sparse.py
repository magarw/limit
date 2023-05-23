import json
import requests
import os
from os.path import exists
import matplotlib.pyplot as plt

#
CUTOFF = 1 # > CUTOFF characters
# About half the stories have more than 1000 characters.

# paths and constants
INPUT_PATH = "../../../data/clean/pratham-books-storyweaver/verified/"
OUTPUT_PATH = "../../../data/clean/pratham-books-storyweaver/non-sparse/"
CONTENT_PATH = "../../../data/clean/pratham-books-storyweaver/content_length.json"
EMPTY_PATH = "../../../data/clean/pratham-books-storyweaver/sparse.json"

verified_file_names = [x for x in os.listdir(INPUT_PATH) if '.json' in x]
print(len(verified_file_names), "stories to start with.")

# saves book lengths if not there already.
if not exists(CONTENT_PATH) or not exists(EMPTY_PATH):
    content_length = {}
    empty_books = {}
    for file_name in verified_file_names:
        file_json = json.load(open(INPUT_PATH + file_name))

        if len(file_json["pages"]) > 0 and isinstance(file_json["pages"][0], list):
            page_lengths = [len(x[1].strip()) for x in file_json["pages"]]
            file_text = "".join([x[1].strip() for x in file_json["pages"]])
            if page_lengths.count(0) > len(page_lengths)/2:
                print("more than half the pages empty: ", file_name)
                empty_books[file_name.split(".json")[0]] = page_lengths.count(0)

        elif len(file_json["pages"]) > 0 and isinstance(file_json["pages"][0], str):
            page_lengths = [len(x.strip()) for x in file_json["pages"]]
            file_text = "".join([x.strip() for x in file_json["pages"]])
            if page_lengths.count(0) > len(page_lengths)/2:
                print("more than half the pages empty: ", file_name)
                empty_books[file_name.split(".json")[0]] = page_lengths.count(0)

        content_length[file_name.split(".json")[0]] = len(file_text)

    with open(CONTENT_PATH, "w") as f:
        json.dump(content_length, f)

    with open(EMPTY_PATH, "w") as f:
        json.dump(empty_books, f)

else:
    content_length = json.load(open(CONTENT_PATH))
    empty_books = json.load(open(EMPTY_PATH))

# Plotting some visual of length (# of words  per book) distribution
plt.plot(sorted(content_length.values()))
plt.savefig("../../../data/clean/pratham-books-storyweaver/content_length_distribution.png")
plt.clf()

plt.hist(content_length.values(), bins='auto', color='#0504aa')
plt.savefig("../../../data/clean/pratham-books-storyweaver/content_length_histogram.png")
plt.clf()

print("Fraction of books with more than 50% empty pages: ", len(empty_books.keys()), len(verified_file_names))
# Filtering Code

if not exists(f"{OUTPUT_PATH}empty-books-removed/"):
    os.mkdir( f"{OUTPUT_PATH}empty-books-removed/")

    content_length_set = set(content_length.keys())
    empty_books_set = set(empty_books.keys())
    non_empty_pages = content_length_set.difference(empty_books_set)
    i = 0

    for key in non_empty_pages:
        i = i + 1
        data = json.load(open(INPUT_PATH + key + ".json"))

        if len(data["pages"]) > 0 and isinstance(data["pages"][0], list):
            new_data = []
            for p in data["pages"]:
                new_data.append(p[1]) # ignore page number.
            data["pages"] = new_data

        with open(f"{OUTPUT_PATH}empty-books-removed/{key}.json", "w") as f:
            json.dump(data, f)

    print(i, f"stories saved with majority non-empty pages . {len(verified_file_names) - i} files didn't qualify/were filtered out.")


# paths and constants
INPUT_PATH = "../../../data/clean/pratham-books-storyweaver/non-sparse/empty-books-removed/"
OUTPUT_PATH = "../../../data/clean/pratham-books-storyweaver/non-sparse/"
CONTENT_PATH = "../../../data/clean/pratham-books-storyweaver/content_length.json"


if not exists(f"{OUTPUT_PATH}cutoff-{CUTOFF}/"):
    os.mkdir( f"{OUTPUT_PATH}cutoff-{CUTOFF}/")
i = 0
for key in content_length.keys():
    if key not in empty_books.keys() and content_length[key] > CUTOFF:
        i = i + 1
        data = json.load(open(INPUT_PATH + key + ".json"))
        with open(f"{OUTPUT_PATH}cutoff-{CUTOFF}/{key}.json", "w") as f:
            json.dump(data, f)

print(i, f"stories remain at cutoff {CUTOFF}. {len(content_length.keys()) - len(empty_books.keys()) - i} files didn't qualify")





#
