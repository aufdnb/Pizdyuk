import pzd_utils as utils
import market.stock_manager as stock_manager
from market.portfolio import Portfolio
from market.core import MarketObjectBase 
from pzd_errors import PzdNotLoadedError, PzdInvalidOperationError

class User(MarketObjectBase):
    """ Class to represent a user """
    def __init__(self, name, id=None, balance = 0, portfolio_members=None):
        """
            User class constructor

            Args:
            name (str) - User name
            id (str) - User id, must be unique. If not provided, is generated
            portfolio_members ([PortfolioMember]) - portfolio_members of the current user
        """
        self.__name = name
        self.__id = id
        self.__balance = balance

        if not id:
            self.__id = utils.get_unique_id()

        self.__portfolio = Portfolio(id, portfolio_members)

    def update(self):
        """
            Updates user portfolio
        """
        self.__portfolio.update()

    def can_add_position(self, symbol, amount):
        """
            Returns True if a position can be added

            Args:
            symbol (str) - Stock symbol to add
            amount (int) - position size to add
        """
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            return False

        buy_price = stock.price * amount

        return buy_price <= self.__balance

    def can_remove_position(self, symbol, amount):
        """
            Returns True if a position can be removed

            Args:
            symbol (str) - Stock symbol to remove
            amount (int) - position size to remove
        """
        owned_amount = self.__portfolio.get_position_size(symbol)
        print("Own {0} remove {1}".format(owned_amount, amount))
        return owned_amount >= amount 

    def add_position(self, symbol, amount):
        """
            Adds specified position if possible.

            Args:
            symbol (str) - Stock symbol to add
            amount (int) - position size to add
        """
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise PzdNotLoadedError("{} is not loaded!".format(symbol))

        if not self.can_add_position(symbol, amount):
            raise PzdInvalidOperationError("Not enough funds to buy {0} shares of {1}. Buy price ${2}. Your Balance ${3}".format(amount, stock.symbol, buy_price, self.__balance))


        self.__balance = self.__balance - (stock.price * amount)
        self.__portfolio.add_position(symbol, stock.price, stock.current_time, amount)

    def remove_position(self, symbol, amount):
        """
            Removes specified position.

            Args:
            symbol (str) - Stock symbol to remove
            amount (int) - position size to remove
        """

        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise PzdNotLoadedError("{} is not loaded!".format(symbol))

        if not self.can_remove_position(symbol, amount):
            raise PzdInvalidOperationError("The sell amount requested exceeds the owned amount")

        self.__portfolio.remove_position(symbol, stock.price, stock.current_time, amount)

    def add_funds(self, amount):
        """
            Increases user balance by specified amount

            Args:
            amount (int) - amount to increase user balance by.
        """
        self.__balance = self.__balance + amount

    def get_object_info(self):
        """
            Returns a dict representing object
        """
        return {
            "name": self.__name,
            "user_id": self.__id,
            "balance": self.__balance,
            "portfolio": self.__portfolio.get_object_info()
        }

    @property
    def name(self):
        """
            A getter function for user's name
        """
        return self.__name

    @property
    def id(self):
        """
            A getter function for user's id
        """
        return self.__id

    @property
    def balance(self):
        """
            A getter function for user's balance
        """
        return self.__balance