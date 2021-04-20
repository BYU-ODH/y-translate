import re

CUSTOM_DELIM = 'Ɖ'

filename = input("File name (.txt): ")
language_code = input("Language code (es): ")

with open(filename) as f:
    lines = f.read().split('\n')

dictionary = {}

for line in lines:
    if line.strip() == '':
        continue
    if 'SEE' in line:
        continue
    print(line)
    eng = ''
    pos = ''
    mean = ''
    i = 0
    while line[i] not in '({/' + CUSTOM_DELIM:
        eng += line[i]
        i += 1
    while line[i] not in '({' + CUSTOM_DELIM:
        i += 1
    if line[i] == '{':
        while line[i] not in '(/' + CUSTOM_DELIM:
            pos += line[i]
            i += 1
    while line[i] not in '({' + CUSTOM_DELIM:
        i += 1
    if line[i] == '(':
        while line[i] not in '/' + CUSTOM_DELIM:
            mean += line[i]
            i += 1
    while line[i] == CUSTOM_DELIM:
        i += 1

    heads = [ea.strip() for ea in re.findall(r'(?:,|^) ([^/{]*)', line[i:])]
    eng = eng.strip()
    pos = pos.strip()
    mean = mean.strip()
    for head in heads:
        if head not in dictionary:
            dictionary[head] = list()
        dictionary[head].append({'lemma': eng,
                                 'pos': pos,
                                 'meaning': mean})

import json

with open(f'JsonDictionaries/{language_code}-en-dictionary.json', 'w') as f:
    json.dump(dictionary, f, ensure_ascii=False)