import os
import nltk
import pickle
import random
import time
from features import *
total_start_time = time.time()
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

# Step 1: Get language codes.
def get_language_code_values(ISO_PATH):
    isocodes = json.load(open(ISO_PATH))
    iso_keys = list(isocodes.keys())
    isocode_values = set() # ISO code values (eng, hin, etc.).

    for key in isocodes:
        isocode_values.add(isocodes[key])
    return isocode_values

# Step 2: Combine Data
def get_combined_data(isocode_values, INPUT_PATH, MAX_DATA):
    isocodes_found = []
    combined_data = []
    lengths = {}
    for lang in isocode_values:
        lang_fp = open(INPUT_PATH + lang + ".txt")
        lang_contents = lang_fp.readlines()

        lang_data = []
        for page in lang_contents:
            sentences = nltk.sent_tokenize(page)
            for s in sentences:
                lang_data.append((s, lang))

        random.shuffle(lang_data)
        clipped = lang_data[:MAX_DATA]# randomly select MAX_DATA sentences.

        length = len(clipped)
        if length >= 20: # TODO: change back to 20. we only want to build LID for langs that have at least 20 sentences. 10 test. rest for train.
            combined_data += clipped
            lengths[lang] = length

    # also return isocodes that you found data for.
    print(f"Number of classes: {len(lengths.keys())}")

    return combined_data, lengths

# create a process pool that uses all cpus
if __name__ == "__main__":
    # Step 0: Constants
    OUTPUT_PATH = "../../data/lms/"
    ISO_PATH = "../../data/parallel/isocodes_lid.json"
    INPUT_PATH = "../../data/language-id/monolingual_combined/"
    MAX_DATA = 1000
    experiment_no = 104

    #isocode_values = get_language_code_values(ISO_PATH) # 1. Get code values
    isocode_values = ["yue", "zho"]

    combined_data, lengths = get_combined_data(isocode_values, INPUT_PATH, MAX_DATA) # 2. Get combined data
    print("splitting data now + feauturizing it")

    # Step 5: Train a Naive Bayes model for all languages.
    trainX, trainY = train_test_split(combined_data, lengths, isocode_values, experiment_no)
    print("training naive bayes classifier now")
    start_time = time.time()

    classifier = MultinomialNB(force_alpha=True)
    # classifier = RandomForestClassifier()
    classifier.fit(trainX, trainY)
    end_time = time.time()
    total_end_time = time.time()
    print(f"Training Time: {end_time - start_time}s")
    print(f"Total Script Run Time: {total_end_time - total_start_time}s")

    with open(OUTPUT_PATH + f"test{experiment_no}", "wb") as p:
        pickle.dump(classifier, p)
