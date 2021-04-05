import pzd_utils as utils
import market.stock_manager as stock_manager
from market.portfolio import Portfolio
from market.core import MarketObjectBase 
from pzd_errors import PzdNotLoadedError, PzdInvalidOperationError

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

    def can_add_position(self, symbol, amount):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            return False

        buy_price = stock.price * amount

        return buy_price <= self.__balance

    def can_remove_position(self, symbol, amount):
        owned_amount = self.__portfolio.get_position_size(symbol)
        print("Own {0} remove {1}".format(owned_amount, amount))
        return owned_amount >= amount 

    def add_position(self, symbol, amount):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise PzdNotLoadedError("{} is not loaded!".format(symbol))

        if not self.can_add_position(symbol, amount):
            raise PzdInvalidOperationError("Not enough funds to buy {0} shares of {1}. Buy price ${2}. Your Balance ${3}".format(amount, stock.symbol, buy_price, self.__balance))


        self.__balance = self.__balance - (stock.price * amount)
        self.__portfolio.add_position(symbol, stock.price, stock.current_time, amount)

    def remove_position(self, symbol, amount):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise PzdNotLoadedError("{} is not loaded!".format(symbol))

        if not self.can_remove_position(symbol, amount):
            raise PzdInvalidOperationError("The sell amount requested exceeds the owned amount")

        self.__portfolio.remove_position(symbol, stock.price, stock.current_time, amount)

    def add_funds(self, amount):
        self.__balance = self.__balance + amount

    def get_object_info(self):
        return {
            "name": self.__name,
            "user_id": self.__id,
            "balance": self.__balance,
            "portfolio": self.__portfolio.get_object_info()
        }

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    @property
    def balance(self):
        return self.__balance