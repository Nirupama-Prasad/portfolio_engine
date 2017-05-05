from flask import Flask
from flask import request
from flask import render_template

import lookup as lk
import json

app = Flask(__name__)
 
@app.route("/")
def enter():
	print "here"
	return render_template('index.html')	

@app.route("/calculate", methods=["POST"])
def runn():
	data = request.data

	ticker_symbol = request.form["stock_symbol"]
	stock_dict = lk.pull_stock(ticker_symbol)

	if stock_dict is None:
		abort(make_response("Integrity Error", 400))


	print stock_dict
	
	json_values = json.dumps(stock_dict)
	return json_values
 
if __name__ == "__main__":
    app.run()