
from yahoo_finance import Share as sh
import operator

#Global
growth_stocks = ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
g_stock_dictionary = {}
dictionary_strategies = {
	'growth' : growth_stocks
	}



def get_portfolio(amount, stock_type):
	global g_stock_dictionary
	sum_peg = 0
	total_balance = 0
	stock_dictionary = {}

	for each_stock in stock_type:
		internal_dictionary = {}
		stock = sh(each_stock)
		price = float(stock.get_price())

		if(price > amount):
			continue

		internal_dictionary['price'] = float(price)
		internal_dictionary['peg'] = float(stock.get_price_earnings_growth_ratio())
		
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

		if bool(g_stock_dictionary) == True:
			g_stock_dictionary[each_stock]['count'] += each_stock_count
			g_stock_dictionary[each_stock]['amount'] += each_stock_amount
			print "updating stock: ", each_stock, "to", g_stock_dictionary[each_stock]['count'] 
			print "updating stock amount: ", each_stock, "to", g_stock_dictionary[each_stock]['amount'] 


	#if dictionary was empty
	if bool(g_stock_dictionary) == False:
		g_stock_dictionary = stock_dictionary.copy()

	return total_balance


def test_command_line():
	global g_stock_dictionary
	global dictionary_strategies

	balance = get_portfolio(5000, dictionary_strategies['growth'])
	print "before"
	for key, value in g_stock_dictionary.items():
		print key, value
	print "balance is ", balance


	balance = get_portfolio(balance, dictionary_strategies['growth'])
	print "*" * 20

	for key, value in g_stock_dictionary.items():
		print key, value

	print "balance is", balance


test_command_line()