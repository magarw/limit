import json
import requests
import os
php_path = "../../../data/raw/african-storybooks-initiative/booklistjs.php"
OUTPUT_PATH = "../../../data/clean/african-storybooks-initiative/"
RAW_PATH = "../../../data/raw/african-storybooks-initiative/"

response = open(php_path)
lines = response.readlines()
verified = {}
for line in lines[:-2]:
    verified[line.split("id:")[1].split(",title:")[0]] = line.split("approved:")[1].split(",other:")[0]
with open(OUTPUT_PATH + "verified.json", "w") as f:
    json.dump(verified, f)
verified = json.load(open(OUTPUT_PATH + "verified.json"))

book_names_list = [x for x in os.listdir(RAW_PATH) if '.json' in x]

for book_name in book_names_list:
    book_json = json.load(open(RAW_PATH + book_name))
    book_json["verified"] = verified[f"\"{book_name.split('.json')[0]}\""][1]
    with open(OUTPUT_PATH + "verified/" + book_name, 'w') as f:
        json.dump(book_json, f)

print(len(os.listdir(OUTPUT_PATH + "verified/")), " stories in clean.")
















#
