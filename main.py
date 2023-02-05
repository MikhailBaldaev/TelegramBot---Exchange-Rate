import telebot

from parsing import find_rate, create_graph
from config import *


token = token

bot = telebot.TeleBot(token)

instructions = 'Используй команду /rate для получения информации о курсе доллара на заданную дату\n\nили команду ' \
               '/graph для получения информации о курсе доллара за период'


@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    bot.send_message(cid, instructions)


@bot.message_handler(commands=['rate'])
def rate(message):
    cid = message.chat.id
    sent = bot.send_message(cid, 'Напиши дату в формате DD.MM.YYYY')
    bot.register_next_step_handler(sent, call)


@bot.message_handler(commands=['graph'])
def graph(message):
    cid = message.chat.id
    sent = bot.send_message(cid, 'Напиши начальную дату и конечную дату периода в формате DD.MM.YYYY-DD.MM.YYYY')
    bot.register_next_step_handler(sent, call2)


def call(message):
    text = message.text
    cid = message.chat.id

    if len(text.split('.')) == 3 and text.split('.')[0].isnumeric() and text.split('.')[1].isnumeric() and \
            text.split('.')[2].isnumeric():
        result = find_rate(text)
        bot.send_message(cid, result)
        bot.send_message(cid, instructions)
    else:
        sent = bot.send_message(cid, 'Дата должна быть строго в формате DD.MM.YYYY')
        bot.register_next_step_handler(sent, call)


def call2(message):
    text = message.text.split('-')
    cid = message.chat.id

    if len(text[0].split('.')) == 3 and text[0].split('.')[0].isnumeric() and text[0].split('.')[1].isnumeric() and \
            text[0].split('.')[2].isnumeric() and len(text[1].split('.')) == 3 and text[1].split('.')[0].isnumeric() \
            and text[1].split('.')[1].isnumeric() and text[1].split('.')[2].isnumeric() :
        result = create_graph(text[0], text[1])
        f = open(f'C:\\Users\\emper\\PycharmProjects\\CBR RUB-USD\\{result}', 'rb')
        bot.send_document(cid, f)
        bot.send_message(cid, instructions)
    else:
        sent = bot.send_message(cid, 'Начальная дата и конечная дата должны быть строго в формате DD.MM.YYYY-DD.MM.YYYY')
        bot.register_next_step_handler(sent, call2)


bot.polling(none_stop=True)
