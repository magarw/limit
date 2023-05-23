import json
import os
CUTOFF=1

OUTPUT_PATH = f"../../data/merged/cutoff-{CUTOFF}/"

AFRICAN_BASE_PATH = f"../../data/clean/african-storybooks-initiative/eng-mismatch-removed/cutoff-{CUTOFF}/"
PRATHAM_BASE_PATH = f"../../data/clean/pratham-books-storyweaver/eng-mismatch-removed/cutoff-{CUTOFF}/"

african_base_names = [x for x in os.listdir(AFRICAN_BASE_PATH) if '.json' in x]
pratham_base_names = [x for x in os.listdir(PRATHAM_BASE_PATH) if '.json' in x]

print("\nPre-Merge")
print("# African files: ", len(african_base_names))
print("# Pratham files: ", len(pratham_base_names))

print("\nMerging. Step 1: Key-Value Pair Consistency")
for african_file in african_base_names:
    african_json = json.load(open(AFRICAN_BASE_PATH + african_file))
    african_new_json = {}

    african_new_json['id'] = african_json['id']
    african_new_json['author'] = african_json['author']
    african_new_json['translator'] = african_json['translation']
    african_new_json['illustrator'] = african_json['illustration']

    african_new_json['level'] = african_json['level']
    african_new_json['verified'] = african_json['verified']
    african_new_json['copyright'] = african_json['copyright']

    african_new_json['language'] = african_json['language']

    african_new_json['pages'] = [x['text'] for x in african_json['pages']]

    entries_modified = []
    for entry in african_json['related_versions']:
        entry_modified = {}
        entry_modified['id']  = entry['id']
        entry_modified['language'] = entry['lang'].replace("(Translation)", "").replace("(Adaptation)","").replace("(Original)", "").strip()
        entry_modified['title'] = entry['title']
        if entry['translation']:
            entry_modified['type'] = "Translation"
        elif entry['adaptation']:
            entry_modified['type'] = "Adaptation"
        elif entry['original']:
            entry_modified['type'] = "Original"

        entries_modified.append(entry_modified)
    african_new_json['related_versions'] = entries_modified
    african_new_json['source'] = 'african-storybooks-initiative'
    with open(OUTPUT_PATH + african_file, "w") as f:
        json.dump(african_new_json, f)

for pratham_file in pratham_base_names:
    pratham_json = json.load(open(PRATHAM_BASE_PATH + pratham_file))
    pratham_new_json = {}

    pratham_new_json['id'] = pratham_json['identifier']

    first_page = pratham_json['pages'][0]
    if 'Author:' in first_page:
        trim = first_page.split("Author:")[1]
        if 'Illustrator' in trim:
            pratham_new_json['author'] = trim.split("Illustrator")[0].strip()
        elif 'Translator' in trim:
            pratham_new_json['author'] = trim.split("Translator")[0].strip()
        else:
            pratham_new_json['author'] = trim.strip()
    else:
        pratham_new_json['author'] = ""

    if 'Translator:' in first_page:
        trim = first_page.split("Translator:")[1]
        if 'Illustrator' in trim:
            pratham_new_json['translator'] = trim.split("Illustrator")[0].strip()
        elif 'Author' in trim:
            pratham_new_json['translator'] = trim.split("Author")[0].strip()
        else:
            pratham_new_json['translator'] = trim.strip()
    else:
        pratham_new_json['translator'] = ""

    if 'Illustrator:' in first_page:
        trim = first_page.split("Illustrator:")[1]
        if 'Translator' in trim:
            pratham_new_json['illustrator'] = trim.split("Translator")[0].strip()
        elif 'Author' in trim:
            pratham_new_json['illustrator'] = trim.split("Author")[0].strip()
        else:
            pratham_new_json['illustrator'] = trim.strip()
    else:
        pratham_new_json['illustrator'] = ""

    pratham_new_json['level'] = pratham_json['level']
    pratham_new_json['verified'] = pratham_json['verified']
    pratham_new_json['copyright'] = "Refer to author, translator, illustrator information."

    pratham_new_json['language'] = pratham_json['language']
    pratham_new_json['pages'] = pratham_json['pages'][1:] # remove the first page with title, author, illustrator, translator info since its already been preserved/extracted.

    entries_modified = []
    for entry in pratham_json['translations']['parallelTranslations']:
        entry_modified = {}
        entry_modified['id'] =  entry['slug']
        entry_modified['language'] = entry['language']
        entry_modified['title'] = entry['title']
        entry_modified['type'] = 'Translation'
        entries_modified.append(entry_modified)

    pratham_new_json['related_versions'] = entries_modified

    pratham_new_json['source'] = 'pratham-storybooks-initiative'
    with open(OUTPUT_PATH + pratham_file, "w") as f:
        json.dump(pratham_new_json, f)

print("\nMerge Complete. Key-Value Pairs are now consistent. Located in merged/cutoff-1")

print("\n\n")
















#
