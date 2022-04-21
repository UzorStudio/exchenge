import time

import telebot
from telebot import types

import base

bot = telebot.TeleBot('5194270771:AAF2zvg8MEBgCjOusmaIyX6u4yF7X_CtmCw')
bd = base.Base("localhost")


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    if bd.getuser(message.chat.id) is None:
        bd.regUser(message.chat.id)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="payment"))

    bot.send_message(message.chat.id, "Here you can receive a newsletter of important events for cryptocurrency",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "payment":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="I have a promo code"))
        keyboard.add(types.KeyboardButton(text="Pay for a subscription"))
        bot.send_message(message.chat.id, "Pay for a subscription",
                         reply_markup=keyboard)
    if message.text == "I have a promo code":
        bot.send_message(message.chat.id, "Enter a promo code")
        bot.register_next_step_handler(message,PayPromos)
    if message.text == "Pay for a subscription":
        bot.send_message(message.chat.id, "Enter a promo code")
        bot.register_next_step_handler(message,PayPromos)


def PayPromos(message):
    pr = bd.PayPromo(message.chat.id,message.text)
    print(pr)
    if pr == True:
        bot.send_message(message.chat.id, "The subscription is activated for 5 days for free!")
    elif pr == False:
        bot.send_message(message.chat.id, "Subscription not activated(")
    elif pr == "admin":
        bot.send_message(message.chat.id, "Режим бога богатства активирован!")

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            bot.polling(none_stop=True)

