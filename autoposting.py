import telebot 
import dbworker
from datetime import time, datetime
import requests
import json
import yahoo_parser
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
TOKEN = '1389715736:AAE5tnOA2sSLz16QgACPmJ4xH3-8aXwGghI'
db = dbworker.DBWorker()


#Emoji codes
STONKS_UP = b'\xF0\x9F\x93\x88'
STONKS_DOWN = b'\xF0\x9F\x93\x89'
MONEY = b'\xF0\x9F\x92\xB8'





def time_sort(s): 
	t = datetime.now().timetuple()
	time_minutes = t.tm_hour * 60 + t.tm_min
	times = s[1].split(' ')
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
			r = yahoo_parser.get_price(i)
			if r != 'Error':
				if r[2][0] == '-':
					message += STONKS_DOWN.decode('utf-8') + r[0] + " " + '\n' + MONEY.decode('utf-8') + r[1] + ' ' + r[2] + '\n' + '\n' 
				else:
					message += STONKS_UP.decode('utf-8') + r[0] + " " + '\n' + MONEY.decode('utf-8') +  r[1] + ' ' + r[2] + '\n' + '\n'
		except Exception as e:
			print(e)
	return message

@sched.scheduled_job('interval', minutes=5)
def timed_job():
	bot = telebot.TeleBot(TOKEN)
	dates = sorted(db.all_data(), key = lambda x: time_sort(x))
	time_all = datetime.now().timetuple()
	t = time_all.tm_hour * 60 + time_all.tm_min
	i = 0
	while len(dates) > i and time_sort(dates[i]) <= 5:
		try:
			bot.send_message(dates[i][0], format_message(dates[i][0]))
		except Exception as e:
			print(e)
		i += 1



if __name__ == "__main__":
	sched.start()
