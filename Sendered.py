from urllib3 import Retry

import base
import telebot
from telebot import types
import datetime
import time




db = base.Base("localhost")
bot = telebot.TeleBot('5194270771:AAF2zvg8MEBgCjOusmaIyX6u4yF7X_CtmCw')
#bot = telebot.TeleBot('5188999206:AAFDzoHQCE6_YTsAxTA8hlhJD4M2tPXyVh4')#dev
retry = Retry(connect=3, backoff_factor=0.5)


def sender():
    # try:
    for l in db.FindNoPost():
        print("l")
        if l["tweet"] != 0:
            tweet = l["tweet"]
        else:
            tweet = " "

        txt = f"{l['title']} \n {l['coinName']['full']} \nExchenge: {l['exchenge']} \n {tweet} \nNeural network evaluation: {l['balls']} of 5\nThe news was published: {l['addNewsDate'][1]} \nListing date: {l['date']}"

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Link to event", url=l['source'])
        markup.add(button1)

        if l["img"] != 0:
            if l["type"] <= 2:
                print("type 2")
                for a in db.getAdmin():
                    bot.send_photo(a["usrId"], photo=l["img"],caption=txt,reply_markup=markup)
                for u in db.getAllPaymentUsr():
                    bot.send_photo(u["usrId"], photo=l["img"], caption=txt,reply_markup=markup)
            else:
                print("type 3")
                bot.send_photo(-1001755014693, photo=l["img"],caption=txt,reply_markup=markup)
                #bot.send_photo(-1001504500389, photo=l["img"],caption=txt,reply_markup=markup)
    # except:



while True:
    sender()
    time.sleep(1)
