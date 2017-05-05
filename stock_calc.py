
from yahoo_finance import Share as sh
import operator


growth_stocks = ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']

dictionary_strategies = {
	'growth' : growth_stocks
	}


def get_portfolio(amount, stock_type):
	stock_dictionary = {}
	sum_peg = 0
	total_balance = 0

	for each_stock in stock_type:
		internal_dictionary = {}
		stock = sh(each_stock)
		internal_dictionary['price'] = stock.get_price()
		internal_dictionary['peg'] = stock.get_price_earnings_growth_ratio()
		
		#calculate sum here for later on
		sum_peg += float(internal_dictionary['peg'])

		stock_dictionary[each_stock] = internal_dictionary

	#balance = 0
	for each_stock in stock_dictionary.keys():
		each_stock_price = float(stock_dictionary[each_stock]['price'])
		each_stock_peg = stock_dictionary[each_stock]['peg']
		each_stock_ratio = float(each_stock_peg)/sum_peg	
		each_stock_amount = float(amount * each_stock_ratio)
		
		each_stock_count = int(each_stock_amount/each_stock_price)
		total_balance += each_stock_amount % each_stock_price

		stock_dictionary[each_stock]['ratio'] = each_stock_ratio
		stock_dictionary[each_stock]['amount'] = each_stock_amount
		stock_dictionary[each_stock]['count'] = each_stock_count

	for key, value in stock_dictionary.items():
		print key, value

	print "balance is: ", total_balance

	return stock_dictionary


def test_command_line():
	balance = 0
	get_portfolio(5000, dictionary_strategies['growth'])
	get_portfolio(balance, dictionary_strategies['growth'])


test_command_line()