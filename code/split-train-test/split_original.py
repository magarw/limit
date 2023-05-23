import json
import os

ISO_PATH = "../../data/parallel/isocodes.json"
isocodes = json.load(open(ISO_PATH))

ROOT_PATH = "../../data/parallel/selected-round1/"
INPUT_PATH = ROOT_PATH + "base/"
OUTPUT_PATH = ROOT_PATH + "wmt-format/"

files = os.listdir(INPUT_PATH)
for f in files:
    if 'json' in f:
        empty = 0
        total = 0
        input_json = json.load(open(INPUT_PATH + f))
        stories = input_json.keys()
        num_stories = len(stories)

        output = {}

        for story in stories:
            languages = input_json[story].keys()

            for lang in languages:
                if lang not in output.keys():
                    output[lang] = []
                output[lang] += input_json[story][lang]

        folders = os.listdir(OUTPUT_PATH)
        for folder in folders:
            this = True
            for l in output.keys():
                if isocodes[l] not in folder:
                    this = False
                    continue

            if this: # correct folder found.
                for l in output.keys():
                    with open(OUTPUT_PATH + folder + "/" + isocodes[l] + ".txt", 'w') as fp:
                        pass

                entries = 0
                for l in output.keys():
                    entries = len(output[l])
                    break

                for i in range(entries):
                    flag = True
                    for l in output.keys():
                        if output[l][i].strip() == "":
                            flag = False

                    if flag == True: # none of the entries are empty
                        for l in output.keys():
                            with open(OUTPUT_PATH + folder + "/" + isocodes[l] + ".txt", 'a') as fp:
                                fp.write(output[l][i].strip().replace('\r\n', '').replace('\r','').replace('\n', '') + "\n")


                # done writing the text files.
                # now split them into 2 (train and test)
                for l in output.keys():
                    num_lines = 0
                    with open(OUTPUT_PATH + folder + "/" + isocodes[l] + ".txt", 'r') as fp:
                        num_lines = sum(1 for line in fp if line.rstrip())
                    print(isocodes[l] + ".txt has ", num_lines, "lines ")

                    # writing first thousand in train, second thousand in test.
                    train_size = 1000
                    test_size = 1000

                    with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".test", 'w') as f2:
                        pass
                    with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".train", 'w') as f1:
                        pass

                    with open(OUTPUT_PATH + folder + "/" + isocodes[l] + ".txt", 'r') as fp:
                        lineno = 0
                        for line in fp:
                            lineno += 1

                            if lineno < 1001 :
                                with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".test", 'a') as f2:
                                    f2.write(line)
                            elif lineno > 1000 :
                                with open(OUTPUT_PATH  + folder + "/" + isocodes[l] + ".train", 'a') as f1:
                                    f1.write(line)
                print()




#
