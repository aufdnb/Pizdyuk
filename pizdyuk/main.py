import argparse
import time
import market.stock_manager as stocks
import market.user_manager as users
import market.trader as trade
from pzd_http import PizdyukServer, PizdyukRequestHandler
from pzd_errors import PizdyukError, PizdyukErrorHandler
from pzd_logging import PizdyukLogger

parser = argparse.ArgumentParser()
parser.add_argument('--server_address', help="Server address, if not provided defaults to localhost", type=str, default="localhost")
parser.add_argument('--port', help="The port to start the server on, if not provided defaults to 8080", type=int, default=8080)
parser.add_argument('--tick', help="The time it takes to update a stock. Defaults to 1", type=int, default=1)
parser.add_argument('--save_users', help="If set to true, will save the users of the current session. Defaults to false", type=bool, default=False)

args = parser.parse_args()
server_address = args.server_address
port = args.port
tick = args.tick
save_users = args.save_users

server = PizdyukServer(server_address, PizdyukRequestHandler, port)
stock_manager = stocks.get_manager()
user_manager = users.get_manager()
trader = trade.get_trader()
logger = PizdyukLogger.get_logger()
error_handler = PizdyukErrorHandler()

try:
    server.start()

    while True:
        try:
            stock_manager.update()
            user_manager.update()
            trader.update()
            time.sleep(tick)
        except IndexError:
            logger.log_info("Reached the end of stock data. Closing")
            raise Exception()
        except PizdyukError as e:
            error_handler.handle(e)
            continue
except Exception as e:
    logger.log_fatal("Error occurred! {}".format(e))
finally:
    if save_users:
        user_manager.save_users()
    server.close()