import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from datetime import datetime


TOKEN = "5092926905:AAHxp3Pas4cgxmiBCTy_I1eWTiQf6N2h07Y"
bot = telebot.TeleBot(TOKEN)


class Bot():
    pass


@bot.message_handler(content_types=['text', 'photo', 'video'])
def get_text_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Йо!")

bot.polling(none_stop=True, interval=0)
