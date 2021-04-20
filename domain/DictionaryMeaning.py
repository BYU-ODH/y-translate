class DictionaryMeaning:
    def __init__(self, lemma: str, pos: str, meaning: str):
        self.lemma = lemma
        self.pos = pos
        self.meaning = meaning

    def __repr__(self):
        return f'{self.lemma}, {self.pos}, {self.meaning}'