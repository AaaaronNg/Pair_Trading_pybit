
from pybit import usdt_perpetual
# config variables


# ticker
mode = "test"
ticker_1 = "BTCUSDT" # BALUSDT
ticker_2 = "ETHUSDT" # JASMYUSDT
signal_positive_ticker = ticker_2
signal_negative_ticker = ticker_1


# it depends on your sym_1 and sym_2
rounding_ticker_1 = 2
rounding_ticker_2 = 2
quantity_rounding_ticker_1 = 3
quantity_rounding_ticker_2 = 2



limit_order_basis = True

tradable_capital_usdt = 2000 # total tradable capital to be split between both pairs
stop_loss_fail_safe = 0.15 # stop loss at market order in cas of drastic event
signal_trigger_thresh = 0.2 # z-score threshold 

timeframe = 60
kline_limit = 200
z_score_window = 21


# live api
api_key_mainnet = ""
api_secret_mainnet = ""


# test API
api_key_testnet = "NxHj88GUceVJNGQiUL"
api_secret_testnet = "6EwFeftts97jarOxwK1pbAsWm0ckvdOAsz73"

# selected api
api_key = api_key_testnet if mode == "test" else api_key_mainnet
api_secret = api_secret_testnet if mode == "test" else api_secret_testnet

# selected URL
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"
ws_public_url = "wss://stream-testnet.bybit.com/realtime_public" if mode == "test" else "wss://stream.bybit.com/realtime_public"


# session activation
session = usdt_perpetual.HTTP(
    endpoint=api_url
    )
# session_private = HTTP(api_url, api_key)
session_private = usdt_perpetual.HTTP(
    endpoint=api_url,
    api_key=api_key,
    api_secret=api_secret
)