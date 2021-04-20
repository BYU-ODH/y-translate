from domain.SupportedLanguage import SupportedLanguage


def generateKey(lemma: str, language_code: SupportedLanguage) -> str:
    return language_code + '_' + lemma