#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from time import sleep
import constants
from neupusti_db import SQLight
import telebot
import sys
db = SQLight(constants.db_name)
bot = telebot.TeleBot(constants.token)
links=[]
deadlines=[]
tmp=[]
pages=1
main_url="http://neupusti.net/category/"
categories=["obrazovanie-nauka","karera-trudoustroistvo","iskustvo-tvorchestvo","predprinimatelstvo-innovacii"]

def get_data(url,num):
	soup=BeautifulSoup((requests.get(url)).content,"html.parser")
	g_data = soup.find_all("div",{"class" : "td-block-span6"})
	global links
	global deadlines
	global tmp
	deadlines=[]
	links=[]
	for item in g_data:
		try:
			deadline=item.contents[1].find_all("span",{"class":"deadline"})[0].text
			link=item.contents[1].find_all("a")[0].get("href")
			print(link)
		except:
			pass
		try:
			deadlines.append(deadline)
		except:
			pass
		try:
			links.append(link)
		except:
			pass
	temp_last_title=db.get_last_link(num)
	if db.check_last_link(num):
		print("ITS IN LAST LINK")
		current_index=links.index(temp_last_title)
		if temp_last_title in links:
			if links.index(temp_last_title)==0:
				print ("NOTHING NEW IN category",num)
				pass
			else:
				print ("GOT NEW INFORMATION for category",categories[num-1])
				user_db=db.get_user_by_category(num)
				for i in range(current_index):
					for user in user_db:
						sleep(0.5)
						print ("SENDING TO USER [",user[0],']')
						try:
							if links[i] in tmp:
								pass
							else:
								if deadline[i]!='Просрочен':
									#bot.send_message(user[0],links[i]+'\n'+deadlines[i])
									bot.send_message(295091909,links[i])
									#print("HELLo")
						except:
							print (user[0],"Blocked DELETING HIM FROM DB")
							db.unfollow(user[0])
							db.delete_user_all(user[0])
					tmp.append(links[i])
					print (tmp)
					print("Done sending users from category",num)
				print("UPDATE to new last_link")
				db.update_last_link(num,links[0])
		else:
			print("UPDATE db")
			db.update_last_link(num,links[0])
	
	else:
		print("NEW DATABASE FOR TITLE")
		db.add_last_link(num,links[0])
for i in range(len(categories)):
	url=main_url+categories[i]
	get_data(url,i+1)
	############################################################################################################
	#tmp.append(links[0])																					   #
	############################################################################################################
db.close()