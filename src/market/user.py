import pzd_utils as utils
import market.stock_manager as stock_manager
from market.portfolio import Portfolio
from market.core import MarketObjectBase 

class User(MarketObjectBase):
    """ Class to represent a user """
    def __init__(self, name, id=None, balance = 0, portfolio_members=None):
        self.__name = name
        self.__id = id
        self.__balance = balance

        if not id:
            self.__id = utils.get_unique_id()

        self.__portfolio = Portfolio(id, portfolio_members)

    def update(self):
        self.__portfolio.update()

    def add_position(self, symbol, amount):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise RuntimeError("{} is not loaded!".format(symbol))

        print("{0}, {1}, {2}".format(stock.price, amount, self.__balance))

        if stock.price * amount > self.__balance:
            raise RuntimeError("Not enough funds to buy {0} shares of {1}".format(amount, stock.symbol))

        self.__portfolio.add_position(symbol, stock.price, stock.current_time, amount)

    def remove_position(self, symbol, amount):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise RuntimeError("{} is not loaded!".format(symbol))

        self.__portfolio.remove_position(symbol, stock.price, stock.current_time, amount)

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def balance(self):
        return self.__balance