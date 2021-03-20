import time
import market.stock_manager as stock_manager
from pzd_http import PizdyukServer, PizdyukRequestHandler


manager = stock_manager.get_manager()
server = PizdyukServer("localhost", PizdyukRequestHandler)
server.start()

time.sleep(60)

server.close()