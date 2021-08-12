import telebot
import configparser

from Enum.property_enum import ConfirmInputMode
from Dao.good_dao import GoodDAO
from Dao.category_dao import CategoryDAO
from Dao.order_dao import OrderDAO
from telebot import types

from Service.order_service import OrderService
from Utils.localization import Localization
from Dao.property_dao import PropertyDao
from Service.e_mail_service import EmailService

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])

category_dao = CategoryDAO()
good_dao = GoodDAO()
order_dao = OrderDAO()
property_dao = PropertyDao()
email_service = EmailService()
confirm_mode_enabled = False
property_dict = {}
order_service = OrderService()


@bot.message_handler(commands=['start'])
def start(message):
    Localization.init_locale(message.from_user.language_code)
    bot.send_message(message.chat.id, Localization.get_message('start_message').format(bot.get_me()))


@bot.message_handler(commands=['cart'])
def get_cart(message):
    Localization.init_locale(message.from_user.language_code)
    text_message = order_service.get_orders(message.from_user.id, False)
    bot.send_message(chat_id=message.chat.id, text=text_message, parse_mode='html')


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
    elif callback[1] == 'confirm':
        if callback[0] == 'yes':
            property_dao.add_properties(property_dict, call.from_user.id)
            #TODO e_mail_service.send_message
            email_service.send_gmail(property_dict, call.from_user.id)
            bot.send_message(chat_id=call.message.chat.id, text=Localization.get_message('order_in_confirm'))
        else:
            bot.send_message(chat_id=call.message.chat.id, text=Localization.get_message('repeat_confirm'))
        property_dict.clear()
        order_dao.clear_cart(call.from_user.id)
    else:
        order_dao.add_to_cart(call.from_user.id, callback[0])
        bot.send_message(chat_id=call.message.chat.id, text=Localization.get_message('order_added'))


@bot.message_handler(commands=['confirm'])
def confirm(message):
    Localization.init_locale(message.from_user.language_code)
    global confirm_mode_enabled
    confirm_mode_enabled = ConfirmInputMode.NAME
    bot.send_message(chat_id=message.chat.id, text=Localization.get_message('properties_confirm').
                     format(Localization.get_message('name')))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global confirm_mode_enabled
    global property_dict
    if confirm_mode_enabled == ConfirmInputMode.NAME:
        property_dict[ConfirmInputMode.NAME.value] = message.text
        bot.send_message(chat_id=message.chat.id, text=Localization.get_message('properties_confirm').
                         format(Localization.get_message('telephone')))
        confirm_mode_enabled = ConfirmInputMode.TELEPHONE_NUMBER
    elif confirm_mode_enabled == ConfirmInputMode.TELEPHONE_NUMBER:
        property_dict[ConfirmInputMode.TELEPHONE_NUMBER.value] = message.text
        bot.send_message(chat_id=message.chat.id, text=Localization.get_message('properties_confirm').
                         format(Localization.get_message('e_mail')))
        confirm_mode_enabled = ConfirmInputMode.E_MAIL
    elif confirm_mode_enabled == ConfirmInputMode.E_MAIL:
        property_dict[ConfirmInputMode.E_MAIL.value] = message.text
        bot.send_message(chat_id=message.chat.id, text=Localization.get_message('properties_confirm').
                         format(Localization.get_message('address')))
        confirm_mode_enabled = ConfirmInputMode.ADDRESS
    elif confirm_mode_enabled == ConfirmInputMode.ADDRESS:
        property_dict[ConfirmInputMode.ADDRESS.value] = message.text
        markup = types.InlineKeyboardMarkup()
        yes_button = types.InlineKeyboardButton(text=Localization.get_message('yes'), callback_data='yes confirm')
        no_button = types.InlineKeyboardButton(text=Localization.get_message('no'), callback_data='no confirm')
        markup = markup.add(yes_button, no_button)
        bot.send_message(chat_id=message.chat.id, text=Localization.get_message('order_data') + '\n\n{0}\n{1}\n{2}\n{3}'
                         .format(property_dict[ConfirmInputMode.NAME.value],
                                 property_dict[ConfirmInputMode.TELEPHONE_NUMBER.value],
                                 property_dict[ConfirmInputMode.E_MAIL.value],
                                 property_dict[ConfirmInputMode.ADDRESS.value]), reply_markup=markup)


bot.polling(none_stop=True)
