filename = "../../data/language-id/monolingual/ach.txt"

f = open(filename)
data = [x.strip() for x in f.readlines()]

character_frequencies = {}

for sentence in range(len(data)):
    for character in data[sentence]:
        character = character.lower()
        if character in character_frequencies.keys():
            character_frequencies[character] += 1
        else:
            character_frequencies[character] = 1


character_frequencies = dict(sorted(character_frequencies.items(), key=lambda item: item[1]))
for key in character_frequencies.keys():
    print(f"{key}: {character_frequencies[key]}")
