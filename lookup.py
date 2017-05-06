from yahoo_finance import Share 
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dict_stock_to_five_day_prices = {}
portfolio_history_list = []
portfolio_dates = []

def draw_stock(stock):
	global dict_stock_to_five_day_prices, portfolio_dates
	stock_dictionary = {}
	#Plot five day data
	date_now = datetime.now().date()
	date_five_before = (datetime.now() - timedelta(days=5)).date()
	
	five_day_data = stock.get_historical(str(date_five_before), str(date_now))

	list_dates = []
	list_prices = []

	for each in five_day_data:
		list_dates.append(each['Date'])
		list_prices.append(each['Close'])

	dict_stock_to_five_day_prices[each['Symbol']] = list_prices[:]
	portfolio_dates = list_dates


	x = [datetime.strptime(d,'%Y-%m-%d').date() for d in list_dates]
	y = list_prices
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.plot(x,y, label=stock.get_name())
	plt.gcf().autofmt_xdate()

	plt.savefig('static/stocks.png')
	#plt.clf() 

def draw_portfolio(portfolio):
	global portfolio_history_list, dict_stock_to_five_day_prices, portfolio_dates

	print dict_stock_to_five_day_prices
	print "*" * 80

	for each_stock, five_day_prices in dict_stock_to_five_day_prices.items():
		count = portfolio[each_stock]['count']
		count_five_day_prices = [count * float(x) for x in five_day_prices] 
		dict_stock_to_five_day_prices[each_stock] = count_five_day_prices

	print dict_stock_to_five_day_prices

	list_prices = []


	x = [datetime.strptime(d,'%Y-%m-%d').date() for d in portfolio_dates]
	y = list_prices
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.plot(x,y, label=stock.get_name())
	plt.gcf().autofmt_xdate()

	plt.savefig('static/stocks.png')





