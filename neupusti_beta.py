#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from time import sleep
import datetime


import pygsheets
from pytz import timezone
import telebot
import constants
from neupusti_db import SQLight


# Open spreadsheet and then workseet


db = SQLight(constants.db_name)
categories_ru=["1. Образование и Наука"+u"\U0001F393","2. Карьера и Трудоустройство"+u"\U0001F4BC","3. Исскуство и Творчество"+u"\U0001F3A8","4. Предпринимательство и Инновации"+u"\U0001F4B8","5. Подписаться на все"+u"\U0001F47B"]
markup_get_create_query=telebot.types.ReplyKeyboardMarkup(True,False)
markup_get_create_query.row(u"\U0001F4CB"+" Мои подписки")
markup_get_create_query.row(u"\U0001F6E0"+" Создать новый запрос ")
markup_category = telebot.types.ReplyKeyboardMarkup(True,False)
for row in categories_ru:
	markup_category.row(row)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(constants.token)

class Post:
    def __init__(self, category):
        self.category = category
        
post_dict = {}


@bot.message_handler(commands=['start'])
def starting(message):
	global markup_get_create_query
	last_posts = telebot.types.InlineKeyboardMarkup()
	row=[telebot.types.InlineKeyboardButton(u"\U0001F4E3"+" Получить последние посты",callback_data="/posts")]	
	last_posts.row(*row)
	db = SQLight(constants.db_name)
	if db.check_user_info(message.from_user.id) or db.check_new_user_info(message.from_user.id):
		bot.send_message(message.from_user.id,'Приветствую ' + (message.from_user.first_name)+"!")
		bot.send_message(message.from_user.id,'<b>[ '+u"\U0001F4CB"+' Мои подписки ]</b> - отоброжает список категории вашей подписки, также можно редактировать\n<b>[ '+u"\U0001F6E0"+' Создать новый запрос ]</b> - создаете новый список для подписки',reply_markup=markup_get_create_query,parse_mode='HTML')
		return
	bot.send_message(message.from_user.id,'Добро пожаловать, ' + message.from_user.first_name + "!",reply_markup=markup_get_create_query)
	bot.send_message(message.from_user.id,'<b>[ '+u"\U0001F4CB"+' Мои подписки ]</b> - отоброжает список категории вашей подписки, также можно редактировать\n<b>[ '+u"\U0001F6E0"+' Создать новый запрос ]</b> - создаете новый список для подписки',parse_mode='HTML',reply_markup = last_posts)		
	time_zone = 'Asia/Almaty'
	current = "%Y-%m-%d %H:%M"
	now_time = datetime.datetime.now(timezone(time_zone)).strftime(current)
	db.add_new_user_info(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username,now_time)
	db.import_user(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username,now_time)
	db.close()




def admin_buttons():
	admin_inline = telebot.types.InlineKeyboardMarkup()
	row_1 = [telebot.types.InlineKeyboardButton("Добавить нового админа",callback_data="/add_admin")]
	row_2 = [telebot.types.InlineKeyboardButton("Редактировать список админов",callback_data="/edit_admin")]
	row_3 = [telebot.types.InlineKeyboardButton("Обновить пост по категории",callback_data="/edit_post")]
	row_4 = [telebot.types.InlineKeyboardButton("Последние 4 поста",callback_data="/posts")]
	
	admin_inline.row(*row_1)
	admin_inline.row(*row_2)
	admin_inline.row(*row_3)
	admin_inline.row(*row_4)
	return admin_inline



@bot.message_handler(content_types=['text'])
def categorizing(message):
	global markup_get_create_query
	global markup_category
	db = SQLight(constants.db_name)
	if message.text == 'admin':
		admins = db.get_admin_list()
		if message.from_user.username in admins or message.from_user.id==295091909:
			print("IS ADMIN")
			bot.send_message(message.from_user.id,"Здарвствуйте, Админ!",reply_markup = admin_buttons())

	if message.text=='del':
		print("DELETED Kairat")
		db.delete_user_all(295091909)
		db.delete_user_info_all(295091909)
		db.delete_new_user_info_all(295091909)
	if "Мои подписки" in message.text:	
		temp=db.get_category(message.from_user.id)
		following=''
		for i in temp:
			following+='[ '+categories_ru[i[0]-1][3:]+']\n'
		bot.send_message(message.from_user.id,'Вы подписаны: \n'+following,reply_markup=markup_get_create_query)
	elif "Создать новый запрос" in message.text:
		bot.send_message(message.from_user.id,'Выберите категории, на которые вы бы хотели подписаться.\nЧтобы подписаться на несколько категории, отправьте номера категории с запятыми.\nНапример:1,3,4',reply_markup=markup_category)
	else:
		if message.text in categories_ru:
			print (message.text[0])
			db.delete_user_all(message.from_user.id)						
			if message.text[0]=='5':
				for i in range(1,5):
					db.add_new_user(i,message.from_user.id)					
				bot.send_message(message.from_user.id,'Вы успешно подписаны на все категории!',reply_markup=markup_get_create_query)
			else:
				db.add_new_user(int(message.text[0]),message.from_user.id)
				bot.send_message(message.from_user.id,'Вы успешно подписаны на категорию \n[ '+message.text[3:]+']',reply_markup=markup_get_create_query)
		elif message.text[0]=='5' and len(message.text)==1:
			db.delete_user_all(message.from_user.id)
			for i in range(1,5):
				db.add_new_user(i,message.from_user.id)					
			bot.send_message(message.from_user.id,'Вы успешно подписаны на все категории!',reply_markup=markup_get_create_query)

		elif len(message.text)>1 and len(message.text)<8 and ',' in message.text and message.text[0] in '1234' and message.text[len(message.text)-1] in '1234':
			db.delete_user_all(message.from_user.id)
			temp=(message.text).split(',')
			followed=''
			if db.check_user(message.from_user.id):
				db.delete_user_all(message.from_user.id)
			for i in temp:
				db.add_new_user(int(i),message.from_user.id)
				followed+='['+(categories_ru[int(i)-1])[3:]+' ]\n'
			bot.send_message(message.from_user.id,'Вы успешно подписаны на категории:\n'+followed[:-1],reply_markup=markup_get_create_query)
	db.close()

