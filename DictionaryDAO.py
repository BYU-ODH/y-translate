from bson import ObjectId

from Utils import generateKey
from config import config
from domain.DictionaryEntry import DictionaryEntry
from domain.DictionaryMeaning import DictionaryMeaning
from domain.SupportedLanguage import SupportedLanguage
import json
from pymongo import MongoClient


def _readFromDatabase(key: str, client: MongoClient) -> dict:
    return client[config['db_name']].translations.find_one({'_id': key})


def _overwriteToDatabase(key: str, value: str, client: MongoClient):
    client[config['db_name']].translations.update_one({'_id': key}, {'$set': {'meanings': value}})


def _writeToDatabase(key: str, value: str, client: MongoClient):
    client[config['db_name']].translations.insert_one({'_id': key, 'meanings': value})


def appendMeaning(lemma: str, language_code: SupportedLanguage, meaning: DictionaryMeaning):
    client = MongoClient()
    dbRes = _readFromDatabase(generateKey(lemma, language_code), client)
    curEntry = []
    if dbRes is not None:
        for ea in json.loads(dbRes['meanings']):
            curEntry.append(
                DictionaryMeaning(ea['lemma'], ea['pos'], ea['meaning']))
    curEntry.append(meaning)
    curEntry = [ea.__dict__ for ea in curEntry]
    if dbRes is None:
        _writeToDatabase(generateKey(lemma, language_code), json.dumps(curEntry), client)
    else:
        _overwriteToDatabase(generateKey(lemma, language_code), json.dumps(curEntry), client)


def getDictionaryEntry(lemma: str, language_code: SupportedLanguage) -> DictionaryEntry:
    # with open(f'JsonDictionaries/{language_code}-en-dictionary.json') as f:
    #     dictionary = json.load(f)
    client = MongoClient()
    res = DictionaryEntry(lemma, [])
    dbRes = _readFromDatabase(generateKey(lemma, language_code), client)
    if dbRes is None:
        return None
    for ea in json.loads(dbRes['meanings']):
        res.meanings.append(DictionaryMeaning(ea['lemma'], ea['pos'], ea['meaning']))
    return res

# print(getDictionaryEntry('élder', SupportedLanguage.es))
# appendMeaning('élder', SupportedLanguage.es, DictionaryMeaning('élder', '{n}', '(a representative of the Church of Jesus Christ of Latter-day Saints)'))
# print(getDictionaryEntry('élder', SupportedLanguage.es))

# from pprint import pprint
# q = input('Spanish word: ')
# pprint(getDictionaryEntry(q, SupportedLanguage.es))