import user_manager
from core import MarketObjectBase, Action
from queue import Queue

__trader = None

def get_trader():
    if not __trader:
        __trader = Trader()

    return __trader

class Trader(MarketObjectBase):
    def __init__(self):
        global __trader

        if __trader:
            raise RuntimeError("Trader instance already exists! Trader class should not be instantiated more than once!")

        self.__ordersQueue = Queue()

    def update(self):
        while not self.__ordersQueue.empty():
            order = self.__ordersQueue.get()
            order.execute()

    def handle_order(self, order_type, **kwargs):
        switch = {
            "buy": self.create_buy_order,
            "sell": self.create_sell_order,
        }

        order = switch[order_type](**kwargs)
        self.__ordersQueue.put(order)

    def create_buy_order(self, **kwargs):
        """ returns an action which represents the market buy """
        user_id = kwargs.pop("user_id", None)
        symbol = kwargs.pop("symbol", None)
        num_shares = kwargs.pop("num_shares", None)
        
        manager = user_manager.get_manager()
        user = manager.get_user(user_id)
        return Action(user.add_position, symbol, num_shares)

    def create_sell_order(self, **kwargs):
        """ returns an action which represents the market sell """
        user_id = kwargs.pop("user_id", None)
        symbol = kwargs.pop("symbol", None)
        num_shares = kwargs.pop("num_shares", None)

        manager = user_manager.get_manager()
        user = manager.get_user(user_id)
        return Action(user.remove_position, symbol, num_shares)