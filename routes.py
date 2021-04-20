import Translator
from domain.SupportedLanguage import SupportedLanguage
from main import app


@app.get('/')
async def root():
    return {"message": "Hello, World!"}


@app.get('/translate/{language_code}/{words}')
async def translate(language_code: SupportedLanguage, words: str):
    return Translator.Translate(words, language_code)

#
# @app.post('/add-translation')
# async def add_translation()