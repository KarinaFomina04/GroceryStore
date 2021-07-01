import telebot
import configparser

from enum import Enum
from Dao.good_dao import GoodDAO
from Dao.category_dao import CategoryDAO
from Dao.order_dao import OrderDAO
from telebot import types
from Utils.localization import Localization

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])

category_dao = CategoryDAO()
good_dao = GoodDAO()
order_dao = OrderDAO()
is_confirm = False


@bot.message_handler(commands=['start'])
def start(message):
    Localization.init_locale(message.from_user.language_code)
    bot.send_message(message.chat.id, Localization.get_message('start_message').format(bot.get_me()))


@bot.message_handler(commands=['cart'])
def get_cart(message):
    Localization.init_locale(message.from_user.language_code)
    orders = order_dao.find_orders(message.from_user.id)
    text_message = Localization.get_message('your_orders')
    if (orders is not None) and (len(orders) != 0):
        total_price = 0
        for order in orders:
            text_message = text_message + order.get_html_order()
            total_price = total_price + order.get_price() * order.get_count()
        text_message = text_message + Localization.get_message('total_price').format(
            str(total_price)) + Localization.get_message('properties_added')
        bot.send_message(chat_id=message.chat.id, text=text_message, parse_mode='html')
    else:
        bot.send_message(chat_id=message.chat.id, text=Localization.get_message('empty_cart'))


@bot.message_handler(commands=['category'])
def getCategory(message):
    Localization.init_locale(message.from_user.language_code)
    markup = types.InlineKeyboardMarkup()
    categories = category_dao.find_all()

    for category in categories:
        markup.add(types.InlineKeyboardButton(text=category.get_category_name(),
                                              callback_data=str(category.get_category_id()) + ' category'))

    bot.send_message(chat_id=message.chat.id, text=Localization.get_message('good_categories'), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    Localization.init_locale(call.from_user.language_code)
    callback = call.data.split(' ')

    if callback[1] == 'category':
        markup = types.InlineKeyboardMarkup()
        goods = good_dao.find_by_category_id(callback[0])

        for good in goods:
            markup.add(types.InlineKeyboardButton(text=good.get_product_name(),
                                                  callback_data=str(good.get_product_id()) + ' good'))
        bot.send_message(chat_id=call.message.chat.id, text=Localization.get_message('show_goods'),
                         reply_markup=markup)
    elif callback[1] == 'good':
        markup = types.InlineKeyboardMarkup()
        good = good_dao.find_by_id(callback[0])
        markup.add(types.InlineKeyboardButton(text=Localization.get_message('add_to_cart'),
                                              callback_data=str(good.get_product_id()) + ' order'))

        bot.send_message(chat_id=call.message.chat.id,
                         text=good.get_html_good(),
                         parse_mode='html',
                         reply_markup=markup)
        bot.send_photo(call.message.chat.id, good.get_url())
    else:
        order_dao.add_to_cart(call.from_user.id, callback[0])
        bot.send_message(chat_id=call.message.chat.id, text=Localization.get_message('order_added'))


@bot.message_handler(commands=['confirm'])
def confirm(message):
    Localization.init_locale(message.from_user.language_code)
    order_dao.clear_cart(message.from_user.id)
    global is_confirm
    is_confirm = True
    bot.send_message(chat_id=message.chat.id, text=Localization.get_message('properties_confirm').format('Ф.И.О'))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global is_confirm
    if is_confirm:
        bot.send_message(chat_id=message.chat.id, text='test')
        is_confirm = False


bot.polling(none_stop=True)
