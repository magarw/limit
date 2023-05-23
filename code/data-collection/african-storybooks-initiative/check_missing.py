import os
LOG_PATH = "../../../data/raw/african-storybooks-initiative/logs/"

logfiles = os.listdir(LOG_PATH)
total_count = len(logfiles)
missing_count = 0
for file in logfiles:
    f = open(LOG_PATH + file)
    f = f.read()
    if 'MISSING' in f:
        missing_count += 1
    else:
        print(file)
print(missing_count)
print(total_count)
