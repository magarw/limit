import pandas
import seaborn as sn
import matplotlib.pyplot as plt
import time

experiment = 24
PATH = f"../../data/lms/data/confusion_matrix_{experiment}.csv"
confusion_matrix = pandas.read_csv(PATH, index_col=0)
plt.figure(figsize=(200,200))
sn.set(font_scale=5) # for label size

a_time = time.time()
mismatches = []
for i in range(confusion_matrix.shape[0]):
    for j in range(confusion_matrix.shape[1]):
        if confusion_matrix.index[i] != confusion_matrix.columns[j] and confusion_matrix.iloc[i][j] > 0:
            mismatches.append((confusion_matrix.index[i], confusion_matrix.columns[j], confusion_matrix.iloc[i][j]))
b_time = time.time()
print(f"Time taken (mismatches): {b_time - a_time:.2f}") #Time taken: 6s

a_time = time.time()
sorted_mismatches = sorted(mismatches, key=lambda x: x[2], reverse=True)
with open(f"../../data/lms/data/sorted_{experiment}.txt", "w") as fp:
    for x in sorted_mismatches:
        fp.write(x[0] + "\t"+ x[1] + "\t"+ str(x[2]) + "\n")
b_time = time.time()
print(f"Time taken (sorting): {b_time - a_time:.2f}") #Time taken: 0s (very fast)

a_time = time.time()
sn.heatmap(confusion_matrix, annot=True, annot_kws={"size": 16}) # font size
plt.savefig(f"../../data/lms/data/heatmap_{experiment}.png")
b_time = time.time()
print(f"Time taken (heatmapping): {b_time - a_time:.2f}") #Time taken: 120s

# calculate precision and recall.
precisions = []
for i in range(confusion_matrix.shape[0]):
    total = sum(confusion_matrix.iloc[i, :])
    tp = 0
    for j in range(confusion_matrix.shape[1]):
        # True Positive
        if confusion_matrix.index[i] != confusion_matrix.columns[j] and confusion_matrix.iloc[i][j] > 0:
            tp += confusion_matrix.iloc[i, j]
    if total != 0:
        precisions.append((confusion_matrix.index[i], tp/total))
        #print(f"{confusion_matrix.index[i]}: {tp/total:.2f}")
    else:
        precisions.append((confusion_matrix.index[i], -1))
        #print(f"{confusion_matrix.index[i]}: 0")
sorted_precisions = sorted(precisions, key=lambda x: x[1], reverse=True)
with open(f"../../data/lms/data/precisions_{experiment}.txt", "w") as fp:
    for x in sorted_precisions:
        fp.write(str(x) + "\n")
