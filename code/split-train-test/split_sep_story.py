import json
import os
import random

# ISO_PATH = "../../data/parallel/isocodes.json"
# isocodes = json.load(open(ISO_PATH))

CUTOFF = 1000
ROOT_PATH = f"../../data/parallel/wmt-pairs/filtered-{CUTOFF}/"

INPUT_PATH = ROOT_PATH
files = os.listdir(INPUT_PATH)

OUTPUT_PATH = ROOT_PATH + "wmt-format/"

with open(OUTPUT_PATH + "stats.txt","w") as fp:
    fp.write("pair" +  "\t"  + "train_size" + "\t" + "test_size" + "\n")

for f in files:
    if 'json' in f:

        empty = 0
        total = 0
        output = {}

        input_json = json.load(open(INPUT_PATH + f))
        stories = list(input_json.keys())

        # these stories can be randomly shuffled.
        random.shuffle(stories)

        num_stories = len(stories)

        for story in stories:
            languages = input_json[story].keys()

            # trim output[lang][test] for all languages, and remove any "" ones

            length = 0
            for l in output.keys():
                length = len(output[l]['test'])
                output[l]['temp'] = [] # reset temp

            for i in range(length):
                flag = True
                for l in output.keys():
                    if output[l]['test'][i] == "":
                        flag = False
                if flag: # only if both have non empty text, then we proceed.
                    for l in output.keys():
                        output[l]['temp'].append(output[l]['test'][i])

            for l in output.keys():
                output[l]['test'] = output[l]['temp']
                output[l]['temp'] = []
                # print("Test length: ", len(output[l]['test']))
                # print("Temp length: ", len(output[l]['temp']))

            for lang in languages:
                if lang not in output.keys():
                    output[lang] = {}
                    output[lang]['test'] = []
                    output[lang]['temp'] = []
                    output[lang]['train'] = []

                if len(output[lang]['test']) > CUTOFF:
                    output[lang]['train'] += input_json[story][lang] # a story will never be in both train/test.
                else:
                    output[lang]['test'] += input_json[story][lang]

        folders = os.listdir(OUTPUT_PATH)
        path =OUTPUT_PATH + f.replace(".json", "") + "/"
        os.makedirs(path, exist_ok=True)

        for l in output.keys():
            with open(path + "/" + l + ".train", 'w') as fp:
                pass
            with open(path + "/" + l + ".test", 'w') as fp:
                pass

        entries = 0
        for l in output.keys():
            entries_train = len(output[l]['train'])
            entries_test = len(output[l]['test'])
            break

        if entries_test > CUTOFF:
            entries_test = CUTOFF
        for i in range(entries_test):
            flag = True
            for l in output.keys():
                if output[l]['test'][i].strip() == "":
                    flag = False

            if flag == True: # neither of the entries are empty
                for l in output.keys():
                    with open(path + "/" + l + ".test", 'a') as fp:
                        fp.write(output[l]['test'][i].strip().replace('\r\n', '').replace('\r','').replace('\n', '') + "\n")

        for i in range(entries_train):
            flag = True
            for l in output.keys():
                if output[l]['train'][i].strip() == "":
                    flag = False

            if flag == True: # neither of the entries are empty
                for l in output.keys():
                    with open(path + "/" + l + ".train", 'a') as fp:
                        fp.write(output[l]['train'][i].strip().replace('\r\n', '').replace('\r','').replace('\n', '') + "\n")

        with open(OUTPUT_PATH + "stats.txt","a") as fp:
            fp.write(f.replace(".json", "") +  "\t"  + str(entries_train) + "\t" + str(entries_test) + "\n")
        # done writing   the text files.
        # now split them into 2 (train and test)
        # for l in output.keys():
        #     num_lines = 0
        #     with open(OUTPUT_PATH + folder + "/" + isocodes[l] + ".txt", 'r') as fp:
        #         num_lines = sum(1 for line in fp if line.rstrip())
        #     print(isocodes[l] + ".txt has ", num_lines, "lines ")
        #
        #     # writing first thousand+ in train, second thousand in test.
        #     with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".test", 'w') as f2:
        #         pass
        #     with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".train", 'w') as f1:
        #         pass
        #
        #     with open(OUTPUT_PATH + folder + "/" + isocodes[l] + ".txt", 'r') as fp:
        #         lineno = 0
        #         for line in fp:
        #             lineno += 1
        #
        #             if lineno <= CUTOFF :
        #                 with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".test", 'a') as f2:
        #                     f2.write(line)
        #             elif lineno > CUTOFF :
        #                 with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".train", 'a') as f1:
        #                     f1.write(line)
        # print()

#
