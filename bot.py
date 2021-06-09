import telebot
import configparser

from Dao.good_dao import GoodDAO
from Dao.category_dao import CategoryDAO
from telebot import types

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])

category_dao = CategoryDAO()
good_dao = GoodDAO()


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
                                              callback_data=category.get_category_id()))

    bot.send_message(chat_id=message.chat.id, text="Категории товаров:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    markup = types.InlineKeyboardMarkup()
    goods = good_dao.find_by_id(call.data)

    for good in goods:
        markup.add(types.InlineKeyboardButton(text=good.get_product_name(),
                                              callback_data=good.get_product_id()))
    bot.send_message(chat_id=call.message.chat.id, text='Представлены товары данной категории: ', reply_markup=markup)


bot.polling(none_stop=True)
