import json
import os
import nltk
from random import choices
import unicodedata

WRITING_PATH = "../../data/language-id/characters.json"
writing_systems = json.load(open(WRITING_PATH))

WORD_PATH = "../../data/language-id/word_frequencies.json"
word_frequencies = json.load(open(WORD_PATH))

CHAR_PATH = "../../data/language-id/character_frequencies.json"
char_frequencies = json.load(open(CHAR_PATH))

RAND_PATH = "../../data/language-id/unknown.txt"
with open(RAND_PATH, 'w') as fp:
    pass

def generate_sentence(script_name):
    sentence = ""
    word_freq_keys = list(word_frequencies[script_name].keys())
    word_freq_vals = list(word_frequencies[script_name].values())
    char_freq_keys = list(char_frequencies[script_name].keys())
    char_freq_vals = list(char_frequencies[script_name].values())

    len_sentence = int(choices(word_freq_keys, word_freq_vals)[0]) # choose a sentence lenth.
    for i in range(len_sentence):
        len_word = int(choices(char_freq_keys, char_freq_vals)[0]) # choose a word length, per word.
        # randomly pick characters from this script.
        sentence += ''.join(choices(writing_systems[script_name], k = len_word )) + " "
    return sentence

for i in range(5000):
    found = False
    while found == False:
        random_script = choices(list(writing_systems.keys()), k = 1)[0]
        try:
            sentence = generate_sentence(random_script)
            sentence = sentence.replace('\n', '').replace('\r\n','').replace('\r', '')
            with open(RAND_PATH, 'a') as fp:
                fp.write(sentence + "\n")
            found = True
        except:
            continue
