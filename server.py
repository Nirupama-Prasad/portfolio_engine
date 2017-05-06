from flask import Flask
from flask import request
from flask import render_template

import lookup as lk
import json
import stock_bot as sb

app = Flask(__name__)
 
@app.route("/")
def enter():
	print "here"
	return render_template('index.html')	

@app.route("/calculate", methods=["POST"])
def runn():
	data = request.data
	total_amount = float(request.form['total_amount'])
	strategy_1 = request.form['strategy_1']
	strategy_2 = request.form['strategy_2']

	portfolio = sb.test_command_line(total_amount, strategy_1.lower())
	# ticker_symbol = request.form["stock_symbol"]
	# stock_dict = lk.pull_stock(ticker_symbol)	
	json_values = json.dumps(portfolio)
	return json_values
 	
if __name__ == "__main__":
    app.run()