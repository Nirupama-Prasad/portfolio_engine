
from yahoo_finance import Share as sh


growth_stocks = ['AAPL', 'FB', 'VMW']

dictionary_strategies = {
	'growth' : growth_stocks
	}


def get_portfolio(amount, stock_type):
	stock_dictionary = {}

	for each_stock in stock_type:
		internal_dictionary = {}
		stock = sh(each_stock)
		internal_dictionary['price'] = stock.get_price()
		internal_dictionary['peg'] = stock.get_price_earnings_growth_ratio()
		stock_dictionary[each_stock] = internal_dictionary

	print stock_dictionary


def test_command_line():
	get_portfolio(5000, dictionary_strategies['growth'])


test_command_line()