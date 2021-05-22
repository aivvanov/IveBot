import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('stickerpack/welcomepic.png', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот созданный для общения:)".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == "private":
        if message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Отлично", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень:(", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично. Как твои?:)', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Не знаю, что и ответить:(')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отлично:)')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает:(')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=':) Как дела?', reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Это тестовое уведомление!')


    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
