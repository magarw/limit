import json
import os
import sys
import nltk
import random
import bz2
import pickle
import time
import _pickle as cPickle
from nltk.util import ngrams

from scipy import sparse
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import IncrementalPCA
#from sklearn.decomposition import MiniBatchSparsePCA
#from sklearn.decomposition import TruncatedSVD

import multiprocessing as mp

# import imblearn
from imblearn.over_sampling import SMOTE

# Pickle a file and then compress it into a file with extension
def compressed_pickle(title, data):
 with bz2.BZ2File(title + ".pbz2", "w") as f:
     cPickle.dump(data, f)

# Load any compressed pickle file
def decompress_pickle(file):
 data = bz2.BZ2File(file, "rb")
 data = cPickle.load(data)
 return data

def filter_lang(language_data, language):
    filtered_data = []
    for x in language_data:
        if x[1] == language:
            filtered_data.append(x)

    random.shuffle(filtered_data)
    return filtered_data

def train_test_split(language_data, lengths, filter_langs, experiment_no):

    DATA_PATH = "../../data/lms/data/"

    test_data = []
    train_data = []
    train_counts = {}

    f = open(DATA_PATH + "test.txt", "r")
    test_data_overall = [eval(x) for x in f.readlines()]
    entries = [x[0] for x in test_data_overall]
    testgold = [x[1] for x in test_data_overall]

    for lang in lengths.keys():
        sub_data = filter_lang(language_data, lang)

        # filter out the test examples from it..
        train_selection = list(filter(lambda tup: tup[0] not in entries, sub_data))
        test_selection = list(filter(lambda tup: tup[1] == lang, test_data_overall))

        # if lengths[lang] >= 200:
        #     test_samples = 100
        # else:
        #     test_samples = 10
        # train_selection = sub_data[test_samples:]

        test_data += test_selection
        train_data +=train_selection
        train_counts[lang] = len(train_selection)

    print(f"Total Data Size: {len(language_data)}")
    print(f"Test Data Size: {len(test_data)}")
    print(f"Train Data Size: {len(train_data)}")

    if False:
        print("writing train and test data to text files")
        with open(DATA_PATH + "train_67.txt", "w") as fp:
            for x in train_data:
                fp.write(str(x) + "\n")
        with open(DATA_PATH + "test_67.txt", "w") as fp:
            for x in test_data:
                fp.write(str(x) + "\n")
        print("done writing to txt")
    else:
        pass
        # f = open(DATA_PATH + "train.txt", "r")
        # train_data_ = []
        # for x in f.readlines():
        #     try:
        #         train_data_ += [eval(x)]
        #     except:
        #         continue

    # train_data = [tup if tup[1] in filter_langs for tup in train_data_]
    #train_data = filter(lambda tup: tup[1] in filter_langs, train_data_)

    print(f"Length of filtered train data: {len(train_data)}")
    a_time = time.time()
    print(time.strftime('%X %x %Z'))
    if True:
        X, y = add_features(train_data, experiment_no)
        print("returned from add features")

    else:
        print("X and y files detected")
        with open("../../data/lms/data/post_feat_X.pickle", "rb") as pickle_p:
            X = pickle.load(pickle_p)
        with open("../../data/lms/data/post_feat_y.pickle", "rb") as pickle_p:
            y = pickle.load(pickle_p)
    b_time = time.time()

    print(f"Time taken for loading X,y: {b_time - a_time:.2f}")

    print("SMOTING - LAST STEP")
    a_time = time.time()
    oversample = SMOTE(k_neighbors= 5)
    X, y = oversample.fit_resample(X, y)
    b_time = time.time()
    print(f"Time taken: {b_time - a_time:.2f}\nSMOTING complete")

    print("creating sparse matrix")
    a_time = time.time()
    print(time.strftime('%X %x %Z'))
    X_sparse = sparse.csr_matrix(X)
    b_time = time.time()
    print(f"Time taken: {b_time - a_time:.2f}")

    lda_time_start = time.time()
    print(time.strftime('%X %x %Z'))
    if True: #not os.path.exists("../../data/lms/data/projection_model.pickle"):
        print("SVD start")
        transformer = IncrementalPCA(n_components=1000, batch_size=1000) # change batch size to 100 later.
        transformer.fit(X_sparse)
        print("Fitting complete")
        with open(f"../../data/lms/data/projection_model_{experiment_no}.pickle", "wb") as p_pickle:
            pickle.dump(transformer, p_pickle)
        print("Explained Variance: ", transformer.explained_variance_ratio_.sum()) # 85+%
        print("fitting and saving done")
    else:
        with open("../../data/lms/data/projection_model.pickle", "rb") as p_pickle:
            transformer = pickle.load(p_pickle)

    X = transformer.transform(X_sparse)
    print("transformation of X done")
    lda_time_end = time.time()
    print(f"SVD time: {lda_time_end - lda_time_start:.2f}s ", )
    print("scaling")
    scaler = MinMaxScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    print("scaling complete")

    return X, y

