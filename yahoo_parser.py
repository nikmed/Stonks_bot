from bs4 import BeautifulSoup
import requests



def get_html(sym):
	page = requests.get('https://finance.yahoo.com/quote/{symbol}'.format(symbol = sym))
	soup = BeautifulSoup(page.text, 'html.parser')
	return soup

def get_price(sym):
	try:
		html = get_html(sym)
		name = html.find(id = 'Lead-3-QuoteHeader-Proxy').find(class_='Mt(15px)').find('h1').get_text()
		spans = html.find(id = 'Lead-3-QuoteHeader-Proxy').find(class_='D(ib) Mend(20px)').find_all('span')
		price = spans[0].get_text()
		delta = spans[1].get_text()
		return [name, price, delta]
	except Exception as e:
		print(e)
		return 'Error'




if __name__ == '__main__':
	sym = input()
	print(get_price(sym))


