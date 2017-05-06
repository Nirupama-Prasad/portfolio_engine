from yahoo_finance import Share 
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def draw_stock(stock):
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

	x = [datetime.strptime(d,'%Y-%m-%d').date() for d in list_dates]
	y = list_prices
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.plot(x,y, label=stock.get_name())
	plt.gcf().autofmt_xdate()

	plt.savefig('static/stocks.png')
	#plt.clf() 