def add_features_test(examples, experiment):
    data = []
    targets = []

    #print("starting pool now")
    with mp.Pool() as pool:
        data = list(pool.map(extract_faster_test, examples))
    #print(" pool over")

    for s in examples:
        targets.append(s[1])

    #print("loading pickles")
    with open(f"../../data/lms/data/projection_model_{experiment}.pickle", "rb") as pickle_p:
        lda_model = pickle.load(pickle_p)

    with open(f"../../data/lms/data/keys_{experiment}.pickle", "rb") as key_pickle:
        keys_original = pickle.load(key_pickle)

    #print("creating test data with same features as train")
    new_data = []
    a_time =time.time()
    with mp.Pool() as pool:
        new_data = pool.starmap(extract_newdata_faster, [(data[i], keys_original ) for i in range(len(data))])
    b_time = time.time()
    #print(f"Time taken: {b_time - a_time:.2f}")

    #print("transforming test data")
    lda_df = lda_model.transform(new_data)

    data = []
    for i in range(len(lda_df)):
        data.append((lda_df[i].reshape(1,-1), targets[i]))

    return data

def extract_newdata_faster(data_i, keys):
    sub_data = []
    data_i_keys = data_i.keys()
    for k in keys:
        if k in data_i_keys:
            sub_data.append(data_i[k])
        else:
            sub_data.append(0)
    return sub_data

def extract_faster(s):
    features = feature_extract(s[0])
    keys = set()
    for k in features.keys():
        keys.add(k)

    return (features, keys, s[1])

def extract_faster_test(s):
    features = feature_extract(s[0])
    return features

def add_features(examples, experiment_no):
    data = []
    targets = []
    keys = set()
    print("starting pool now")
    with mp.Pool() as pool:
        results = list(pool.map(extract_faster, examples))
    print(" pool over")

    for x in results:
        data.append(x[0])

    targets = [x[2] for x in results]
    for x in results:
        keys.update(x[1])

    print("Pre-SVD Shape: ", len(data), len(data[0]))     # length of keys per dictionary in data will be non-homogenous.combine data first.
    keys = list(keys) # save these feature keys.
    with open(f"../../data/lms/data/keys_{experiment_no}.pickle", "wb") as key_pickle:
        pickle.dump(keys, key_pickle)

    print("setting up data")
    new_data = []
    total_data = len(data)
    print("Total:", total_data)

    a_time =time.time()
    print(time.strftime('%X %x %Z'))
    with mp.Pool() as pool:
        new_data = pool.starmap(extract_newdata_faster, [(data[i], keys ) for i in range(total_data)])

    b_time = time.time()
    print(f"Time taken: {b_time - a_time:.2f}")

    print("Pre-Return/SVD Shape: ", len(new_data), len(new_data[0]), len(new_data[1]))

    return new_data, targets

def extract_ngrams(data, num):
    # n_grams = ngrams(nltk.word_tokenize(data), num)
    n_grams = ngrams(data, num) # character n-grams
    return [ ' '.join(grams) for grams in n_grams]

def extract_word_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [ ' '.join(grams) for grams in n_grams]

def feature_extract(input_text):
    features = dict()

    word_unigrams = dict(nltk.FreqDist(extract_word_ngrams(input_text, 1)))
    word_bigrams = dict(nltk.FreqDist(extract_word_ngrams(input_text, 2)))

    char_bigrams = dict(nltk.FreqDist(extract_ngrams(input_text, 2)))
    char_trigrams = dict(nltk.FreqDist(extract_ngrams(input_text, 3)))
    char_fourgrams = dict(nltk.FreqDist(extract_ngrams(input_text, 4)))

    features.update(word_unigrams)
    features.update(word_bigrams)

    features.update(char_bigrams)
    features.update(char_trigrams)
    features.update(char_fourgrams)

    return features
