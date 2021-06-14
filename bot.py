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
                                              callback_data=str(category.get_category_id()) + ' category'))

    bot.send_message(chat_id=message.chat.id, text="Категории товаров:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    callback = call.data.split(' ')

    if callback[1] == 'category':
        markup = types.InlineKeyboardMarkup()
        goods = good_dao.find_by_category_id(callback[0])

        for good in goods:
            markup.add(types.InlineKeyboardButton(text=good.get_product_name(),
                                                  callback_data=str(good.get_product_id()) + ' good'))
        bot.send_message(chat_id=call.message.chat.id, text='Представлены товары данной категории: ',
                         reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        good = good_dao.find_by_id(callback[0])
        markup.add(types.InlineKeyboardButton(text='Добавить в корзину',
                                              callback_data='test'))

        bot.send_message(chat_id=call.message.chat.id,
                         text='<b>{0}</b>\n Вес: {1} мл.\n Цена: {2} руб'.format(
                             good.get_product_name(),
                             str(good.get_weight()),
                             str(good.get_price())),
                         parse_mode='html',
                         reply_markup=markup)
        bot.send_photo(call.message.chat.id, good.get_url())


bot.polling(none_stop=True)
