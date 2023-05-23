import json
import requests
import os
import multiprocessing

def task(filename):
    try:
        RAW_PATH = "../../../data/raw/pratham-books-storyweaver/stories/"
        OUTPUT_PATH = "../../../data/clean/pratham-books-storyweaver/"
        file_name_slug = filename.split(".json")[0]

        URL = f"https://storyweaver.org.in/api/v1/stories/{file_name_slug}/read?&ignore_count=false&source="
        response = requests.get(URL)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            verification_status = json_response["data"]["recommended"]
            if verification_status == True:
                verification = 1
            else:
                verification = 0

        raw_file = json.load(open(RAW_PATH + filename))
        raw_file['verified'] = f"{verification}"

        with open(OUTPUT_PATH + filename, 'w') as f:
            json.dump(raw_file, f)

        return True
    except:
        return False

if __name__ == '__main__':

    RAW_PATH = "../../../data/raw/pratham-books-storyweaver/stories/"
    OUTPUT_PATH = "../../../data/clean/pratham-books-storyweaver/"

    filenames = [x for x in os.listdir(RAW_PATH) if 'json' in x] # to remove DS JSON file, if there.
    length = len(filenames)
    print("Total raw: ", length)

    already_done = set([x for x in os.listdir(OUTPUT_PATH) if 'json' in x]) # to remove DS JSON file, if there.
    print("Already done: ", len(already_done))
    filenames_set = set(filenames)
    filenames = list(filenames_set.difference(already_done))
    print("Remaining: ", len(filenames))

    # create a process pool that uses all cpus, and automatically closes.
    with multiprocessing.Pool() as pool:
        # call the function for each item in parallel with multiple arguments
        for result in pool.map(task, filenames, chunksize=1000):
            print(result)


















#
