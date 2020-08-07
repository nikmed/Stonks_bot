import telebot
import requests
import json
import dbworker
import yahoo_parser 
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from multiprocessing import Process
from time import sleep
import os
from flask import Flask, request

TOKEN = '1389715736:AAE5tnOA2sSLz16QgACPmJ4xH3-8aXwGghI'
server = Flask(__name__)


#Emoji codes
STONKS_UP = b'\xF0\x9F\x93\x88'
STONKS_DOWN = b'\xF0\x9F\x93\x89'
MONEY = b'\xF0\x9F\x92\xB8'

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
		msg = bot.send_message(message.chat.id, 'В какое время ты хочешь получать уведомления. Пиши в формате HH:MM. В 24-часовом формате.', reply_markup = markup)
		bot.register_next_step_handler(msg, date_tune)
	elif message.text == '2 раза в день':
		msg = bot.send_message(message.chat.id, 'В какое время ты хочешь получать уведомления. Пиши в формате HH:MM HH:MM. В 24-часовом формате.', reply_markup = markup)
		bot.register_next_step_handler(msg, date_tune)
	else:
		msg = bot.send_message(message.chat.id, 'Прости я тебя не понимаю. Попробуй еще раз.', reply_markup = markup)
		bot.register_next_step_handler(msg, schedule_tune)
	

def date_tune(message):
	res = re.findall('\d{2}:\d{2}',message.text)
	if len(res) > 0:
		s = res[0].split(':')
		hh, mm = int(s[0]), int(s[1]) 
		if len(res) == 1:
			if hh >= 0 and hh <= 24 and mm >= 0 and mm <= 60:
				db.insert_date(message.chat.id, res[0])
				bot.send_message(message.chat.id, 'Время добавлено')
			else:
				msg = bot.send_message(message.chat.id, 'Я тебя не понял. Попробуй еще раз. Пиши в формате HH:MM')
				bot.register_next_step_handler(msg, date_tune)
		else:
			s1 = res[1].split(':')
			hh1, mm1 = int(s1[0]), int(s1[1]) 
			if hh >= 0 and hh <= 24 and mm >= 0 and mm <= 60 and hh1 >= 0 and hh1 <= 24 and mm1 >= 0 and mm1 <= 60:
				db.insert_date(message.chat.id, str(res[0]) + ' ' + str(res[1]))
				bot.send_message(message.chat.id, 'Время добавлено')
			else:
				msg = bot.send_message(message.chat.id, 'Я тебя не понял. Попробуй еще раз. Пиши в формате HH:MM')
				bot.register_next_step_handler(msg, date_tune)
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
		j = yahoo_parser.get_price(message.text)
		print(j)
		if j == 'Error':
			bot.send_message(message.chat.id, 'Такой компании не найдено')
		else:
			markup = InlineKeyboardMarkup()
			add_to_list = InlineKeyboardButton('Подписаться', callback_data = message.text)
			markup.add(add_to_list)
			if j[2][0] == "-":
				bot.send_message(message.chat.id, STONKS_DOWN.decode('utf-8') + j[0] + '\n' + MONEY.decode('utf-8') +j[1] + ' ' + j[2], reply_markup = markup)
			else:
				bot.send_message(message.chat.id, STONKS_UP.decode('utf-8') + j[0] + '\n' + MONEY.decode('utf-8') +j[1] + ' ' + j[2], reply_markup = markup)

	

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	global user_id
	db.insert_company(user_id, call.data)
	


if __name__ == "__main__":
	server.debug = True
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
	try:
		bot.polling()
	except Exception as e:
		print(e)