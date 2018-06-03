import telebot
import constants
import pygsheets
from pytz import timezone
from neupusti_db import SQLight
bot = telebot.TeleBot(constants.token)
db=SQLight(constants.db_name)
last_row = db.get_last_row_import()
try:
    if last_row:    
        gc = pygsheets.authorize(service_file=constants.client,no_cache=True)
        sht = gc.open("Neupusti Bot sheet")
        sheet = sht.worksheet('title','users')
        index = 1
        sheet.insert_rows(index,values=last_row)
        db.delete_data()
except Exception as e:
    bot.send_message(someID,"NOT OK: "+str(e))



