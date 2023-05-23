import json
import os
import collections

import nltk
from nltk.util import ngrams
import random
import pickle
from features import *
import gcld3

# ISO codes, getting language names. Samim changed to 'fas'
ISO_PATH = "../../data/parallel/isocodes_lid.json"
isocodes = json.load(open(ISO_PATH))
iso_keys = list(isocodes.keys())

isocode_values = set() # ISO code values (eng, hin, etc.).
for key in isocodes:
    isocode_values.add(isocodes[key])

# First, we will test with the following languages.
# Afrikaans, Amharic, Zulu, English, French, Kinyarwanda, Xhosa, Luganda, Swahili.
INPUT_PATH = '../../data/parallel/master.json'
OUTPUT_PATH = '../../data/language-id/monolingual/'
MAX_DATA = 5000

# HELPER FUNCTIONS
# Step 1: Data Preparation
def get_language_data(input_language, INPUT_PATH, MAX_DATA):
    master_json = json.load(open(INPUT_PATH))
    master_list = []
    for story in master_json.keys():
        story_languages = master_json[story].keys()
        for l in story_languages:
            if l in isocodes.keys() and isocodes[l] == input_language:
                master_list += master_json[story][l]

    print("Num pages:", len(master_list))
    complete_data = []
    for page in master_list:
        sentences = nltk.sent_tokenize(page)
        for s in sentences:
            complete_data.append((s, input_language))

    return complete_data[:MAX_DATA]

# Step 2: Train/Dev/Test Split
def add_features(examples):
    data = []
    for s in examples:
        features = feature_extract(s[0])
        data.append((features, s[1]))
    return data

def train_test_split(language_data, test_size):
    import random
    test_samples = int(test_size * len(language_data))
    random.shuffle(language_data)
    test_data = language_data[:test_samples]
    train_data = language_data[test_samples:]

    print(f"Total Data Size: {len(language_data)}")
    print(f"Test Data Size: {len(test_data)}")
    print(f"Train Data Size: {len(train_data)}")

    return add_features(train_data), add_features(test_data)

# combined_data = []
# input_languages = ["English", "Hindi"]
# isocode_values = ["tel","hin"]
for lang in isocode_values:
    language_data = get_language_data(lang, INPUT_PATH, MAX_DATA)

    # Output this monolingual training data for LID purposes.
    with open(OUTPUT_PATH + lang + '.txt', 'w') as fp:
        for x in language_data:
            y = x[0].strip().replace("\n", "").replace("\r", "").replace("\r\n", "")
            if y != "":
                fp.write(y + "\n")

#train_data, test_data = train_test_split(combined_data, 0.33)

#classifier = nltk.NaiveBayesClassifier.train(train_data)
# print(classifier.classify(feature_extract("Hy is in die hospitaal, maar hy eet nie.")))
#print(nltk.classify.accuracy(classifier, test_data))

# f = open(OUTPUT_PATH + 'eng-hin.pickle', 'wb')
# pickle.dump(classifier, f)
# f.close()

"""
From the Python binding GCLD3, we don't have access to the character level embeddings,
so we will likely have to use the C version.

"""
# min_num_bytes : minimum number of bytes to consider during inference. Setting this to a value higher than 0 will return und for empty string.
# max_num_bytes : maximum number of bytes to consider during inference. It will truncate excess bytes should the input text exceeds the value set.
# If you intent to filter out empty string and short strings, you initialize the instance as follows:
# detector = gcld3.NNetLanguageIdentifier(min_num_bytes=10, max_num_bytes=1000)
"""
detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)

# CDL3 comes with two inference functions.
# The first one is the FindLanguage function which is meant for single language inference.
# It accepts the a single text argument which represents the sample text.

sample = "Mit tech aato re baryaa koda gedaraa kina taankana unkina ngutum do dholuu aar bholuu."
result = detector.FindLanguage(text=sample)

# language : language code represented in BCP-47-style.
# is_reliable : a boolean which reflects the reliability of the detection.
# proportion : a float which represents the proportion and weights of the predicted language in the sample text. Range from 0 to 1. This field is useful during multi-language detection.
# probability : the confidence level of the prediction. Range from 0 to 1.
print(result.language, result.is_reliable, result.proportion, result.probability)

sample = ("Welcome to Medium. Bienvenido a Medium.")
results = detector.FindTopNMostFreqLangs(text=sample, num_langs=2)
for result in results:
    print(result.language, result.is_reliable, result.proportion, result.probability)
"""
