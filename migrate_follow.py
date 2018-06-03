#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from time import sleep
import telebot
class SQLight:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor() 
    def select_users(self):
        with self.connection:
            return self.cursor.execute('select message_id from user_info').fetchall()

import constants
db = SQLight(constants.db_name)
bot = telebot.TeleBot(constants.token)
users = (db.select_users())
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton("Neupusti Bot", url="t.me/NeupustiBot"))

for user in users:
    user = user[0]
    try:
        #bot.send_message(user,"Уважаемый подписчик, связи с миграцией сервера мы перезапустили наш телеграм бот. Просим вас переподписаться на наш новый телеграм бот @NeupustiBot",reply_markup=markup)
        print(user)
        sleep(0.2)
    except:
        print("CANt send to user")