import json
import os
import nltk

# 8-way parallel file:
INPUT_PATH = "../../data/parallel/french-kinyarwanda.json"
master_json = json.load(open(INPUT_PATH))
keys = master_json.keys()
print(f"Found { len(keys)} stories in 8-way file")

count = {}

# pge = page entries
total_pge = 0
multi_pge1 = 0 # to keep track of pge's with multiple sentences in them.
multi_pge2 = 0
multi_pge3 = 0
multi_pge4 = 0
multi_pge5 = 0

for key in keys:
    for lang in master_json[key].keys():
        if lang not in count.keys():
            count[lang] = 0

        for entry in master_json[key][lang]:
            total_pge += 1

            page_entry_count = len(nltk.sent_tokenize(entry))
            if page_entry_count > 1:
                multi_pge1 += 1
            if page_entry_count > 2:
                multi_pge2 += 1
            if page_entry_count > 3:
                multi_pge3 += 1
            if page_entry_count > 4:
                multi_pge4 += 1
            if page_entry_count > 5:
                multi_pge5 += 1

            count[lang] += page_entry_count


x = ""
for key in count:
    x += f"{key}: {count[key]}, "
print(x[:-2])


# This prints:
# English: 2317, Kiswahili: 2337, Amharic: 1916, Afrikaans: 3335, isiZulu: 2881, isiXhosa: 2568, Kinyarwanda: 1655, Luganda: 1755


# What percentage of page entries have multiple sentences?
print(f"Percentage of page entries with >1 sentences: {multi_pge1*100/total_pge:.2f}")
print(f"Percentage of page entries with >2 sentences: {multi_pge2*100/total_pge:.2f}")
print(f"Percentage of page entries with >3 sentences: {multi_pge3*100/total_pge:.2f}")
print(f"Percentage of page entries with >4 sentences: {multi_pge4*100/total_pge:.2f}")
print(f"Percentage of page entries with >5 sentences: {multi_pge5*100/total_pge:.2f}")


# EASY ALIGN: check if # of sentences are equal.
# pages
total_pages_a = 0
total_pages_b = 0
unequal_pages_a = 0
unequal_pages_b = 0


# stories
total_stories = len(keys)
unequal_stories = 0

# page entries
total_page_entries_a = 0
total_page_entries_b = 0
unequal_page_entries_a = 0
unequal_page_entries_b = 0
unequal_pages = 0
total_pages = 0

for key in keys:
    pg_fr  = len(master_json[key]['French'])
    pg_kw = len(master_json[key]['Kinyarwanda'])
    #print(pg_fr) #11
    #print(pg_kw) #11

    total_pages_a += pg_fr
    total_pages_b += pg_kw

    # 11 pages-entries in this story.
    if pg_fr != pg_kw:
        unequal_stories += 1
        unequal_pages_a += pg_fr
        unequal_pages_b += pg_kw

        #print("unequal page counts")
        continue

    for p in range(pg_kw):
        fr_sent = nltk.sent_tokenize(master_json[key]['French'][p])
        kw_sent =nltk.sent_tokenize(master_json[key]['Kinyarwanda'][p])
        len_fr = len(fr_sent)
        len_kw = len(kw_sent)
        #print(len_fr, len_kw)
        total_pages += 1
        total_page_entries_a += len_fr
        total_page_entries_b += len_kw

        if len_fr != len_kw:
            unequal_pages += 1
            #print("unequal num sentences on this page.")
            unequal_page_entries_a += len_fr
            unequal_page_entries_b += len_kw

            #print(fr_sent)
            #print(kw_sent)

print(f"Total Pages (A): {total_pages_a}, Total Pages (B): {total_pages_b}")
print(f"Unequal Pages (A): {unequal_pages_a}, Unequal Pages (B): {unequal_pages_b}")
print(f"Unequal Page% (A): {unequal_pages_a*100/total_pages_a:.2f}, Unequal Page% (B): {unequal_pages_b*100/total_pages_b:.2f}")

print(f"Total Stories: {total_stories}, Unequal Stories: {unequal_stories}, %: {unequal_stories*100/total_stories:.2f}")

print(f"Total Page-Entries (A): {total_page_entries_a}, Total Page-Entries (B): {total_page_entries_b}")
print(f"Unequal Pages: {unequal_pages}, Total Pages: {total_pages}, %: {unequal_pages*100/total_pages:.2f}")





















#
