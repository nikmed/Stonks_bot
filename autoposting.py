import telebot 
import dbworker
from datetime import time, datetime
import requests
import json

TOKEN = '1389715736:AAE5tnOA2sSLz16QgACPmJ4xH3-8aXwGghI'
db = dbworker.DBWorker()


#Emoji codes
STONKS = b'\xF0\x9F\x93\x88'
MONEY = b'\xF0\x9F\x92\xB8'


def request(symbol):
	url = "https://stockexchangeapi.p.rapidapi.com/price/{sym}".format(sym = symbol)
	headers = {
    	'x-rapidapi-host': "stockexchangeapi.p.rapidapi.com",
    	'x-rapidapi-key': "0f0c2f6bf5msh5c1fd736fa37043p1bd0f4jsn0a126ab7fb44"
    	}
	response = requests.request("GET", url, headers=headers)
	print(response.text)
	try:
		result = json.loads(response.text)
		return result
	except:
		return 'Error'


def time_sort(s): 
	t = datetime.now().timetuple()
	time_minutes = t.tm_hour * 60 + t.tm_min
	times = s[1].split(',')
	t1 = int(times[0].split(':')[0]) * 60 + int(times[0].split(':')[1])
	delta1 = (t1 - time_minutes)
	if len(times) > 1:
		t2 = int(times[1].split(':')[0]) * 60 + int(times[1].split(':')[1])
		delta2 = t2 - time_minutes
		if delta1 > 0 and delta2 > 0:
			return delta1 if delta2 == None or delta2 > delta1 and delta1 > 0 else delta2
		else:
			return 1440	
	return delta1 if delta1 > 0 else 1440


def format_message(user_id):
	message = ''
	for i in db.all_company(user_id):
		print(i)
		try:
			req = request(i)
			message += STONKS.decode('utf-8') + req['symbolName'] + " " + MONEY.decode('utf-8') + req['price'] + '\n'
		except Exception as e:
			print(e)
	return message


if __name__ == "__main__":
	bot = telebot.TeleBot(TOKEN)
	dates = sorted(db.all_data(), key = lambda x: time_sort(x))
	time_all = datetime.now().timetuple()
	t = time_all.tm_hour * 60 + time_all.tm_min
	if len(dates[0][1].split(',')) > 1:
		tm1 , tm2 = dates[0][1].split(',')
		t1 = int(tm1.split(':')[0]) * 60 + int(tm1.split(':')[1])
		t2 = int(tm2.split(':')[0]) * 60 + int(tm2.split(':')[1])
	else:
		tm1 = dates[0][1]
		t1 = int(tm1.split(':')[0]) * 60 + int(tm1.split(':')[1])
		t2 = 1440
	if abs(t - int(t1)) < 10 or abs(t - int(t2)) < 10:
		bot.send_message(dates[0][0], format_message(dates[0][0]))