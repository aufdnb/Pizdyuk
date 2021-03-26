import market.user_manager as user_manager
import market.stock_manager as stock_manager
from market.core import MarketObjectBase, Action
from queue import Queue

TRADER = None

def get_trader():
    global TRADER
    if not TRADER:
        TRADER = Trader()

    return TRADER

class Trader(MarketObjectBase):
    def __init__(self):
        global TRADER

        if TRADER:
            raise RuntimeError("Trader instance already exists! Trader class should not be instantiated more than once!")

        self.__ordersQueue = Queue()

    def update(self):
        while not self.__ordersQueue.empty():
            order = self.__ordersQueue.get()
            print("Executing")
            order.execute()

    def handle_order(self, order_type, **kwargs):
        is_valid, error_msg = self.__validate_order(order_type, **kwargs)

        if not is_valid:
            return (400, {"error": error_msg})

        switch = {
            "buy": self.__create_buy_order,
            "sell": self.__create_sell_order,
        }

        order = switch[order_type](**kwargs)
        print("adding to queue")
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