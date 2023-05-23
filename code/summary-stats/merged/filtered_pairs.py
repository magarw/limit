
import json

FILTER = 10
num_filtered = 0
out_file = open(f"../../../data/parallel/filtered{FILTER}.txt", 'w')
dashed = 0
dashed_ = 0
with open("../../../data/parallel/pair_lengths.txt", 'r') as fp:
    lang_pairs = {}
    data = fp.readlines()

    total = len(data)
    languages = set()
    for d in data:
        d_ = d.strip().split("\t")
        key = d_[0]
        value = int(d_[1])

        if '-' in key:
            dashed += 1

            key_p = key[1:-1].split(',')
            blacklist = ['Kannada','Telugu', 'Hindi', 'English', 'Tamil', 'Bengali', 'Marathi', 'Odia']
            if '-' in key_p[0]:
                flag_ = True

                for b in blacklist:
                    if b in key_p[0]:
                        flag = False
                if flag == False:
                    dashed_ += 1
                else:
                    print("FLAG: ", key_p[0])

            else:
                flag = True
                for b in blacklist:
                    if b in key_p[1]:
                        flag = False
                if flag == False:
                    dashed_ += 1
                else:
                    print("FLAG: ", key_p[1])


        if value >= FILTER :
            out_file.write(d)
            num_filtered += 1
            #print(key, value)

            languages.add(key_p[0])
            languages.add(key_p[1])

    out_file.close()

    print(f"Pairs extracted (>={FILTER} pages: {num_filtered}/{total} i.e. {num_filtered*100/total:.2f}%")
    print(f"Pairs dashed: {dashed}/{total} i.e. {dashed*100/total:.2f}%")
    print(f"Pairs easylangID dashed: {dashed_}/{total} i.e. {dashed_*100/total:.2f}%")

    print(f"Number of unique languages: {len(languages)}")
    # print(languages)
