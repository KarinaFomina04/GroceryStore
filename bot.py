import telebot
import configparser
import Dao.category_dao

from telebot import types

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])

category_dao = Dao.category_dao.CategoryDAO()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в {0.first_name}!\n Введите /category для вывода категорий "
                                      "товаров.".format(bot.get_me()))


@bot.message_handler(commands=['category'])
def getCategory(message):
    markup = types.InlineKeyboardMarkup()
    categories = category_dao.find_all()

    for category in categories:
        markup.add(types.InlineKeyboardButton(text=category.get_category_name(),
                                              callback_data=category.get_category_name()))

    bot.send_message(chat_id=message.chat.id, text="Категории товаров:", reply_markup=markup)


bot.polling(none_stop=True)
