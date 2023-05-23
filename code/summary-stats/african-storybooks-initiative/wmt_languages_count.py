import json
import os
from os.path import exists
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

WMT_LANGUAGES_ENG = ["Afrikaans", "Amharic", "Chichewa", "Nigerian Fulfulde", "Hausa",
                 "Igbo", "Kamba", "Kinyarwanda", "Luganda", "Luo", "Northern Sotho",
                 "Oromo", "Shona", "Somali", "Swahili", "Swati", "Tswana", "Umbundu",
                 "Xhosa", "Xitsonga", "Yoruba", "Zulu"]
WMT_LANGUGES_FR = ["Kinyarwanda", "Lingala", "Swahili", "Wolof"]

CUTOFF = 1
INPUT_PATH = f"../../../data/clean/african-storybooks-initiative/eng-mismatch-removed/cutoff-{CUTOFF}/"
base_stories = [x for x in os.listdir(INPUT_PATH) if '.json' in x]
lang_story_count = {}
lang_sentence_count = {}

for filename in base_stories:
    json_file = json.load(open(INPUT_PATH + filename))
    json_lang = json_file['language']

    if json_lang not in lang_story_count.keys():
        lang_story_count[json_lang] = 0

    lang_story_count[json_lang] += 1


    if json_lang not in lang_sentence_count.keys():
        lang_sentence_count[json_lang] = 0

    page_sentences = [sent_tokenize(page['text']) for page in json_file['pages'] ]
    book_total_sentences = sum([len(s) for s in page_sentences])
    lang_sentence_count[json_lang] += book_total_sentences

sorted_list = sorted( ((v,k) for k,v in lang_sentence_count.items()), reverse=True)
for entry in sorted_list:
    print(entry[0], entry[1])
#
# for key in lang_story_count.keys():
#     #for x in WMT_LANGUGES_FR + WMT_LANGUAGES_ENG:
#     x = "Afrikaans"
#     if similar(x, key) > 0.5:
#         print(key, lang_sentence_count[key])
#
#
# #
