import market.user_manager as user_manager
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
            order.execute()

    def handle_order(self, order_type, **kwargs):
        switch = {
            "buy": self.__create_buy_order,
            "sell": self.__create_sell_order,
        }

        order = switch[order_type](**kwargs)
        self.__ordersQueue.put(order)

        return ""

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