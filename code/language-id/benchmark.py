import os
import json
import pandas as pd

#from afrolid.main import classifier
import gcld3
from pyfranc import franc
import langid

"""
Prints a table of F1 scores for different models

Parameters:
- list_f1s (list) : List of tuples containing F1 scores and model names
- latex (bool) : Flag to indicate if output should be formatted for LaTeX

Returns:
- None
"""
def print_f1_table(list_f1s, latex=False):
    all_rows = set()
    all_columns = [x[1] for x in list_f1s]
    for d in list_f1s:
        cur_set = set(d[0].keys())
        print("Num rows in ", d[1], " are " , len(cur_set))
        all_rows.update()

    f1_score_table = pd.DataFrame(0, index=list(all_rows) + ['aggregate'], columns=all_columns)

    for d in list_f1s:
        colname = d[1]
        for k in d[0].keys():
            val = d[0][k]
            if isinstance(val, str):
                val = 0
            f1_score_table.loc[k,colname] = round(val, 4)
        # Aggregate score.
        f1_score_table.loc['aggregate',colname] = 0

    col_sums = f1_score_table.sum(axis=0)
    #print("printing column sums now:")
    total = len(f1_score_table.index)- 1
    for c in all_columns:
        f1_score_table.loc['aggregate',c] = col_sums[c]/total

    f1_score_table.to_csv("../../data/language-id/f1_scores.csv")

    if latex:
        a = f1_score_table.loc['aggregate','gcld3']
        b = f1_score_table.loc['aggregate','franc']
        c = f1_score_table.loc['aggregate','langid']
        d = f1_score_table.loc['aggregate','limit']
        if isinstance(a, str):
            a = 0
        if isinstance(b, str):
            b = 0
        if isinstance(c, str):
            c = 0
        if isinstance(d, str):
            d = 0
        #if a < 0.9 and b < 0.9 and c < 0.9 and a > 0 and b > 0 and c > 0:
        if a >= b and a >= c and a >= d:
            a = f"\\textbf{{ {a} }}"
        elif  b >= a and b >=c and b >= d:
            b= f"\\textbf{{ {b} }}"
        elif c >= a and c >= b and c >= d:
            c = f"\\textbf{{ {c} }}"
        else:
            d = f"\\textbf{{ {d} }}"
        print(f"Macro F1  &  {a} & {b} &  {c} &{d} \\\\")

def calculate_precisions(matrix, labels):
    precisions = {}
    for x in labels:
        precisions[x] = [0,0]

    for x in matrix.index:
        precisions[x][1] = sum(matrix.loc[x, :])
        for y in matrix.columns:
            val = matrix.loc[x, y]
            if x == y:
                precisions[x][0] += val
    return precisions

def calculate_recall(matrix, labels):
    recall = {}
    for x in labels:
        recall[x] = [0,0]

    for x in matrix.columns:
        recall[x][1] = sum(matrix.loc[:, x])
        for y in matrix.index:
            val = matrix.loc[y, x]
            if x == y:
                recall[x][0] += val

    return recall

def calculate_f1(matrix):
    precisions = calculate_precisions(matrix, matrix.index)
    recall = calculate_recall(matrix, matrix.columns)
    common_keys = set(recall.keys()).intersection(precisions.keys())
    print("Common key length: ", len(common_keys))
    filtered_precisions = {k:v for (k,v) in precisions.items() if k in common_keys}
    filtered_recall = {k:v for (k,v) in recall.items() if k in common_keys}
    f1_scores = {}
    for k in common_keys:
        p = filtered_precisions[k][0]/filtered_precisions[k][1]
        r = filtered_recall[k][0]/filtered_recall[k][1]
        if p == 0 and r == 0:
            f1_scores[k] = 0
        f1_scores[k] = 2 * p * r / (p + r)
    return f1_scores

TEST_DATA = "../../data/lms/data/test.txt"
test_data = [eval(x.strip()) for x in open(TEST_DATA).readlines()]
test_labels_set = set([x[1] for x in test_data])
test_labels = list(test_labels_set)
print("Number of classes in test: ", len(test_labels))
#
# langid_maps = json.load(open("../../data/language-id/mappings_langid.json"))
# langid_preds_set = set(langid_maps.values())
# common_langid_test = langid_preds_set.intersection(test_labels_set)
# langid_preds = list(common_langid_test)
# print(f"Langid number of languages tested: {len(langid_preds)}/{len(langid_preds_set)}")
# langid_confusion_matrix = pd.DataFrame(0, index=list(langid_preds_set) + ["other"], columns=test_labels)
# unique = test_labels_set.difference(common_langid_test)

