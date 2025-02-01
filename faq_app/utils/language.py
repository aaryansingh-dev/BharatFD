from logging import Logger

from googletrans import Translator

LANGUAGES = ['en', 'hi', 'bn', 'ta', 'te', 'mr']

translator = Translator()


def translate(text, lang):
    try:
        return translator.translate(text, dest=lang).text
    except Exception as e:
        print('Error translating text: ', text, ' to language: ', lang)
        return text
