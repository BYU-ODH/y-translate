import stanfordnlp as stanfordnlp

from domain.SupportedLanguage import SupportedLanguage

lemmatizers = {k: stanfordnlp.Pipeline(lang=k, processors='tokenize,lemma') for k in SupportedLanguage}

def lemmatize(words: str, language_code: SupportedLanguage) -> [(str, str)]:
    """
    Converts either word or sentence to corresponding lemmas. Returns each tokens and lemmas a list of tuples: [(tok1, lem1), (tok2, lem2) ... ]. If unable to process words, returns empty list.
    :param words: 1 or more words
    :param language_code: language the words string is in
    :return: list of tokens and lemmas
    """
    nlp = lemmatizers[language_code]
    res = []
    try:
        doc = nlp(words)
        for sent in doc.sentences:
            for tok in sent.tokens:
                res.extend([(ea.text, ea.lemma) for ea in tok.words])
        return res
    except RuntimeError:
        return []
