import telebot 
import dbworker
import time

TOKEN = '1389715736:AAE5tnOA2sSLz16QgACPmJ4xH3-8aXwGghI'
db = dbworker.DBWorker()

def time_sort():
	

if __name__ == "__main__":
	bot = telebot.TeleBot(TOKEN)
	dates = sorted(db.all_data(), key = lambda x: int(x[1].split(':')[0]) - time.localtime().tm_hour)
	print(dates)