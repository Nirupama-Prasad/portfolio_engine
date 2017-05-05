from yahoo_finance import Share 
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def pull_stock(symbol):
	stock = None

	try:
		stock = Share(symbol)
	except yahoo_finance.YQLQueryError:
		print "Service is down or unreachable. Exiting program"
		exit()
	except:
		print "General error using Yahoo Finance! Api. Exiting"
		exit()

	#check if the input is valid
	if stock.get_name() is None:
		print "Invalid stock symbol. Please enter a valid symbol"
		return None

	stock_dictionary = {}

	stock_dictionary["time"] = time.ctime() 
	print stock_dictionary["time"]

	stock_dictionary["name"] = stock.get_name() 
	print stock_dictionary["name"]

	price = stock.get_price()
	change = stock.get_change()
	percent_change = stock.get_percent_change()
	stock_dictionary["change"] = price + " " + change + " (" + percent_change +")"
	print stock_dictionary["change"]

	#Plot five day data
	date_now = datetime.now().date()
	date_five_before = (datetime.now() - timedelta(days=5)).date()
	
	five_day_data = stock.get_historical(str(date_five_before), str(date_now))
	print five_day_data

	list_dates = []
	list_prices = []

	for each in five_day_data:
		list_dates.append(each['Date'])
		list_prices.append(each['Close'])

	x = [datetime.strptime(d,'%Y-%m-%d').date() for d in list_dates]
	y = list_prices
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.plot(x,y, label=symbol)
	plt.gcf().autofmt_xdate()

	plt.savefig('static/stocks.png')
	plt.clf() 

	return stock_dictionary


def test_cmd_line():
	while (True ):
		try:
			symbol = raw_input("Please enter a symbol: ")
			data = pull_stock(symbol)
		except KeyboardInterrupt:
			print "\nGoodbye!"
			exit()


#test_cmd_line()
#test_matlab()