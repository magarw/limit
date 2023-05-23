import pickle
import json
import os

# https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
#

# adapted from features.py (one extra argument - keys)
def extract(queries, keys):
    extracted = {}
    for key in keys:
        story_versions = master_json[key].keys()

        multiway = True
        for q in queries:
            if q not in story_versions:
                multiway = False

        if multiway:
            inside_json = {}
            for q in queries:
                inside_json[q] = master_json[key][q]

            extracted[key] = inside_json

    return extracted

master_json = json.load(open('../../data/parallel/master.json'))
master_keys = master_json.keys()

candidates = open('../../data/parallel/multilingual_extract_candidates.txt')
candidates = [x.strip().split(';') for x in candidates.readlines()]
print(candidates)
for pair in candidates:
    sample_language, reference_language = pair[0], pair[1]
    print(f"Processing: {sample_language}")
    output_json = {'data': {}, 'info': {'reference_language': reference_language, 'sample_language': sample_language}}

    new_language = sample_language.replace(reference_language, '').replace('-','')

    stories_json = extract([sample_language, reference_language], master_keys)
    stories_keys = stories_json.keys()
    total_stories = len(stories_keys)

    high_confidence = 0
    pages_evaluated = 0

    for key in stories_keys:

        # if both X1 and X2 in X1-X2 are there already
        master_langs = master_json[key].keys()
        if new_language in master_langs and reference_language in master_langs:
            continue

        story = stories_json[key]
        for i in range(len(story[sample_language])):
            if i < len(story[reference_language]):
                pages_evaluated += 1
                max_score_right = 0
                max_index_right = 0
                max_score_left = 0
                max_index_left = 0
                for j in range(len(story[sample_language][i])):
                    score_right = similar(story[reference_language][i], story[sample_language][i][-j:])
                    if score_right > max_score_right:
                        max_score_right = score_right
                        max_index_right = j
                    #print(score_right, story['English-Hindi'][i][-j:])

                    score_left = similar(story[reference_language][i], story[sample_language][i][:j])
                    if score_left > max_score_left:
                        max_score_left = score_left
                        max_index_left = j
                    #print(score_left, story['English-Hindi'][i][:j])

                max_score = 0
                if max_score_left > max_score_right:
                    max_score = max_score_left
                    substring = story[sample_language][i][:max_index_left]
                else:
                    max_score = max_score_right
                    substring = story[sample_language][i][-max_index_right:]

                if max_score > 0.85:
                    high_confidence += 1

                    # add this substring to the new dictionary
                    if key not in output_json['data'].keys():
                        output_json['data'][key] = {}

                    if new_language not in output_json['data'][key].keys():
                        output_json['data'][key][new_language] = []

                    if reference_language not in output_json['data'][key].keys():
                        output_json['data'][key][reference_language] = []

                    output_json['data'][key][reference_language].append(story[reference_language][i])
                    output_json['data'][key][new_language].append(story[sample_language][i].replace(substring, '').strip())

        #print(high_confidence, pages_evaluated, total_stories)

    with open(f'../../data/parallel/multilingual/{sample_language}.json', 'w') as fp:
        json.dump(output_json, fp)
    print(f"Complete: {sample_language}")

#split =  nltk.word_tokenize(sample_sentence) # this assumes that we have spaces between words. doesn't work.

"""
probs_left = []
probs_right = []
for i in range(len(sample_sentence)):
    left = sample_sentence[:i]
    right = sample_sentence[-i:]
    dist_left = classifier.prob_classify(feature_extract(left))
    dist_right = classifier.prob_classify(feature_extract(right))

    probs_left.append(dist_left.prob("English"))
    probs_right.append(dist_right.prob("English"))

    # for label in dist_left.samples():
    #     print("%s: %f" % (label, dist.prob(label)))

# print(probs_left)
# print(probs_right)
# it would be assigned a low score for Odia till true Odia text is mixed in, when the score should jump
maxpos = probs_left.index(max(probs_left))
print("Prediction 1: ", "".join(sample_sentence[:maxpos]))
print("Prediction 2: ", "".join(sample_sentence[maxpos:]))
maxpos = probs_right.index(max(probs_right))
print("Prediction 1: ", "".join(sample_sentence[-maxpos:]))
print("Prediction 2: ", "".join(sample_sentence[:-maxpos]))

"""

#
