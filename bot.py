import telebot
import configparser

from telebot import types

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])

# def toString(collection):
#     output = ''
#
#     for i in range(len(collection)):
#         output = output + str(i+1) + '. ' + collection[i] + '\n'
#
#     return output


categories = ['Бакалея', 'Десерты', 'Напитки', 'Чай']


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в {0.first_name}!\n Введите /category для вывода категорий "
                                      "товаров.".format(bot.get_me()))


@bot.message_handler(commands=['category'])
def getCategory(message):
    markup = types.InlineKeyboardMarkup()

    for i in categories:
        markup.add(types.InlineKeyboardButton(text=i, callback_data=i))

    bot.send_message(chat_id=message.chat.id, text="Категории товаров:", reply_markup=markup)


bot.polling(none_stop=True)