@bot.callback_query_handler(func=lambda call: call.data=='/posts')
def posts(call):
	try:
		global markup_get_create_query
		db = SQLight(constants.db_name)
		links = db.get_last_links() 
		for link in links[:-1]:
			bot.send_message(call.from_user.id,link[0])
			sleep(0.1)
		bot.send_message(call.from_user.id,links[-1][0],reply_markup=markup_get_create_query)
	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call: call.data=='/add_admin')
def add_admin(call):
	try:
		msg = bot.send_message(call.from_user.id,"Напишите username админа \nДля отменты нажмите на /back")
		bot.register_next_step_handler(msg, process_username)
	except Exception as e:
		print(e)
def process_username(message):
	username = message.text
	db = SQLight(constants.db_name)
	try:
		if username == '/back':
			bot.send_message(message.from_user.id,"Вы в меню админа!", reply_markup=admin_buttons())	
			return
		db.add_admin(username)
		bot.send_message(message.from_user.id,"Admin под ником "+username+" добавлен!", reply_markup=admin_buttons())			
	except Exception as identifier:
		bot.send_message(message.from_user.id,str(identifier))

@bot.callback_query_handler(func=lambda call: call.data=='/edit_admin')
def edit_admin(call):
	try:
		db = SQLight(constants.db_name)
		_admins = telebot.types.InlineKeyboardMarkup()
		for admin in db.get_admin_list():
			row = [telebot.types.InlineKeyboardButton(admin + " " + u"\u2715",callback_data="del"+admin)]
			_admins.row(*row)
		row = [telebot.types.InlineKeyboardButton("Назад в меню",callback_data="/admin_menu")]
		_admins.row(*row)
		bot.send_message(call.from_user.id,"Выберите админа, которого хотите удалить!",reply_markup = _admins)
	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call: call.data[:3]=='del')
def del_admin(call):
	try:
		db = SQLight(constants.db_name)
		_admins = telebot.types.InlineKeyboardMarkup()
		admin = call.data[3:]
		db.delete_admin(admin)
		bot.answer_callback_query(call.id, text="<"+admin+"> Успешно удален!")
		
		for admin in db.get_admin_list():
			row = [telebot.types.InlineKeyboardButton(admin + " " + u"\u2715",callback_data="del"+admin)]
			_admins.row(*row)
		row = [telebot.types.InlineKeyboardButton("Назад в меню",callback_data="/admin_menu")]
		_admins.row(*row)
		bot.edit_message_text("Выберите админа, которого хотите удалить!",call.from_user.id,call.message.message_id,reply_markup = _admins)
	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call: call.data=='/edit_post')
def edit_post(call):
	try:
		global categories_ru
		categories = telebot.types.InlineKeyboardMarkup()
		for i in range(len(categories_ru)-1):
			row = [telebot.types.InlineKeyboardButton(categories_ru[i],callback_data="category"+str(i+1))]
			categories.row(*row)
		row = [telebot.types.InlineKeyboardButton("Назад в меню",callback_data="/admin_menu")]
		categories.row(*row)
		bot.edit_message_text("Выберите категорию, которую хотите изменить!",call.from_user.id,call.message.message_id,reply_markup = categories)

	except Exception as e:
		print(e)

@bot.callback_query_handler(func=lambda call: call.data[:8]=='category')
def edit_category(call):
	try:
		cat = call.data[8:]
		category = Post(cat)
		chat_id=call.from_user.id
		post_dict[chat_id] = category
		print(cat)
		msg = bot.edit_message_text("Отправьте ссылку поста...\n/otmena - для отмены действия ",call.from_user.id,call.message.message_id)
		bot.register_next_step_handler(msg, update_post)

	except Exception as e:
		print(e)
def update_post(message):
	#try:
	post = message.text
	if post=='/otmena':
		bot.send_message(message.from_user.id,"Вы в главном меню...",reply_markup=admin_buttons())
		return
	db = SQLight(constants.db_name)
	category = post_dict[message.from_user.id]
	print(post, category.category)
	db.update_post(category.category,post)
	bot.send_message(message.from_user.id,"Ссылка категории [ '{0}' ]\n Успешно обновлен на пост [ '{1}' ]".format(categories_ru[int(category.category)-1],post))
	sleep(1)
	bot.send_message(message.from_user.id,"Вы в главном меню...",reply_markup=admin_buttons())
			
	#except Exception as e:
	#	print(e)	
@bot.callback_query_handler(func=lambda call: call.data=='/admin_menu')
def menu_admin(call):
	try:
		bot.edit_message_text('Вы в главном меню', call.from_user.id, call.message.message_id, reply_markup = admin_buttons())					
	except Exception as e:
		print(e)

# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
bot.polling(True)

