import telebot
import config
import random
import requests
import os

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
RESUME = open('static/resume.pdf','rb')
MAIL = 'maximy.pro@gmail.com'
TELEGRAM_CONTACT = '@maximy221'
TO_CHAT_ID = '545804412'

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp','rb')
    bot.send_sticker(message.chat.id,sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Как дела?")
    item3 = types.KeyboardButton("Резюме")

    markup.add(item1,item2,item3)

    bot.send_message(message.chat.id,"Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me())
                     ,parse_mode='html',reply_markup=markup)


@bot.message_handler(commands=['resume'])
def get_resume(message):
    bot.send_message(message.chat.id,'Вот мое резюме:)')
    bot.send_document(message.chat.id,RESUME
                     ,parse_mode='html')

@bot.message_handler(content_types=['text'])
def lala(message):
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    if message.chat.type == 'private':
        if message.text == 'Резюме':
            bot.send_message(message.chat.id, 'Вот мое резюме:)')
            bot.send_document(message.chat.id, RESUME
                              , parse_mode='html')
        elif message.text == 'Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо",callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1,item2)

            bot.send_message(message.chat.id,'Отлично,сам как?',reply_markup=markup)
        else:
            bot.send_message(message.chat.id,'Я не знаю что ответить(')




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)