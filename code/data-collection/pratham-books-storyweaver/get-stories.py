
from bs4 import BeautifulSoup
import json
import os
import requests
import multiprocessing
import time

def fetch_book(pair):
    BOOK_URL, threadNo = pair[0], pair[1]
    OUTPUT_PATH ="../../../data/raw/pratham-books-storyweaver/"
    try:
        response = requests.get(BOOK_URL)
        response_json = json.loads(response.text)

        book_json = {}
        book_json['language'] = response_json['data']['language']
        book_json['isLanguageRtl'] = response_json['data']['isLanguageRtl'] if 'isLanguageRtl' in response_json['data'].keys() else "false"
        book_json['isAudio'] = response_json['data']['isAudio'] if 'isAudio' in response_json['data'].keys() else "false"
        book_json['isTranslation'] = response_json['data']['isTranslation'] if 'isTranslation' in response_json['data'].keys() else "false"
        book_json['authors'] = response_json['data']['authors'] if 'authors' in response_json['data'].keys() else "false"
        book_json['level'] = response_json['data']['level'] if 'level' in response_json['data'].keys() else "false"
        book_json['identifier'] = response_json['data']['slug']
        num_pages = len(response_json['data']['pages'])
        book_json['num_pages'] = num_pages
        book_json['pages'] = []
        for i in range(0, num_pages):
            pageNo = response_json['data']['pages'][i]['pagePostion']
            soup = BeautifulSoup(response_json['data']['pages'][i]['html'], 'html.parser')
            pageText = soup.find('div', {'class': 'content'})
            if pageText != None:
                pageText = pageText.text.strip()
            else:
                pageText = "-"
            book_json['pages'].append(pageText)
            if response_json['data']['pages'][i]['isLastStoryPage']:
                break

        TRANS_URL = f"https://storyweaver.org.in/api/v1/stories/{book_json['identifier']}/translations_and_videos"
        response = requests.get(TRANS_URL)
        print(TRANS_URL)
        response_json = json.loads(response.text)
        book_json['translations'] = {'versions':response_json['data']['versionCount'], 'languageCount': response_json['data']['languageCount'],
                                    'parallelTranslations': response_json['data']['translations']}

        with open(OUTPUT_PATH + 'stories/' + book_json['identifier']+ ".json", 'w') as f:
            json.dump(book_json , f)

        return True

    except Exception as e:
        print(e)
        # time.sleep(1)
        # with open(f"{OUTPUT_PATH}logs/thread{threadNo}.log", 'a') as f:
        #     f.write("EXCEPTION: " + BOOK_URL + "\t" + "\n")
        return False


if __name__ == '__main__':

    OUTPUT_PATH = "../../../data/raw/pratham-books-storyweaver/"
    final_urls = sorted(os.listdir(OUTPUT_PATH + "endpoints"))
    print(len(final_urls))

    stories = os.listdir(OUTPUT_PATH + "stories")
    stories = [story.split(".json")[0] for story in stories]
    print(len(stories))

    print(stories[0])

    threadNo = 0
    bookSlugs = []
    for lang_path in final_urls:
        if '.json' in lang_path: # allows us to ignore any other temporary files that the system may have created.
            JSON_FILE = json.load(open(OUTPUT_PATH + "endpoints/" + lang_path, 'r'))
            for key in JSON_FILE.keys():
                book_entry = JSON_FILE[key]
                bookSlugs.append(book_entry['slug'])
                #
                # if book_entry['slug'] not in stories:
                #     BOOK_URL = f"https://storyweaver.org.in/api/v1/stories/{book_entry['slug']}/read?&ignore_count=false&source="
                #     arguments.append([BOOK_URL, threadNo, lang_path])
                #     threadNo += 1

    print(len(bookSlugs))
    difference = set(bookSlugs).difference(set(stories))
    print("Difference", len(difference))

    i = 0
    arguments = []
    for entry in difference:
        BOOK_URL = f"https://storyweaver.org.in/api/v1/stories/{entry}"
        arguments.append([BOOK_URL, i])
        i = i + 1
    print("Argument Length", len(arguments))

    for arg in arguments:
        print(arg)
        fetch_book(arg)


    #create a process pool that uses all cpus, and automatically closes.
    # with multiprocessing.Pool() as pool:
    #     # call the function for each item in parallel with multiple arguments
    #     for result in pool.map(fetch_book, arguments):
    #         print(result)
