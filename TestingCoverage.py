import json

import requests as r
import tqdm

filename = input('Test filename: ')
language_code = input('Language code (es): ')

with open(filename) as f:
    raw_test = f.read()

s = ''.join(ea for ea in raw_test if ea.isalpha() or ea.strip() == '')
s = s.replace('\n', ' ')
s = s.replace('\t', ' ')

failed = set()
success = set()

print('Querying api with each word')

for word in tqdm.tqdm(set(s.split(' '))):
    if word.strip() == '':
        continue
    res = r.get(f'http://localhost:8000/translate/{language_code}/{word}')
    resBody = json.loads(res.text)
    if len(resBody) == 0:
        failed.add(word)
    else:
        success.add(word)

print(f'Failed: {len(failed)}')
print(*(sorted(failed)))
print(f'Success: {len(success)}')
print(*sorted(success))
print(f'% passed: {round(100 * len(success) / (len(failed) + len(success)), 2)}')