# gcld3_maps = json.load(open("../../data/language-id/mappings_gcld3.json"))
# gcld3_preds_set = set(gcld3_maps.values())
# common_gcld3_test = gcld3_preds_set.intersection(test_labels_set)
# gcld3_preds = list(common_gcld3_test)
# print(f"GCLD3 number of languages tested: {len(common_gcld3_test)}/{len(gcld3_preds_set)}")
# detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)
# gcld3_confusion_matrix = pd.DataFrame(0, index=list(gcld3_preds_set) + ["other"], columns=test_labels)
# unique = unique.difference(common_gcld3_test)

franc_json = json.load(open("../../data/language-id/franc_keys.json"))
franc_keys_set = set()
for key in franc_json.keys():
    for key_ in franc_json[key].keys():
        franc_keys_set.add(key_)
common_franc_test =franc_keys_set.intersection(test_labels_set)
print(f"Franc number of languages tested: {len(common_franc_test)}/{len(franc_keys_set)}")
franc_keys = list(common_franc_test)
franc_confusion_matrix = pd.DataFrame(0, index=list(franc_keys_set) + ["other"], columns=test_labels)

# unique = unique.difference(common_franc_test)
# hierarch_confusion_matrix = pd.DataFrame(0, index=list(franc_keys_set) + ["other"], columns=test_labels)
# print(f"New Languages: {len(unique)} languages")

for line in test_data:
    sample = line[0]
    actual = line[1]

    # result = detector.FindLanguage(text=sample)
    # if result.language in gcld3_maps.keys():
    #     prediction = gcld3_maps[result.language]
    # else:
    #     prediction = result.language
    #     if prediction not in gcld3_confusion_matrix.index:
    #         gcld3_confusion_matrix.loc[prediction] = [0] * gcld3_confusion_matrix.shape[1]
    # gcld3_confusion_matrix.loc[prediction, actual] += 1

    try:
        prediction_franc = franc.lang_detect(sample)[0][0]
    except ZeroDivisionError:
        prediction_franc = "other"

    if prediction_franc not in franc_keys_set and prediction_franc not in franc_confusion_matrix.index:
        franc_confusion_matrix.loc[prediction_franc] = [0] * franc_confusion_matrix.shape[1]
    franc_confusion_matrix.loc[prediction_franc, actual] += 1

    # prediction_lid = langid_maps[langid.classify(sample)[0]]
    # if prediction_lid not in langid_preds_set:
    #     prediction_lid = "other"
    # langid_confusion_matrix.loc[prediction_lid, actual] += 1

franc_confusion_matrix.to_csv("../../data/lms/data/franc_confusion_matrix_latest.csv")

# gcld3_confusion_matrix.to_csv("../../data/lms/data/gcld3_confusion_matrix.csv")
# langid_confusion_matrix.to_csv("../../data/lms/data/langid_confusion_matrix.csv")

# LIMIT confusion matrix:
# limit_confusion_matrix = pd.read_csv("../../data/lms/data/limit_confusion_matrix.csv", index_col=0)
# for i in range(limit_confusion_matrix.shape[0]):
#     for j in range(limit_confusion_matrix.shape[1]):
#         if isinstance(limit_confusion_matrix.iloc[i, j], str):
#             limit_confusion_matrix.iloc[i, j] = 0

#f1_scores_gcld3 = calculate_f1(gcld3_confusion_matrix)
#f1_scores_franc = calculate_f1(franc_confusion_matrix)
#f1_scores_lid = calculate_f1(langid_confusion_matrix)
#f1_scores_limit = calculate_f1(limit_confusion_matrix)

# print_f1_table([(f1_scores_gcld3, 'gcld3'), (f1_scores_franc, 'franc'), (f1_scores_lid, 'langid'), (f1_scores_limit, 'limit')], latex=True)


# GCLD3 on FLORES
"""
FLORES_DATA = "../../data/language-id/flores200/"
flores_files = []
flores_labels = set()
for x in os.listdir(FLORES_DATA):
    if '.devtest' in x:
        flores_files.append(x)
        flores_labels.add(x.split('_')[0])

flores_labels = list(flores_labels)
gcld3_flores_confusion_matrix = pd.DataFrame(0, index=gcld3_preds, columns=flores_labels)
franc_flores_confusion_matrix = pd.DataFrame(0, index=franc_keys, columns=flores_labels)

for file in flores_files:
    actual = file.split('_')[0]
    lines = [x.strip() for x in open("../../data/language-id/flores200/"+ file).readlines()]
    for line in lines:
        try:
            result = detector.FindLanguage(text=line)
            prediction_franc = franc.lang_detect(line)[0][0]
            prediction = gcld3_maps[result.language]
            gcld3_flores_confusion_matrix.loc[prediction, actual] += 1
            franc_flores_confusion_matrix.loc[prediction_franc, actual] += 1
        except:
            continue

gcld3_flores_confusion_matrix.to_csv("../../data/lms/data/gcld3_flores_confusion_matrix.csv")
franc_flores_confusion_matrix.to_csv("../../data/lms/data/franc_flores_confusion_matrix.csv")

"""















#
