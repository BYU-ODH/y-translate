from domain.DictionaryMeaning import DictionaryMeaning


class DictionaryEntry:
    def __init__(self, lemma: str, meanings: [DictionaryMeaning]):
        self.lemma = lemma
        self.meanings = meanings

    def __repr__(self):
        return f'{self.lemma}: {[ea.__repr__() for ea in self.meanings]}'