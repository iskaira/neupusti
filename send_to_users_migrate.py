import telebot
import constants
bot = telebot.TeleBot(constants.token)
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton("Neupusti Bot", url="t.me/Neupusti_Bot"))

bot.send_message(295091909,"Уважаемый подписчик, связи с миграцией сервера мы перезапустили наш телеграм бот. Просим вас переподписаться на наш новый телеграм бот @Neupusti_Bot",reply_markup=markup)