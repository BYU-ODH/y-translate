from Utils import generateKey
from config import config
from domain.DictionaryEntry import DictionaryEntry
from domain.DictionaryMeaning import DictionaryMeaning
from domain.SupportedLanguage import SupportedLanguage
import json
# from pymongo import MongoClient
import psycopg2

def _getConn():
    conn = None
    try:
        conn = psycopg2.connect(host=config['host'],
                                database=config['database'],
                                user=config['user'],
                                password=config['password'],)
        return conn
    except:
        if conn is not None:
            conn.close()
        return None


def _readFromTranslationsTable(key: str) -> dict:
    conn = None
    cur = None
    try:
        conn = _getConn()

        cur = conn.cursor()

        execString = """SELECT meaning FROM meanings WHERE headword=%s;"""

        cur.execute(execString, (key,))

        res = cur.fetchall()

        cur.close()

        return res

    except:
        return {}
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


# def _overwriteToDatabase(key: str, value: str, client: MongoClient):
#     client[config['db_name']].translations.update_one({'_id': key}, {'$set': {'meanings': value}})
#
#
def _writeToTranslationsTable(key: str, value: str):
    conn = None
    cur = None
    try:
        conn = _getConn()

        cur = conn.cursor()

        execString = """INSERT INTO headwords VALUES (%s) ON CONFLICT DO NOTHING;"""
        cur.execute(execString, (key,))

        execString = """INSERT INTO meanings(meaning, headword) VALUES (%s, %s);"""
        cur.execute(execString, (value, key))

        cur.close()

        conn.commit()

        return True

    except:
        return False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def appendMeaning(lemma: str, language_code: SupportedLanguage, meaning: DictionaryMeaning):
    """
    Appends meaning to lemma and language code combination in translations table. If lemma-code does
    exist, it create them first.
    """
    _writeToTranslationsTable(generateKey(lemma, language_code), json.dumps(meaning.__dict__))


def getDictionaryEntry(lemma: str, language_code: SupportedLanguage) -> DictionaryEntry:
    # with open(f'JsonDictionaries/{language_code}-en-dictionary.json') as f:
    #     dictionary = json.load(f)
    res = DictionaryEntry(lemma, [])
    dbRes = _readFromTranslationsTable(generateKey(lemma, language_code))
    if dbRes is None:
        return None
    print(dbRes)
    for ea in dbRes:
        j = json.loads(ea[0])
        res.meanings.append(DictionaryMeaning(j['lemma'], j['pos'], j['meaning']))
    return res

# print(getDictionaryEntry('élder', SupportedLanguage.es))
# print(getDictionaryEntry('elder', SupportedLanguage.es))
# appendMeaning('élder', SupportedLanguage.es, DictionaryMeaning('élder', '{n}', '(a representative of the Church of Jesus Christ of Latter-day Saints)'))
# appendMeaning('élder', SupportedLanguage.es, DictionaryMeaning('élder', '{n}', '(an older person)'))
# print(getDictionaryEntry('élder', SupportedLanguage.es))

# from pprint import pprint
# q = input('Spanish word: ')
# pprint(getDictionaryEntry(q, SupportedLanguage.es))