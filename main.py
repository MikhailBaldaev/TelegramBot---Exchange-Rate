import telebot

from parsing import find_rate, create_graph, find_other_rate
from config import *


token = token

bot = telebot.TeleBot(token)

instructions = 'Используй команду /rate для получения информации о курсе доллара на заданную дату\n\nКоманду ' \
               '/graph для получения информации о курсе доллара за период\n\nИли команду /currency для получения ' \
               'информации о курсе другой иностранной валюты к рублю на заданную дату'


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


@bot.message_handler(commands=['currency'])
def rate_currency(message):
    cid = message.chat.id
    sent = bot.send_message(cid, 'Напиши буквенный индекс интересующей тебя валюты (например, TRY, KZT) и дату '
                                 'в формате CURRENCY-DD.MM.YYYY')
    bot.register_next_step_handler(sent, call3)


def call(message):
    text = message.text
    cid = message.chat.id

    if len(text) == 10 and text.split('.')[0].isnumeric() and text.split('.')[1].isnumeric() and \
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

    if len(text[0]) == 10 and len(text[1]) == 10 and text[0].split('.')[0].isnumeric() and text[0].split('.')[1].isnumeric() and \
            text[0].split('.')[2].isnumeric() and len(text[1].split('.')) == 3 and text[1].split('.')[0].isnumeric() \
            and text[1].split('.')[1].isnumeric() and text[1].split('.')[2].isnumeric():

        result = create_graph(text[0], text[1])

        if result != 'graph.png':
            sent = bot.send_message(cid, result)
            bot.register_next_step_handler(sent, call2)
        else:
            f = open(f'C:\\Users\\emper\\PycharmProjects\\CBR RUB-USD\\{result}', 'rb')
            bot.send_document(cid, f)
            bot.send_message(cid, instructions)
    else:
        sent = bot.send_message(cid, 'Начальная дата и конечная дата должны быть строго в формате DD.MM.YYYY-DD.MM.YYYY')
        bot.register_next_step_handler(sent, call2)


def call3(message):
    text = message.text.split('-')
    cid = message.chat.id

    if len(text[0]) == 3 and text[0].isalpha():
        result = find_other_rate(text[0].upper(), text[1])
        bot.send_message(cid, result)
        bot.send_message(cid, instructions)
    else:
        sent = bot.send_message(cid, 'Запрос должен быть в формате CURRENCY-DD.MM.YYYY (например, TRY-01.01.2022)')
        bot.register_next_step_handler(sent, call3)


bot.polling(none_stop=True)
