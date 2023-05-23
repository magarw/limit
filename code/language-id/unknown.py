import json
import os
import nltk
import unicodedata


"""
- random strings in all of the writing systems that we cover.
- should look like text: sample num of words, num of characters/word,
 and then sample from these distributions.
"""

MONO_PATH = "../../data/language-id/monolingual_combined/"
SEL_PATH = "../../data/language-id/selected_languages.txt"

# Task 1: What writing systems do we cover?

# Read the appropriate files (for languages in the langID model)
selected_langs = set([x.strip() +".txt" for x in open(SEL_PATH).readlines()])
all_files = set(os.listdir(MONO_PATH))
selected_files = all_files.intersection(selected_langs)
blacklist = ['0', '1', '2','3', '4', '5', '6', '7', '8', '9', '÷', '(', ')', '=']
latin_set = set(''.join(map(chr, range(0x0000, 0x024F))))

ch_frq_per_lang = {}
wrd_ct_freq = {}
word_path = "../../data/language-id/word_frequencies.json"
char_path ="../../data/language-id/character_frequencies.json"
#
# if os.path.exists(word_path):
#     wrd_ct_freq = json.load(open(word_path))
# if os.path.exists(char_path):
#     ch_frq_per_lang = json.load(open(char_path))

if len(ch_frq_per_lang.keys()) == 0:
    for selected_lang in selected_files:
        f = open(MONO_PATH + selected_lang).readlines()
        lang_chs = {}
        for line in f:
            # Build character frequencies for each language.
            for character in line:
                if character not in lang_chs.keys() and character not in blacklist:
                    lang_chs[character] = 0
                if character not in blacklist:
                    lang_chs[character] += 1
        ch_frq_per_lang[selected_lang] = lang_chs

    with open(char_path, "w") as fp:
        json.dump(ch_frq_per_lang, fp)

all_scripts = {
'arabic_script': map(chr, range(0x0600,0x06FF)),
'bengali_script': map(chr, range(0x0980,0x09FF)),
'cyrillic_script' : map(chr, range(0x0400,0x04FF)),
'devanagri_script' : map(chr, range(0x0900,0x097F)),
'gujarati_script' : map(chr, range(0x0A80,0x0AFF)),
'georgian_script': map(chr, range(0x10A0, 0x10FF)),
'chinese_script' : map(chr, range(0x4E00, 0x9FFF)),
'telugu_script' : map(chr, range(0x0C00, 0x0C7F)),
'tamil_script' : map(chr, range(0x0B80, 0x0BFF)),
'kannada_script' : map(chr, range(0x0C80, 0x0CFF)),
'malayalam_script' : map(chr, range(0x0D00, 0x0D7F)),
'odia_script' : map(chr, range(0x0B00, 0x0B7F)),
'geez_script' : map(chr, range(0x1200, 0x137F)),
'hebrew_script' : map(chr, range(0x0590, 0x05FF)),
'greek_script' : map(chr, range(0x0370, 0x03FF)),
'tibetan_script' : map(chr, range(0x0F00, 0x0FFF)),
'latin_script': map(chr, range(0x0000, 0x024F)),
'khmer_script':map(chr, range(0x1780,0x17FF)),
'burmese_script': map(chr, range(0x1000,0x109F)),
'olchiki_script': map(chr, range(0x1C50,0x1C7F)),
'thai_script': map(chr, range(0x0E00,0x0E5B))
}

# remove any empty characters:
for key in all_scripts.keys():
    new_str = ""
    for x in all_scripts[key]:
        if unicodedata.category(x) != 'Cn':
            new_str += x
    all_scripts[key] = new_str
all_scripts['malayalam_script'] = ''.join(map(chr, range(0x0D00, 0x0D7F)))

