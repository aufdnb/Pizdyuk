import time
import market.stock_manager as stocks
import market.user_manager as users
import market.trader as trade
from pzd_http import PizdyukServer, PizdyukRequestHandler


server = PizdyukServer("localhost", PizdyukRequestHandler)
server.start()

try:
    stock_manager = stocks.get_manager()
    user_manager = users.get_manager()
    trader = trade.get_trader()

    while True:
        try:
            stock_manager.update()
            user_manager.update()
            trader.update()
            time.sleep(1)
        except:
            server.close()
            raise
            break
except Exception as e:
    server.close()
    raise
# txt = None
# while txt != "exit":
#     txt = input("Type 'exit' to halt the program")