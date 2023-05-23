import pandas as pd
import json
import gcld3

franc_json = json.load(open("../../data/language-id/franc_keys.json"))
franc_keys_set = set()
for key in franc_json.keys():
    for key_ in franc_json[key].keys():
        franc_keys_set.add(key_)
#
# gcld3_maps = json.load(open("../../data/language-id/mappings_gcld3.json"))
# gcld3_preds_set = set(gcld3_maps.values())

input_matrix = "../../data/lms/data/franc_confusion_matrix_latex.csv"
mat = pd.read_csv(input_matrix, index_col=0)

common = set(mat.index).intersection(set(mat.columns))
mat = mat.loc[list(common),list(common)] # Filter the matrix to only include those columns that Franc actually supports.

mat['row_sum'] = mat.sum(axis=1)
mat['mispredictions'] = mat['row_sum']
for i in range(mat.shape[0]):
    row_pred = mat.index[i]
    if row_pred in mat.columns:
        mat.loc[row_pred, 'mispredictions']  = mat.loc[row_pred, 'row_sum'] - mat.loc[row_pred, row_pred]

mat = mat.sort_values(by=['mispredictions'], ascending=False)
for i in range(100):
    row = mat.iloc[i, :]
    pred = mat.index[i]
    print("\nRow: ", pred)
    candidates = row.sort_values(ascending=False)
    for actual in candidates.index:
        if actual in gcld3_preds_set and candidates.loc[actual] > 0:
            print(pred, actual, candidates.loc[actual])

#
