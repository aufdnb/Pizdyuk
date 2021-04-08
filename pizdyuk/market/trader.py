import market.user_manager as user_manager
import market.stock_manager as stock_manager
from market.core import MarketObjectBase, Action
from pzd_errors import PzdLogicError
from pzd_logging import PizdyukLogger
from queue import Queue

TRADER = None

def get_trader():
    """
        Updates the current price of the stock
    """
    global TRADER
    if not TRADER:
        TRADER = Trader()

    return TRADER

class Trader(MarketObjectBase):
    def __init__(self):
        """
            Constructor for the Trader class
        """
        global TRADER

        if TRADER:
            raise PzdLogicError("Trader instance already exists! Trader class should not be instantiated more than once!")

        self.__ordersQueue = Queue()
        self.__logger = PizdyukLogger.get_logger()

    def update(self):
        """
            If there are any queued order executes them
        """
        while not self.__ordersQueue.empty():
            order = self.__ordersQueue.get()
            self.__logger.log_info("Executing order!")
            order.execute()

    def handle_order(self, order_type, **kwargs):
        """
            Handles orders. If a valid order creates and puts to the queue
        """
        is_valid, error_msg = self.__validate_order(order_type, **kwargs)

        if not is_valid:
            return (400, {"error": error_msg})

        switch = {
            "buy": self.__create_buy_order,
            "sell": self.__create_sell_order,
        }

        order = switch[order_type](**kwargs)
        self.__logger.log_info("Adding to order to the queue.")
        self.__ordersQueue.put(order)

        return (200, {})

    def __validate_order(self, order_type, **kwargs):
        user_id = kwargs.pop("user_id", None)
        symbol = kwargs.pop("symbol", None)
        num_shares = kwargs.pop("num_shares", None)
        u_manager = user_manager.get_manager()
        s_manager = stock_manager.get_manager()

        if not user_id:
            return (False, "Field 'user_id' missing")

        if not symbol:
            return (False, "Field 'symbol' missing")

        if not num_shares:
            return (False, "Field 'num_shares' missing")

        user = u_manager.get_user(user_id)
        stock = s_manager.get_stock(symbol)

        if not user:
            return (False, "No user with id: {} found".format(user_id))

        if not stock:
            return (False, "No stock with symbol {} found".format(symbol))

        if order_type == "buy" and not user.can_add_position(symbol, num_shares):
            return (False, "Not sufficient funds to buy {0} shares of {1}".format(num_shares, symbol))
        elif order_type == "sell" and not user.can_remove_position(symbol, num_shares):
            return (False, "Invalid sell order. User owns less shares than tries to sell")

        return (True, "")

    def __create_buy_order(self, **kwargs):
        """ returns an action which represents the market buy """
        user_id = kwargs.pop("user_id", None)
        symbol = kwargs.pop("symbol", None)
        num_shares = kwargs.pop("num_shares", None)

        manager = user_manager.get_manager()
        user = manager.get_user(user_id)
        return Action(user.add_position, symbol, num_shares)

    def __create_sell_order(self, **kwargs):
        """ returns an action which represents the market sell """
        user_id = kwargs.pop("user_id", None)
        symbol = kwargs.pop("symbol", None)
        num_shares = kwargs.pop("num_shares", None)

        manager = user_manager.get_manager()
        user = manager.get_user(user_id)
        return Action(user.remove_position, symbol, num_shares)