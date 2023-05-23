import os
import json
import pandas as pd
import pickle
from pyfranc import franc
from features import *
import gcld3
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale = 5)

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

    f1_score_table.to_csv("../../data/language-id/f1_scores_111.csv")

    if latex:
        a = f1_score_table.loc['aggregate','franc']
        b = f1_score_table.loc['aggregate','LIMIT-H']
        if isinstance(a, str):
            a = 0
        if isinstance(b, str):
            b = 0
        #if a < 0.9 and b < 0.9 and c < 0.9 and a > 0 and b > 0 and c > 0:
        if a >= b:
            a = f"\\textbf{{ {a} }}"
        elif  b >= a:
            b= f"\\textbf{{ {b} }}"
        print(f"Macro F1  &  {a} & {b}  \\\\")

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

def make_heatmap(matrix, name):
    for x in matrix.columns:
        col_sum = matrix[x].sum()
        matrix[x] = matrix[x]/col_sum
    matrix.to_csv(f"../../data/lms/data/{name}.csv")
    matrix = matrix[languages].reindex(languages)
    fig, ax = plt.subplots(figsize=(20, 20))

    ax = sns.heatmap(matrix, linewidth=0.0, cmap='BuPu')
    ax.set(xlabel='True Labels', ylabel='Predicted Labels')

    # cbar = ax.collections[0].colorbar
    # cbar.ax.tick_params(labelsize=50)
    plt.savefig(f"../../data/lms/data/{name}_heatmap_11.eps", format='eps')


if __name__ == "__main__":

    TEST_DATA = "../../data/lms/data/test.txt"
    test_data = [eval(x.strip()) for x in open(TEST_DATA).readlines()]
    # languages = ["guj", "kfr","Bhilori", "amh", "tir", "stv", "cdz",
    #  "ben", "asm", "yue", "zho", "kfc", "tel", "kfa", "kan", "tsc",
    #  "tso", "Dagaare", "mzm", "bbl", "kat"]
    # languages = ["guj", "kfr","Bhilori", "amh", "tir", "stv", "cdz",
    #  "ben", "asm"]
    languages = [ "guj", "kfr","Bhilori","amh", "tir", "stv"]

    test_data = list(filter(lambda tup: tup[1] in languages, test_data))
    test_labels_set = set([x[1] for x in test_data])
    test_labels = list(test_labels_set)

    overall_test_labels = test_labels + ["other", "und"]

    print(f"# of test examples: {len(test_data)}")
    print(f"# of test labels: {len(test_labels)}")

    a_time = time.time()
    franc_json = json.load(open("../../data/language-id/franc_keys.json"))
    franc_keys_set = set()
    for key in franc_json.keys():
        for key_ in franc_json[key].keys():
            franc_keys_set.add(key_)
    franc_confusion_matrix = pd.DataFrame(0, index=overall_test_labels, columns=test_labels)

    hierarch_model_101 = pickle.load(open("../../data/lms/test101", 'rb'))
    hierarch_model_102 = pickle.load(open("../../data/lms/test102", 'rb'))
    hierarch_model_103 = pickle.load(open("../../data/lms/test103", 'rb'))
    hierarch_model_104 = pickle.load(open("../../data/lms/test104", 'rb'))
    hierarch_model_105 = pickle.load(open("../../data/lms/test105", 'rb'))
    hierarch_model_106 = pickle.load(open("../../data/lms/test106", 'rb'))
    hierarch_model_107 = pickle.load(open("../../data/lms/test107", 'rb'))
    hierarch_model_108 = pickle.load(open("../../data/lms/test108", 'rb'))
    hierarch_model_109 = pickle.load(open("../../data/lms/test109", 'rb'))
    b_time = time.time()
    print(f"Loading models takes {b_time - a_time:.2f}s")

    a_time = time.time()
    hierarch_confusion_matrix = pd.DataFrame(0, index=overall_test_labels , columns=test_labels)
    test_featurized_ = [add_features_test(test_data, x) for x in range(101, 104)] # 101, 110
    b_time = time.time()
    print(f"Featurizing took {b_time - a_time:.2f}s and {len(test_featurized_)} entries")

    i = 0
    overall_test_labels = overall_test_labels + ["cmn","dga"]
    for line in test_data:
        print(i)
        sample = line[0]
        actual = line[1]

        try:
            prediction_franc = franc.lang_detect(sample)[0][0]
        except ZeroDivisionError:
            prediction_franc = "other"
        if prediction_franc not in overall_test_labels:
            prediction_franc = "other"
        if prediction_franc == "cmn" or prediction_franc == "dga":
            franc_confusion_matrix.loc["other", actual] += 1
        else:
            franc_confusion_matrix.loc[prediction_franc, actual] += 1
        if prediction_franc == "guj":
            prediction_hierarch = hierarch_model_101.predict(test_featurized_[0][i][0])[0]
        elif prediction_franc == "tir" or prediction_franc == "amh":
            prediction_hierarch = hierarch_model_102.predict(test_featurized_[1][i][0])[0]
        elif prediction_franc == "ben":
            prediction_hierarch = hierarch_model_103.predict(test_featurized_[2][i][0])[0]
        # elif prediction_franc == "cmn":
        #     prediction_hierarch = hierarch_model_104.predict(test_featurized_[3][i][0])[0]
        # elif prediction_franc == "tel":
        #     prediction_hierarch = hierarch_model_105.predict(test_featurized_[4][i][0])[0]
        # elif prediction_franc == "kan":
        #     prediction_hierarch = hierarch_model_106.predict(test_featurized_[5][i][0])[0]
        # elif prediction_franc == "tso":
        #     prediction_hierarch = hierarch_model_107.predict(test_featurized_[6][i][0])[0]
        # elif prediction_franc == "dga":
        #     prediction_hierarch = hierarch_model_108.predict(test_featurized_[7][i][0])[0]
        # elif prediction_franc == "kat":
        #     prediction_hierarch = hierarch_model_109.predict(test_featurized_[8][i][0])[0]
        else:
            prediction_hierarch = prediction_franc
        hierarch_confusion_matrix.loc[prediction_hierarch, actual] += 1

        i = i + 1

    #franc_confusion_matrix.to_csv("../../data/lms/data/franc_confusion_matrix_111.csv")
    #hierarch_confusion_matrix.to_csv("../../data/lms/data/hierarch_confusion_matrix_111.csv")

    make_heatmap(franc_confusion_matrix, "franc_confusions_111")
    make_heatmap(hierarch_confusion_matrix, "hierlimit_confusions_111")

    #f1_scores_franc= calculate_f1(franc_confusion_matrix)
    #f1_scores_hierarch = calculate_f1(hierarch_confusion_matrix)

    #print_f1_table([ (f1_scores_franc, 'franc'),(f1_scores_hierarch, 'LIMIT-H')], latex=True)
