
from yahoo_finance import Share as sh
import operator
import urllib2

#Global
growth_stocks = ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
value_stocks = ['ARW', 'COF', 'CI', 'FITB', 'USB']
portfolio = {}
dictionary_strategies = {
	'growth' 	: growth_stocks,
	'value'		: value_stocks
}
uninvested_amount = 0

def get_eligible_stock(stock_dictionary, amount):
	sorted_stocks_by_peg = sorted(stock_dictionary.items(), key=operator.itemgetter(1), reverse=True)

	for each_element in sorted_stocks_by_peg:
		stock_symbol = each_element[0]
		stock_details = each_element[1]
		stock_price = stock_details['price']
		if stock_price < amount:
			return stock_symbol



def get_portfolio(amount, stock_type):
	global portfolio
	global uninvested_amount
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
		internal_dictionary['name'] = stock.get_name()
		
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
		if bool(portfolio) == True:
			portfolio[each_stock]['count'] += each_stock_count
			portfolio[each_stock]['amount'] += each_stock_amount


	#check if we have a problem
	if total_balance >= amount:
		stock_symbol = get_eligible_stock(stock_dictionary, amount)
		print "chosen stock: ", stock_symbol
		stock_price = stock_dictionary[stock_symbol]['price']
		extra_stocks = int(total_balance / stock_price)
		amount_spent = extra_stocks * stock_price
		total_balance = total_balance - amount
		portfolio[stock_symbol]['count'] += extra_stocks
		portfolio[stock_symbol]['amount'] += amount_spent
		return total_balance

	if total_balance == 0:
		print 'amount uninvested: ', amount
		uninvested_amount =  amount
		return 0

	#get new stocks with highest peg AND < price

	#if dictionary was empty
	if bool(portfolio) == False:
		print 'updating once'
		portfolio = stock_dictionary.copy()

	return total_balance


def test_command_line():
	global portfolio
	global dictionary_strategies
	balance = 5000

	while balance > 0:
		balance = get_portfolio(balance, dictionary_strategies['value'])
		print "new portfolio: "
		print portfolio
		print "------" * 40
		print "new balance =", balance





test_command_line()