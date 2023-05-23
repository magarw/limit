import json
import os

json_files = os.listdir('../../data/parallel/multilingual/')
INPUT_PATH = '../../data/parallel/master.json'
OUTPUT_PATH = '../../data/parallel/new_master.json'

master_json = json.load(open(INPUT_PATH))
for f in json_files[:2]:
    if 'json' in f:
        f_lang = f.replace('.json','')
        # For first run: master_json = json.load(open('../../data/parallel/master.json'))
        extract_json = json.load(open(f'../../data/parallel/multilingual/{f}'))

        for key in extract_json['data']:
            extract_langs = list(extract_json['data'][key].keys())

            if len(extract_langs) == 1:
                master_langs = master_json[key].keys()
                lang_key = extract_langs[0]# new language
                if lang_key not in master_langs:
                    master_json[key][lang_key] = extract_json['data'][key][lang_key]

            # we also want to remove the sample_language
            if f_lang in master_langs:
                del master_json[key][f_lang]

        # temporary dump (in case we lose progress)
        with open(OUTPUT_PATH, 'w') as fp:
            json.dump(master_json, fp)

        print(f"Completed merging for: {f}")
        print(master_json[key])
