import pandas as pd
import warnings
import json

warnings.simplefilter(action="ignore", category=FutureWarning)

# Baic Idea
# https://blog.quantinsti.com/pairs-trading-basics/


from func_get_symbols import get_tradable_symbols
from func_prices_json import store_price_history
from func_cointegration import get_cointegrated_pairs
from func_plot_trends import plot_trends
# strategy code


if __name__ == "__main__":

	# Step 1 - Get list of symbols
	print("Getting symbols ...")
	sym_response = get_tradable_symbols()
	print(sym_response)
	

	# Step 2 - Construct and save price history
	print("Constructing and saving price data to JSON")
	if len(sym_response) > 0:
		store_price_history(sym_response)

	# Step 3 - find cointegrated pairs
	print("Calculating co-integration...")
	with open("1_price_list.json") as json_file:
		price_data = json.load(json_file)
		if len(price_data) > 0:
			coint_pairs = get_cointegrated_pairs(price_data)
	print("done")

	# Step 4 - plot trends and save for backtesting

	print("Plotting trends")
	symbol_1 = "ENJUSDT"
	symbol_2 = "FTMUSDT"
	with open("1_price_list.json") as json_file:
		price_data = json.load(json_file)
		if len(price_data)>0:
			plot_trends(symbol_1, symbol_2, price_data)




