import json

import tqdm
from pymongo import MongoClient

from DictionaryDAO import _writeToDatabase
from domain.DictionaryMeaning import DictionaryMeaning

language_code = input('Language Code (es): ')

with open(f'JsonDictionaries/{language_code}-en-dictionary.json') as f:
    dictionary = json.load(f)

client = MongoClient()

for k, v in tqdm.tqdm(dictionary.items()):
    meanings = [DictionaryMeaning(ea['lemma'], ea['pos'], ea['meaning']).__dict__ for ea in v]
    _writeToDatabase(f'{language_code}_{k}', json.dumps(meanings), client)
