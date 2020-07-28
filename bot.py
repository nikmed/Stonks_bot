import telebot
import requests
import json
import dbworker
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from multiprocessing import Process
from time import sleep


TOKEN = '1389715736:AAE5tnOA2sSLz16QgACPmJ4xH3-8aXwGghI'

bot = telebot.TeleBot(TOKEN)
db = dbworker.DBWorker()
db.create_table()
user_id = ""



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я умею выводить котировки выбранных компаний.')
    print(message.chat.id)

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, 'Так просто меня не выключить.')
    print(message.text)

@bot.message_handler(commands=['settings'])
def settings(message):
	pass

@bot.message_handler(commands=['delete'])
def delete_company(message):
	if (len(message.text.split()) <= 1):
		bot.send_message(message.chat.id, 'Чтобы удалить компанию из рассылки необходимо написать /delete "абривеатура компании"')
	else:
		print(message.text.split()[1])
		print(db.delete_company(message.chat.id, message.text.split()[1]))

@bot.message_handler(commands=['schedule'])
def start_message(message):
	markup = ReplyKeyboardMarkup()
	itembtn1 = KeyboardButton('Никогда')
	itembtn2 = KeyboardButton('1 раз в день')
	itembtn3 = KeyboardButton('2 раза в день')
	markup.add(itembtn1, itembtn2, itembtn3)
	msg = bot.send_message(message.chat.id, 'Ты зашел в настройки расписания. Начнем с простого, как часто ты хочешь получать рассылки?', reply_markup = markup)
	bot.register_next_step_handler(msg, schedule_tune)

def schedule_tune(message):
	markup = ReplyKeyboardRemove(True)
	if message.text == 'Никогда':
		bot.send_message(message.chat.id, '', reply_markup = markup)
	elif message.text == '1 раз в день':
		msg = bot.send_message(message.chat.id, 'В какое время ты хочешь получать уведомления. Пиши в формате HH:MM', reply_markup = markup)
		bot.register_next_step_handler(msg, date_tune)
	elif message.text == '2 раза в день':
		msg = bot.send_message(message.chat.id, 'В какое время ты хочешь получать уведомления. Пиши в формате HH:MM HH:MM', reply_markup = markup)
		bot.register_next_step_handler(msg, date_tune)
	else:
		msg = bot.send_message(message.chat.id, 'Прости я тебя не понимаю. Попробуй еще раз.', reply_markup = markup)
		bot.register_next_step_handler(msg, schedule_tune)
	

def date_tune(message):
	res = re.findall('\d{2}:\d{2}',message.text)
	if len(res) > 0:
		if len(res) == 1:
			db.insert_date(message.chat.id, res[0])
			bot.send_message(message.chat.id, 'Время добавлено')
		else:
			db.insert_date(message.chat.id, str(res[0]) + ' ' + str(res[1]))
			bot.send_message(message.chat.id, 'Время добавлено')
	else:
		msg = bot.send_message(message.chat.id, 'Я тебя не понял. Попробуй еще раз. Пиши в формате HH:MM')
		bot.register_next_step_handler(msg, date_tune)


@bot.message_handler(regexp = "\/\w+")
def func_handler(message):
	print(message.text)


@bot.message_handler(content_types=['text'])
def send_text(message):
	print(message.text)
	global user_id
	user_id = message.from_user.id
	if len(message.text.split()) == 1:
		j = request(message.text)
		print(j)
		if j == 'Error':
			bot.send_message(message.chat.id, 'Такой компании не найдено')
		else:
			markup = InlineKeyboardMarkup()
			add_to_list = InlineKeyboardButton('Подписаться', callback_data = message.text)
			markup.add(add_to_list)
			bot.send_message(message.chat.id, j['symbolName'] + '\n' + j['symbol'] + ' : ' + j['price'], reply_markup = markup)
	

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global user_id
	db.insert_company(user_id, call.data)


def request(symbol):
	url = "https://stockexchangeapi.p.rapidapi.com/price/{sym}".format(sym = symbol)
	headers = {
    	'x-rapidapi-host': "stockexchangeapi.p.rapidapi.com",
    	'x-rapidapi-key': "0f0c2f6bf5msh5c1fd736fa37043p1bd0f4jsn0a126ab7fb44"
    	}
	response = requests.request("GET", url, headers=headers)
	try:
		result = json.loads(response.text)
		return result
	except:
		return 'Error'
	

try:
	bot.polling()
except Exception as e:
	print(e)