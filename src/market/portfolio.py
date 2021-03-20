import pzd_constants as const
from market.core import MarketObjectBase
from datetime import datetime
import market.stock_manager

class Portfolio(MarketObjectBase):
    """ Class to represet a portfolio """
    def __init__(self, user_id, portfolio_members=None):
        """ 
            Portfolio constructor

            Args:
            user_id (string) - id of a user who owns the portfolio
            protfolio_memebers [Optional] (dict{str: PortfolioMembers}) - collection of portfolio members
        """

        self.__user_id = user_id
        self.__portfolio_members = {}

        if portfolio_members:
            self.__portfolio_members = portfolio_members

    def update(self):
        for symbol, portfolio_member in self.__portfolio_members.items():
            portfolio_member.update()


    def add_position(self, symbol, price, date, amount):
        portfolio_member = self.__portfolio_members.get(symbol, None)

        if not portfolio_member:
            portfolio_member = self.__create_portfolio_member(symbol)

        portfolio_member.add_position(price, date, amount)

    def remove_position(self, symbol, price, date, amount):
        portfolio_member = self.__portfolio_members.get(symbol, None)

        if not portfolio_member:
            portfolio_member = self.__create_portfolio_member(symbol)

        portfolio_member.remove_position(price, date, amount)

    def __create_portfolio_member(self, symbol):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise RuntimeError("{} is not loaded!".format(symbol))

        return PortfolioMember(stock)
        

class PortfolioMember(MarketObjectBase):
    def __init__(self, stock):
        """
            Portfolio Member constructor

            Args:
            stock (Stock) - the stock which PortfolioMember represents
        """
        self.__stock = stock
        self.__average_price = 0
        self.__performance_percentage = 0
        self.__performance = 0
        self.__position_size = 0
        self.__activity = []

    def update(self):
        self.__performance = self.__average_price - self.__stock.price
        self.__performance_percentage = self.__performance / self.__bought_price

    def add_position(self, price, date, amount):
        self.__average_price = (self.__average_price * self.__position_size + price * amount) / (self.__position_size + amount)
        date_str = datetime.strftime(date, const.DATE_FORMAT)
        self.__activity.append(("BUY", date_str, price, amount))
        self.__position_size = self.__position_size + amount

    def remove_position(self, price, date, amount):
        if self.__position_size >= amount:
            date_str = datetime.strftime(date, const.DATE_FORMAT)
            self.__average_price = (self.__average_price * self.__position_size - price * amount) / (self.__position_size - amount)
            self.__activity.append(("SELL", date_str, price, amount))
            self.__position_size = self.__position_size - amount

        raise RuntimeError("Not enought shares to sell! {}".format(self.__stock.symbol))

    @property
    def performance(self):
        return self.__performance

    @property
    def performance_percentage(self):
        return self.__performance_percentage

    @property
    def activity(self):
        representation = ""

        for info in self.__activity:
            representation = representation + str(info) + "\n"

        return representation

    @property
    def total_value(self):
        return self.__position_size * self.__average_price 
    