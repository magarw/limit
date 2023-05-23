import json
import requests
import os
from os.path import exists
import matplotlib.pyplot as plt
from langdetect import detect, detect_langs

"""inconsistencies in the results can come because the algorithm under the hood
is non-deterministic, and the higher the noise in the text, the higher the inconsistency.
This issue can be fixed by setting the seed before running the language detection instructions

-- Google's Documentation
"""
from langdetect import DetectorFactory
DetectorFactory.seed = 0

def language_detection(text, method = "single"):

  """
  @desc:
    - detects the language of a text
  @params:
    - text: the text which language needs to be detected
    - method: detection method:
      single: if the detection is based on the first option (detect)
  @return:
    - the langue/list of languages
  """

  if(method.lower() != "single"):
    result = detect_langs(text)

  else:
    result = detect(text)

  return result

# paths and constants
CUTOFF = 1
INPUT_PATH = f"../../../data/clean/pratham-books-storyweaver/non-sparse/cutoff-{CUTOFF}/"
OUTPUT_PATH = "../../../data/clean/pratham-books-storyweaver/eng-mismatch-removed/"

print("Script to remove stories with excessive English in a non-English stories.")
input_filenames = [x for x in os.listdir(INPUT_PATH) if '.json' in x]
total = len(input_filenames)
print(total, " files to start off with.")

progress = 0
for file_name in input_filenames:
    progress += 1
    print(f"{progress}/{total} files read.")
    json_file = json.load(open(INPUT_PATH + file_name))
    if "english" not in json_file["language"].lower():
        text = json_file["pages"]
        num_pages_with_excess_english = 0

        for t in text[1:]: # i.e. for each page
            try:
                prediction = language_detection(t, 'show_proba')
            except Exception as e:
                continue
            for p in prediction:
                if p.lang == 'en' and p.prob > 0.90:
                    num_pages_with_excess_english += 1

        if num_pages_with_excess_english/(len(text) - 1) >= 0.5: # i.e. more than half the pages have excess English
            with open(f"{OUTPUT_PATH}candidate_removals_cutoff{CUTOFF}.txt", "a") as f:
                f.write(f"Excess: {num_pages_with_excess_english}/{len(text) - 1}; File: {file_name}; OrigLang: {json_file['language']}\n")








                #
