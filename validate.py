from yahoo_finance import Share as sh


stocks 	= ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN', 'ARW', 'COF', 'CI', 'FITB', 'USB', 'WFM', 'SBUX', 'MSFT', 
'SBUX', 'NSRGY', 'PORTX', 'ENS', 'EME', 'CVG', 'AXP', 'IXUS', 'VTI', 'ILTB', 'VTSMX', 'VXUS']


value_stocks 	= ['ARW', 'COF', 'CI', 'FITB', 'USB']

sum_peg = 0

for each in value_stocks:
	try:
		stock = sh(each)
		print stock.get_name(), " - ", stock.get_price_earnings_growth_ratio()
		sum_peg += float(stock.get_price_earnings_growth_ratio())
	except:
		continue

print sum_peg
