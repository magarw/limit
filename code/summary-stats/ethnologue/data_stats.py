import pandas as pd
import json
import os
import nltk

"""
country_populations.tsv: contains country names and populations.
CountryCodes.tab: contains country codes, names, and regions.
ethnologue20.tab

Index(['Also spoken in', 'Alternate Names', 'Autonym', 'Classification',
       'Country', 'Dialects', 'ISO 639-3', 'Language Development',
       'Language Maps', 'Language Resources', 'Language Status',
       'Language Use', 'Location', 'Other Comments', 'Population',
       'Population Numeric', 'Typology', 'Writing', 'name'],

ethnologue20b.tsv: contains information about number of speakers
LanguageIndex.tab: contains information about different varieties of a language with the same isocode
macrolanguages.tsv:
"""
ISOCODES = "../../../data/parallel/isocodes_lid.json"
isocodes_json = json.load(open(ISOCODES))
isocodes_values = set(isocodes_json.values())

ethnologue = pd.read_csv("../../../data/ethnologue/ethnologue20.tab", sep="\t")
records = {}

MONO_PATH = "../../../data/language-id/monolingual_combined/"
special_cases = json.load(open("../../../data/ethnologue/lang-family-exceptions.json"))

for x in isocodes_values:
    if '_'in x:
        x = x.split('_')[0]

    results = list(ethnologue.loc[ethnologue['ISO 639-3'] == x, 'Classification']) # classification has info.
    if len(results) > 0 and str(results[0]) != 'nan' and str(results[0]) != '':    # some non-nan result was returned,
        if ','in results[0]:
            fam = results[0].split(',')[0]
        else:
            fam = results[0]
        if fam in records.keys():
            records[fam].append(x)
        else:
            records[fam] = [x]
    else:
        if x in special_cases.keys():
            fam = special_cases[x]
            if fam in records.keys():
                records[fam].append(x)
            else:
                records[fam] = [x]

# number of languages
for x in records.keys():
    print(x, len(records[x]))

# sentence counts
counts = {}
for x in records.keys():
    counts[x] = 0
    for iso in records[x]:
        #print(MONO_PATH + x + ".txt")
        if os.path.exists(MONO_PATH + iso + ".txt"):
            f = open(MONO_PATH + iso + ".txt").readlines()
            counts[x] += sum([len(nltk.sent_tokenize(l)) for l in f])
for x in counts.keys():
    print(x, counts[x])

#x = pd.read_csv("../../../data/ethnologue/macrolanguages.tsv", sep="\t")
# print(x.loc[x['LangID'] == 'fas',:]) # classification has info.
#print(x.head())
#
