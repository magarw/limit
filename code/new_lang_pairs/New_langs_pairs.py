
mpairs = []
mlangs = ["eng"]
with open("Microsoft.txt","r") as r:
    lines = r.read().splitlines()
    for line in lines:
        lang = line.split(" ")[0].split("-")[0]
        if lang not in mlangs:
            mlangs.append(lang)
        pair = f"eng-{lang}"
        mpairs.append(pair)
        pair = f"{lang}-eng"
        mpairs.append(pair)

fpairs = []
flangs = []
langtocode = {}
with open("Flores.txt","r") as r:
    lines = r.read().splitlines()
    for line in lines:
        lang = line.split("\t")[0]
        code = line.split("\t")[-1].split("_")[0]
        if code not in flangs:
            flangs.append(code)
        if lang not in langtocode:
            langtocode[lang] = code
    for lang1 in flangs:
        for lang2 in flangs:
            if lang1 != lang2:
                pair = f"{lang1}-{lang2}"
                fpairs.append(pair)
                pair = f"{lang2}-{lang1}"
                fpairs.append(pair)

opairs = []
olangs = []
ocodes = ["eng"]
with open("Opus.txt","r") as r:
    lines = r.read().splitlines()
    for line in lines:
        code1 = line.split(" ")[0]
        lang1 = line.split(" ")[1]
        if lang1 not in olangs:
            olangs.append(lang1)
            flag = False
            for flang in langtocode:
                if lang1 in flang:
                    ocodes.append(langtocode[flang])
                    flag = True
                    break
            if not flag:
                ocodes.append(code1)
        if len(line.split(" ")) > 6:
            code2 = line.split(" ")[5]
            lang2 = line.split(" ")[6]
            if lang2 not in olangs:
                olangs.append(lang2)
                flag = False
                for flang in langtocode:
                    if lang2 in flang:
                        ocodes.append(langtocode[flang])
                        flag = True
                        break
                if not flag:
                    ocodes.append(code2)
    
    for lang in ocodes:
        pair = f"eng-{lang}"
        opairs.append(pair)
        pair = f"{lang}-eng"
        opairs.append(pair)

ourpairs = []
with open("Ours.txt","r") as r:
    lines = r.read().splitlines()
    ourpairs.extend(lines)

ourlangs = []
for pair in ourpairs:
    srclang = pair.split("-")[0]
    tgtlang = pair.split("-")[1]
    if srclang not in ourlangs:
        ourlangs.append(srclang)
    if tgtlang not in ourlangs:
        ourlangs.append(tgtlang)

mcnt = 0
fcnt = 0
ocnt = 0
for ourlang in ourlangs:
    if ourlang not in mlangs:
        mcnt += 1
    if ourlang not in flangs:
        fcnt += 1
    if ourlang not in ocodes:
        ocnt += 1

print(f"# of New lanuages in compared to Microsoft: {mcnt}")
print(f"# of New lanuages in compared to Flores: {fcnt}")
print(f"# of New lanuages in compared to Opus: {ocnt}")

mcnt = 0
fcnt = 0
ocnt = 0
for ourpair in ourpairs:
    if ourpair not in mpairs:
        mcnt += 1
    if ourpair not in fpairs:
        fcnt += 1
    if ourpair not in opairs:
        ocnt += 1

print(f"# of New lanuage pairs in compared to Microsoft: {mcnt}")
print(f"# of New lanuage pairs in compared to Flores: {fcnt}")
print(f"# of New lanuage pairs in compared to Opus: {ocnt}")