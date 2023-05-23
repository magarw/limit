import json
import os

ISO_PATH = "../../data/parallel/isocodes.json"
isocodes = json.load(open(ISO_PATH))

ROOT_PATH = "../../data/parallel/selected-round1/"
INPUT_PATH = ROOT_PATH + "wmt-format/"

folders = os.listdir(INPUT_PATH)
for folder in folders:
    if '-' in folder:
        x1 = folder.split('-')[0]
        x2 = folder.split('-')[1]

        f1 = open(INPUT_PATH + f'{x1}-{x2}/{x1}.test')
        f2 = open(INPUT_PATH + f'{x1}-{x2}/{x2}.test')
        l1 = f1.readlines()
        l2 = f2.readlines()
        assert len(l1) == len(l2)
        print(len(l1), f'test {x1}-{x2}')

        f1 = open(INPUT_PATH + f'{x1}-{x2}/{x1}.train')
        f2 = open(INPUT_PATH + f'{x1}-{x2}/{x2}.train')
        l1 = f1.readlines()
        l2 = f2.readlines()
        assert len(l1) == len(l2)
        print(len(l1), f'train {x1}-{x2}')
