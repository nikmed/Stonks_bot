import telebot
import requests
import json
import dbworker
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from multiprocessing import Process
from time import sleep

bot = telebot.TeleBot('1389715736:AAE5tnOA2sSLz16QgACPmJ4xH3-8aXwGghI')
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


@bot.message_handler(content_types=['text'])
def send_text(message):
	print(message.text)
	global user_id
	user_id = message.chat.id
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
	print(message.text)
	global user_id
	db.insert_string(user_id, call.data)


@bot.message_handler(commands=['delete'])
def delete_company(message):
	print(message.text)




def send_schedule_message():
	bot.send_message(285555077,'Sosi')
	time.sleep(60)

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
	

"""scheduler = Process(target = send_schedule_message, args = ())
scheduler.start()"""
while True:
	try:
		bot.polling()
	except Exception as e:
		print(e)
		time.sleep(60)