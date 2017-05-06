
from yahoo_finance import Share as sh
import operator
import urllib2

#Global
growth_stocks = ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
g_stock_dictionary = {}
dictionary_strategies = {
	'growth' : growth_stocks
}

def get_eligible_stock(stock_dictionary, amount):
	sorted_stocks_by_peg = sorted(stock_dictionary.items(), key=operator.itemgetter(1), reverse=True)

	for each_element in sorted_stocks_by_peg:
		stock_symbol = each_element[0]
		stock_details = each_element[1]
		stock_price = stock_details['price']
		if stock_price < amount:
			return stock_symbol



def get_portfolio(amount, stock_type):
	global g_stock_dictionary
	sum_peg = 0
	total_balance = 0
	stock_dictionary = {}

	for each_stock in stock_type:
		internal_dictionary = {}
		stock = None
		try:
			stock = sh(each_stock)
		except urllib2.HTTPError:
			print "Server error - Retrying"
			return amount

		price = float(stock.get_price())

		if(price > amount):
			continue

		internal_dictionary['price'] = float(price)
		internal_dictionary['peg'] = float(stock.get_price_earnings_growth_ratio())
		
		#calculate sum here for later on
		sum_peg += internal_dictionary['peg']

		stock_dictionary[each_stock] = internal_dictionary


	for each_stock in stock_dictionary.keys():
		each_stock_price = float(stock_dictionary[each_stock]['price'])
		each_stock_peg = stock_dictionary[each_stock]['peg']
		each_stock_ratio = float(each_stock_peg)/sum_peg	
		each_stock_amount = float(amount * each_stock_ratio)
		
		each_stock_count = int(each_stock_amount/each_stock_price)
		total_balance += (each_stock_amount % each_stock_price)

		stock_dictionary[each_stock]['ratio'] = each_stock_ratio
		stock_dictionary[each_stock]['amount'] = each_stock_amount
		stock_dictionary[each_stock]['count'] = each_stock_count

		#if dictionary was already there
		if bool(g_stock_dictionary) == True:
			g_stock_dictionary[each_stock]['count'] += each_stock_count
			g_stock_dictionary[each_stock]['amount'] += each_stock_amount


	#check if we have a problem
	if total_balance >= amount:
		stock_symbol = get_eligible_stock(stock_dictionary, amount)
		print "chosen stock: ", stock_symbol
		pass

	#get new stocks with highest peg AND < price


	print stock_dictionary

	#if dictionary was empty
	if bool(g_stock_dictionary) == False:
		print 'updating once'
		g_stock_dictionary = stock_dictionary.copy()

	return total_balance


def test_command_line():
	global g_stock_dictionary
	global dictionary_strategies
	balance = 100000

	while balance > 0:
		balance = get_portfolio(balance, dictionary_strategies['growth'])
		print "new balance =", balance
		print "------" * 40




test_command_line()