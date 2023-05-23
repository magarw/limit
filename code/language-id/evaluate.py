import os
import nltk
import pickle
import random
import time
from features import *
import pandas as pd
import multiprocessing as mp
from functools import partial
from sklearn.naive_bayes import MultinomialNB

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

def prediction_classify(x):
    prediction = classifier.classify(x[0])
    return (prediction, x[1])

if __name__ == "__main__":
    # Step 0: Constants
    experiment = 104
    MODEL_PATH = f"../../data/lms/test{experiment}"
    TEST_PATH  = f"../../data/lms/data/test.txt"
    start_time = time.time()

    # Step 1: Load the Naive Bayes model
    classifier = pickle.load(open(MODEL_PATH, 'rb'))
    labels = classifier.classes_

    # Step 2: Load the test set (which should be a text file, just like new text files)
    # and do the prediction.
    f = open(TEST_PATH)
    test_data_ = [eval(x) for x in f.readlines()]

    # Filter test data.
    test_data = list(filter(lambda tup: tup[1] in labels, test_data_))

    a_time = time.time()
    test_featurized = add_features_test(test_data, experiment)
    b_time = time.time()

    # Step 4: Confusion Matrix Populate
    confusion_matrix = pd.DataFrame(0, index=labels, columns=labels)
    results = []
    i = 0
    X = [x[0] for x in test_featurized]
    with mp.Pool() as pool:
        predictions = list(pool.map(classifier.predict, X))

    results = []
    for i in range(len(predictions)):
        results.append((predictions[i], test_featurized[i][1]))

    # calculate accuracy with results.
    print("processing complete")
    acc = 0
    total = len(results)
    for i in range(total):
        prediction = results[i][0][0]
        actual = results[i][1]
        print(prediction, actual)
        confusion_matrix.loc[prediction, actual] += 1
        if prediction == actual:
            acc += 1

    confusion_matrix.to_csv(f"../../data/lms/data/confusion_matrix_{experiment}.csv")
    print(f"Accuracy {acc}/{total}: {acc*100/total:.2f}%")

    f1 = calculate_f1(confusion_matrix)
    print(f1)
    end_time = time.time()
    print(f"Total Script Run Time: {end_time - start_time}s")
