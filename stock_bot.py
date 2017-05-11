
from yahoo_finance import Share as sh
import operator
import urllib2
import lookup

#Global
growth_stocks 	= ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
value_stocks 	= ['ARW', 'COF', 'CI', 'FITB', 'USB']
ethical_stocks 	= ['WFM', 'SBUX', 'MSFT', 'SBUX', 'NSRGY']
quality_stocks 	= ['PORTX', 'ENS', 'EME', 'CVG', 'AXP']
index_stocks 	= ['IXUS', 'VTI', 'ILTB', 'VTSMX', 'VXUS']

portfolio = {}
dictionary_strategies = {
	'growth' 	: growth_stocks,
	'value'		: value_stocks,
	'ethical'	: ethical_stocks,
	'quality'	: quality_stocks,
	'index'		: index_stocks
}
uninvested_amount = 0
is_stock_drawn = False
global_stock_index = {}
is_ratio_method_over = False

def clear_everything():
	global global_stock_index, portfolio, is_stock_drawn, is_ratio_method_over, uninvested_amount
	global_stock_index = {}
	portfolio = {}
	is_stock_drawn = False
	is_ratio_method_over = False
	uninvested_amount = 0
	lookup.clear_everything()
	#execute clean script here


def get_eligible_stock(stock_dictionary, amount):
	sorted_stocks_by_peg = sorted(stock_dictionary.items(), key=operator.itemgetter(1), reverse=True)

	for each_element in sorted_stocks_by_peg:
		stock_symbol = each_element[0]
		stock_details = each_element[1]
		stock_price = stock_details['price']
		if stock_price < amount:
			return stock_symbol

def cache_stocks(stock_type):
	for each_stock in stock_type:
		try:
			stock = sh(each_stock)
			global_stock_index[each_stock] = stock
		except urllib2.HTTPError:
			print "Server error - Retrying"
			return False
	return True

def generate_five_day():
	for each in global_stock_index.values():
		success = False
		while not success:
			success = lookup.draw_stock(each)
			#repeat for http errors

	lookup.draw_portfolio(portfolio)

def get_portfolio(amount, stock_type):
	global portfolio, uninvested_amount, is_stock_drawn, global_stock_index, is_ratio_method_over

	sum_peg = 0
	total_balance = 0
	stock_dictionary = {}

	for each_stock in stock_type:
		internal_dictionary = {}
		stock = global_stock_index[each_stock]

		price = float(stock.get_price())

		if(price > amount):
			continue

		internal_dictionary['price'] = float(price)
		individual_peg = float(stock.get_price_earnings_growth_ratio())
		if individual_peg == 0:
			individual_peg = 1
		internal_dictionary['peg'] = individual_peg
		internal_dictionary['name'] = stock.get_name()
		#calculate sum here for later on
		sum_peg += internal_dictionary['peg']
		stock_dictionary[each_stock] = internal_dictionary


	if is_ratio_method_over == False:
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


	#check if ratio method won't work:
	if total_balance >= amount:
		is_ratio_method_over = True
		stock_symbol = get_eligible_stock(stock_dictionary, amount)
		# print "chosen stock: ", stock_symbol
		stock_price = stock_dictionary[stock_symbol]['price']
		extra_stocks = int(total_balance / stock_price)
		amount_spent = extra_stocks * stock_price
		total_balance = total_balance - amount
		portfolio[stock_symbol]['count'] += extra_stocks
		portfolio[stock_symbol]['amount'] += amount_spent
		return total_balance

	if total_balance == 0:
		# print 'amount uninvested: ', amount
		uninvested_amount =  amount
		return 0

	#get new stocks with highest peg AND < price

	#if dictionary was empty
	if bool(portfolio) == False:
		#print 'updating once'
		portfolio = stock_dictionary.copy()

	return total_balance


def execute(amount, strategy):
	global portfolio, dictionary_strategies
	balance = amount

	stock_type = dictionary_strategies[strategy]
	ret = cache_stocks(stock_type)
	while ret != True:
		cache_stocks(stock_type)

	# print 'successfully looked up stocks'
	# print global_stock_index

	while balance > 0:
		balance = get_portfolio(balance, stock_type)
		# print "new portfolio: "
		# print portfolio
		# print "------" * 40
		# print "new balance =", balance

	#plot five day historical data for new stocks
	generate_five_day()
	return portfolio
	



#test_command_line('growth')