# Overall writing systems
num = 0
writing_systems_counts = {'latin_script': 0 }
writing_systems_list = {'latin_script': [] }
chr_ct_freq = {'latin_script': {}}
wrd_ct_freq = {'latin_script': {}}
for lang in ch_frq_per_lang.keys():
    flag = False
     # lang's ch set
    cur_lang_set = set(ch_frq_per_lang[lang].keys())
    cur_lang_length = len(cur_lang_set)

    # remove latin script characters from this set.
    cur_lang_set_nolat = cur_lang_set.difference(latin_set)
    cur_lang_set_nolat_length = len(cur_lang_set_nolat)

    if cur_lang_set_nolat_length <= 0.1*cur_lang_length: # i.e. 90% characters were Latin
        flag = True
        writing_systems_counts['latin_script'] += 1
        writing_systems_list['latin_script'].append(lang)
        f = open(MONO_PATH + lang).readlines()
        for line in f:
            sent_split = nltk.word_tokenize(line)
            sent_length = len(sent_split)
            if sent_length not in wrd_ct_freq['latin_script'].keys():
                wrd_ct_freq['latin_script'][sent_length] = 0
            wrd_ct_freq['latin_script'][sent_length] += 1

            for word in sent_split:
                length = len(word)
                if length not in chr_ct_freq['latin_script'].keys():
                    chr_ct_freq['latin_script'][length] = 0
                chr_ct_freq['latin_script'][length] += 1

    cur_lang_length = len(cur_lang_set)
    keys = all_scripts.keys()

    for key in keys:
        key_set = set(all_scripts[key])
        intersection = len(key_set.intersection(cur_lang_set))
        if intersection > 0.5 * cur_lang_set_nolat_length and flag == False:
            flag = True
            if key not in writing_systems_counts.keys():
                writing_systems_counts[key] = 0
            writing_systems_counts[key] += 1

            if key not in writing_systems_list.keys():
                writing_systems_list[key] = []
            writing_systems_list[key].append(lang)

            # we know that the writing system is 'key'
            if key not in chr_ct_freq.keys():
                chr_ct_freq[key] = {}
            if key not in wrd_ct_freq.keys():
                wrd_ct_freq[key] = {}
            f = open(MONO_PATH + lang).readlines()
            for line in f:
                sent_split = nltk.word_tokenize(line)
                sent_length = len(sent_split)
                if sent_length not in wrd_ct_freq[key].keys():
                    wrd_ct_freq[key][sent_length] = 0
                wrd_ct_freq[key][sent_length] += 1

                for word in sent_split:
                    length = len(word)
                    if length not in chr_ct_freq[key].keys():
                        chr_ct_freq[key][length] = 0
                    chr_ct_freq[key][length] += 1
            break

    if flag == False:
        print("didnt match any", lang)
        all_scripts[num] = ''.join(cur_lang_set)
        #print(cur_lang_set)

        if num not in writing_systems_counts.keys():
            writing_systems_counts[num] = 0
        writing_systems_counts[num] += 1

        if num not in writing_systems_list.keys():
            writing_systems_list[num] = []
        writing_systems_list[num].append(lang)

        # we know that the writing system is 'num'
        if num not in chr_ct_freq.keys():
            chr_ct_freq[num] = {}
        if num not in wrd_ct_freq.keys():
            wrd_ct_freq[num] = {}
        f = open(MONO_PATH + lang).readlines()
        for line in f:
            sent_split = nltk.word_tokenize(line)
            sent_length = len(sent_split)

            if sent_length not in wrd_ct_freq[num].keys():
                wrd_ct_freq[num][sent_length] = 0
            wrd_ct_freq[num][sent_length] += 1

            for word in sent_split:
                length = len(word)
                if length not in chr_ct_freq[num].keys():
                    chr_ct_freq[num][length] = 0
                chr_ct_freq[num][length] += 1

        num = num + 1


with open("../../data/language-id/writing_system_counts.json", "w") as fp:
    json.dump(writing_systems_counts, fp)

with open("../../data/language-id/writing_systems_list.json", "w") as fp:
    json.dump(writing_systems_list, fp)

with open("../../data/language-id/word_frequencies.json", "w") as fp:
    json.dump(wrd_ct_freq, fp)

with open("../../data/language-id/character_frequencies.json", "w") as fp:
    json.dump(chr_ct_freq, fp)

with open("../../data/language-id/characters.json", "w") as fp:
    json.dump(all_scripts, fp)
