import telebot
import configparser

from Dao.good_dao import GoodDAO
from Dao.category_dao import CategoryDAO
from Dao.order_dao import OrderDAO
from telebot import types

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])

category_dao = CategoryDAO()
good_dao = GoodDAO()
order_dao = OrderDAO()


def get_measure(category):
    if category == 3:
        return " мл."
    else:
        return " г."


def get_html_good(good):
    return '<b>{0}</b>\n Вес: {1}{3}\n Цена: {2} руб.\n'.format(
        good.get_product_name(),
        str(good.get_weight()),
        str(good.get_price()),
        get_measure(good.get_category()))


def get_html_order(order):
    return '<b>{0}</b>\n Вес: {1}{4}\n Количество единиц: {2} \n Цена: {3} руб.\n\n'.format(
        order.get_product_name(),
        str(order.get_weight()),
        str(order.get_count()),
        str(order.get_price() * order.get_count()),
        get_measure(order.get_category()))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в {0.first_name}!\n Нажмите на /category для вывода категорий "
                                      "товаров.\n Чтобы увидеть выбранные Вами товары, нажмите на /cart."
                     .format(bot.get_me()))


@bot.message_handler(commands=['cart'])
def get_cart(message):
    orders = order_dao.find_orders(message.from_user.id)
    text_message = "<b>Ваши товары:</b>\n\n"
    if (orders is not None) and (len(orders) != 0):
        total_price = 0
        for order in orders:
            text_message = text_message + get_html_order(order)
            total_price = total_price + order.get_price() * order.get_count()
        text_message = text_message + "Итоговая стоимость: " + str(total_price) + " руб."
        bot.send_message(chat_id=message.chat.id, text=text_message, parse_mode='html')
    else:
        bot.send_message(chat_id=message.chat.id, text="Ваша корзина пуста!")


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
    elif callback[1] == 'good':
        markup = types.InlineKeyboardMarkup()
        good = good_dao.find_by_id(callback[0])
        markup.add(types.InlineKeyboardButton(text='Добавить в корзину',
                                              callback_data=str(good.get_product_id()) + ' order'))

        bot.send_message(chat_id=call.message.chat.id,
                         text=get_html_good(good),
                         parse_mode='html',
                         reply_markup=markup)
        bot.send_photo(call.message.chat.id, good.get_url())
    else:
        order_dao.add_to_cart(call.from_user.id, callback[0])
        bot.send_message(chat_id=call.message.chat.id, text='Товар добавлен в корзину!')


bot.polling(none_stop=True)
