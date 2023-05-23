
import requests
import json

OUTPUT_PATH = "../../../data/raw/pratham-books-storyweaver/"

with open(OUTPUT_PATH + "languages_story_counts.txt", 'r') as f:
    languages = [x.strip().split("\t") for x in f.readlines()]

for pair in languages:
    lang_name = pair[0]
    lang_total = int(pair[1])
    output = {}
    if lang_total <= 5000:
        continue
        URL = f"https://storyweaver.org.in/api/v1/books-search?languages[]={lang_name}&page=1&per_page=5000"
        response = requests.get(URL)
        if response.status_code == 200:
            json_response = json.loads(response.text)["data"]
            for i in range(len(json_response)):
                output[i] = {
                'id': json_response[i]['id'],
                'title': json_response[i]['title'],
                'slug': json_response[i]['slug'],
                'language': json_response[i]['language'].replace('/', '-'),
                'level': json_response[i]['level']
                }
        if '/' in lang_name:
            with open(OUTPUT_PATH + "transformations.log", 'a') as f:
                f.write(lang_name + ";" + lang_name.replace('/', '-') + "\n")
                lang_name = lang_name.replace('/', '-')

        with open(OUTPUT_PATH +"endpoints/" + lang_name + ".json", 'w') as f:
            json.dump(output , f)


    else:
        print(pair)
        f = open(OUTPUT_PATH +"endpoints/" + lang_name + ".json", 'w')
        f.close()

        # English's 12265 stories.
        last = 0
        for level in range(1, 6):
            print("pinging level", level)
            URL = f"https://storyweaver.org.in/api/v1/books-search?languages[]={lang_name}&levels[]={level}&page=1&per_page=5000&sort=Most%20Read"
            response = requests.get(URL)
            if response.status_code == 200:
                json_response = json.loads(response.text)["data"]
                for i in range(len(json_response)):
                    if 'level' in json_response[i].keys():
                        output[last + i] = {
                        'id': json_response[i]['id'],
                        'title': json_response[i]['title'],
                        'slug': json_response[i]['slug'],
                        'language': json_response[i]['language'].replace('/', '-'),
                        'level': json_response[i]['level']
                        }
                last += len(json_response)

        with open(OUTPUT_PATH +"endpoints/" + lang_name + ".json", 'a') as f:
            json.dump(output , f)
