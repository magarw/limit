import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load confusion matrix
input_path = "../../../data/lms/data/franc_confusion_matrix_latest.csv"
franc_matrix = pd.read_csv(input_path, index_col=0)
#print(franc_matrix.sum())
#print(len(franc_matrix.columns)) # 357 columns
#print(len(franc_matrix.index)) # 388 predictions

# What percentage of languages are new/unsupported by Franc?
new_langs = set(franc_matrix.columns).difference(set(franc_matrix.index))
# print(len(new_langs)) # 224 new languages.

# What percentage of UND predictions by Franc are correct?
und_predictions = franc_matrix.loc['und', :]
total = und_predictions.sum() # 1525 hits.
correct = 0
ideal = 0
for ix in und_predictions.index:
    if ix not in franc_matrix.index:
        ideal += franc_matrix[ix].sum()
        correct += 1
print(f"Franc UND predictions (correct/total): {correct}/{total}. Ideal: {ideal}")
#Franc UND predictions (correct/total): 224/1525 (14.68%)

# Making a heatmap for this confusion matrix for the appendix.
# fig, ax = plt.subplots(figsize=(50, 50))
# ax = sns.heatmap(franc_matrix, linewidth=0.0, cmap='cubehelix')
# cbar = ax.collections[0].colorbar
# cbar.ax.tick_params(labelsize=50)
# plt.savefig("../../../data/lms/data/franc_confusion_matrix_latex.eps", format='eps')

# Sorted list of confused entries:
CUTOFF = 0.7
output = ""
for i in range(franc_matrix.shape[1]):
    actual_label = franc_matrix.columns[i]
    predictions = franc_matrix.loc[:, actual_label]
    total = sum(predictions)
    predictions_ratios = predictions/total
    predictions_filt = predictions_ratios[predictions_ratios > CUTOFF]
    if actual_label in predictions_filt.index:
        predictions_filt = predictions_filt.drop(actual_label)
    if "und" in predictions_filt.index:
        predictions_filt = predictions_filt.drop("und")
    if "_" in actual_label and actual_label.split('_')[0] in predictions_filt.index:
        predictions_filt = predictions_filt.drop(actual_label.split('_')[0])
    if len(predictions_filt.index) > 0:
        for k in predictions_filt.keys():
            output += f" {actual_label}-{k}, {predictions_filt[k]} \n"
print(output)
