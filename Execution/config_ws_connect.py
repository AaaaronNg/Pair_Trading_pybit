from config_execution import ws_public_url
from config_execution import ticker_1
from config_execution import ticker_2


from pybit import usdt_perpetual
from time import sleep


ws_linear = usdt_perpetual.WebSocket(
    test=True,
    ping_interval=30,  # the default is 30
    ping_timeout=10,  # the default is 10
    domain="bybit"  # the default is "bybit"
)

def handle_message(msg):
    print(msg)
# To subscribe to multiple symbols,
# pass a list: ["BTCUSDT", "ETHUSDT"]
ws_linear.orderbook_25_stream(
    handle_message, [ticker_1, ticker_2]
)


while True:
    sleep(1)