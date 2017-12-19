import requests
import bs4


base_url = 'https://coinmarketcap.com/all/views/all/'
one_year_url = 'https://coinmarketcap.com/historical/20161204/'
old_currencies = {}
current_currencies = {}
snapshots = {}
old_value = 100.00


def get_previous_dates():
	url = 'https://coinmarketcap.com/historical/'
	res = requests.get(url)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	snapshot_number = 1
	for month in soup.findAll('div', attrs={'class':'col-sm-4 col-xs-6'}):
		for link in month.findAll('a'):
			snapshot_date = str(link['href']).split('/')[-2]
			new_link = 'https://coinmarketcap.com' + link['href']
			snapshots[snapshot_number] = [snapshot_date, new_link]
			snapshot_number += 1


def get_current_all():
	print('GETTING PRICE OF ALL CURRENT COINS...')
	res = requests.get(base_url)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	for tr in soup.find_all('tr')[1:]:
		currency_name = str(tr.find('a', attrs={'class': 'currency-name-container'}).text).lstrip().rstrip()
		# market_cap = str(tr.find('td', attrs={'class': 'no-wrap market-cap text-right'}).text).lstrip().rstrip()
		price = float(str(tr.find('a', attrs={'class': 'price'}).text).lstrip().rstrip().replace('$', '').replace(',', ''))
		# print(currency_name, price)
		current_currencies[currency_name] = price
	print('DONE.\n')


def get_old_tops(link, number_to_buy):
	date_box = link.split('/')[-2]
	print('GETTING TOP ' + str(number_to_buy) + ' FROM ' + str(date_box) + '...')
	res = requests.get(link)
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	print('SIMULATING BUYING $10.00 OF EACH COIN...')
	for tr in soup.find_all('tr')[1:(number_to_buy + 1)]:
		currency_name = str(tr.find('a', attrs={'class':'currency-name-container'}).text).lstrip().rstrip()
		market_cap =str(tr.find('td', attrs={'class':'no-wrap market-cap text-right'}).text).lstrip().rstrip()
		price = float(str(tr.find('a', attrs={'class': 'price'}).text).lstrip().rstrip().replace('$', '').replace(',', ''))
		coins_purchased = float('%.6f' % ((old_value / number_to_buy) / price))
		print('BOUGHT: ' + str(coins_purchased) + ' of ' + str(currency_name) + ' for $' + '%.2f' %(old_value/number_to_buy))
		old_currencies[currency_name] = coins_purchased
	print('DONE.\n')


def calculate_current_value():
	# old_value = 100.00
	current_value = 0.0
	for name, amount in old_currencies.items():
		try:
			new_value = float(amount * current_currencies.get(name))
			print(name + ' is now worth: $' + ('%.2f' % (new_value)))
			current_value += new_value
		except:
			print(name + ' NO LONGER EXISTS.')
	print('\nTOTAL NEW PORTFOLIO VALUE: $' + ('%.2f' % (current_value)))
	increase = (current_value - old_value)/old_value * 100
	print('THERE WAS A ' + ('%.2F' % (increase)) + '% INCREASE')


if __name__ == '__main__':
	get_previous_dates()
	old_value = float(input('ENTER DOLLAR AMOUNT TO INVEST: '))
	number_of_cryptos = int(input('ENTER HOW MANY COIN TYPES YOU WANT TO BUY: '))
	year_to_compare = input('WHAT YEAR WOULD YOU LIKE TO COMPARE TO: ')
	for key, value in snapshots.items():
		if str(value[0]).startswith(year_to_compare):
			print(str(key) + ': ' + str(value[0]))
	compare_date = int(input('SELECT DATE TO COMPARE: '))
	get_current_all()
	get_old_tops(snapshots.get(compare_date)[1], number_of_cryptos)
	calculate_current_value()
	quit_check = input('\nPRESS ENTER TO QUIT')
