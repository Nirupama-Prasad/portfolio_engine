

ALGORITHM:
----------
x1. make static lists of all stocks for all strategies (3 per strat)
x2. for each stock, get price, PEG
x3. find out ranking and ratios per stock
x4. get amount per stock + round down number of stocks
x5. figure out what to do with remainder
x6. catch http error
x7. add remaining lists
x8. performance caching
x9. plot each stocks and portfolio chart

FRONT END INPUT:
-----------
1. dropdown lists for strategy picking
2. text box for amount
3. portfolio values for multiple strategy

FRONT END OUTPUT:
-----------
1. P elements with portfolio details:
2. for each in stock:
	amount spent - pie chart
3. portfolio image itself

BACKEND 
1. pass information back

ERROR CHECKS:
1. for invalid symbols, etc
2. httperror in lookup.py while doing history
3. empty input from html