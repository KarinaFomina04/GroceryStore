import telebot
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])


def toString(collection):
    output = ''

    for i in range(len(collection)):
        output = output + str(i+1) + '. ' + collection[i] + '\n'

    return output


categories = ['бакалея', 'десерты', 'напитки', 'чай']


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в {0.first_name}!\n Введите /category для вывода категорий "
                                      "товаров.".format(bot.get_me()))


@bot.message_handler(commands=['category'])
def getCategory(message):
    bot.send_message(message.chat.id, "Категории товаров:\n{0}".format(toString(categories)))


bot.polling(none_stop=True)
