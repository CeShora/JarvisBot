import os
import telebot
from dotenv import load_dotenv

import Responses as res

load_dotenv()
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = res.welcome
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = res.echo_all
    bot.reply_to(message, text)


if __name__ == "__main__":
    bot.polling()
