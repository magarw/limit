# This file opens a connection to storyweaver and downloads the name of all the available languages on the website.
import requests
import json

OUTPUT_PATH = "../../../data/raw/pratham-books-storyweaver/"

with open(OUTPUT_PATH + "languages.txt", 'r') as f:
    languages = [x.strip() for x in f.readlines()]
print("Num langs: ", len(languages))

for lang in languages:
    URL2 = f"https://storyweaver.org.in/api/v1/books-search?languages[]={lang}&page=1&per_page=1"
    while True:
        response = requests.get(URL2)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            total_books = json_response['metadata']['hits']
            with open(OUTPUT_PATH + "languages_story_counts.txt", 'a') as f2:
                f2.write(f"{lang}\t{total_books}\n")
            break
