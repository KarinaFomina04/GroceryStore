import telebot
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["TG_TOKEN"])


@bot.message_handler(content_types=['text'])
def welcome(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
