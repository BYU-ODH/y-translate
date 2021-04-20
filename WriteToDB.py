import json

import tqdm

from DictionaryDAO import appendMeaning, _getConn, _writeToTranslationsTable
from Utils import generateKey
from domain.DictionaryMeaning import DictionaryMeaning

language_code = input('Language Code (es): ')

with open(f'JsonDictionaries/{language_code}-en-dictionary.json') as f:
    dictionary = json.load(f)

conn = None
cur = None

try:
    conn = _getConn()
    cur = conn.cursor()

    headwordString = """INSERT INTO headwords VALUES (%s) ON CONFLICT DO NOTHING;"""
    meaningString = """INSERT INTO meanings(meaning, headword) VALUES (%s, %s);"""

    for k, v in tqdm.tqdm(dictionary.items()):
        key = generateKey(k, language_code)
        cur.execute(headwordString, (key,))
        meanings = [DictionaryMeaning(ea['lemma'], ea['pos'], ea['meaning']) for ea in v]
        for meaning in meanings:
            value = json.dumps(meaning.__dict__)
            if k == 'Abiyán':
                asdf = 12
            cur.execute(meaningString, (value, key))
    conn.commit()
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
