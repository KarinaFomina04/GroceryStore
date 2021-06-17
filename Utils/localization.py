import configparser
import os


class Localization:
    locale = 'en'
    list_available_locales = ['en', 'ru']

    @classmethod
    def init_locale(cls, lang):
        if lang in cls.list_available_locales:
            cls.locale = lang

    @classmethod
    def get_message(cls, key):
        config = configparser.ConfigParser(interpolation=None)
        config.read(os.path.abspath(os.path.join("Locale", cls.locale + ".ini")), encoding="UTF-8")
        return config["MESSAGES"][key].replace("\\n", "\n")
