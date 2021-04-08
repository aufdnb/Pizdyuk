import pzd_constants as const
from pzd_errors import PzdNotFoundError, PzdInvalidOperationError, ErrorSeverity
from pzd_logging import PizdyukLogger
from market.core import MarketObjectBase
from datetime import datetime
import market.stock_manager as stock_manager

class Portfolio(MarketObjectBase):
    """ Class to represet a portfolio """
    def __init__(self, user_id, portfolio_members=None):
        """ 
            Portfolio constructor

            Args:
            user_id (str) - id of a user who owns the portfolio
            protfolio_memebers [Optional] (dict[str, PortfolioMembers]) - collection of portfolio members
        """

        self.__user_id = user_id
        self.__portfolio_members = {}

        if portfolio_members:
            self.__portfolio_members = portfolio_members

    def update(self):
        """
            Calls update on each of its portfolio members
        """
        for symbol, portfolio_member in self.__portfolio_members.items():
            portfolio_member.update()


    def add_position(self, symbol, price, date, amount):
        """
            Tries to add a position to the portfolio.
            Will update or create a portfolio member depending on whether it exists or not.

            Args:
            symbol (str) - Stock symbol
            price (float) - current Stock price
            date (datetime) - current (simulated) date
            amount (int)  - the size of the position to add
        """
        portfolio_member = self.__portfolio_members.get(symbol, None)

        if not portfolio_member:
            portfolio_member = self.__create_portfolio_member(symbol)
            self.__portfolio_members[symbol] = portfolio_member

        portfolio_member.add_position(price, date, amount)

    def remove_position(self, symbol, price, date, amount):
        """
            Tries to remove a position from the portfolio.

            Args:
            symbol (str) - Stock symbol
            price (float) - current Stock price
            date (datetime) - current (simulated) date
            amount (int)  - the size of the position to add
        """
        portfolio_member = self.__portfolio_members.get(symbol, None)

        if not portfolio_member:
            raise PzdNotFoundError("Cannot remove position that does not exist")

        portfolio_member.remove_position(price, date, amount)

    def has_member(self, symbol):
        """
            Returns true if a stock with symbol exists

            Args:
            symbol (str) - Stock symbol
        """
        return bool(self.__portfolio_members.get(symbol, None))

    def get_position_size(self, symbol):
        """
            Returns the position size of the stock with the provided symbol.

            Args:
            symbol (str) - Stock symbol
        """
        portfolio_member = self.__portfolio_members.get(symbol, None)

        if not portfolio_member:
            return 0

        return portfolio_member.position_size

    def get_object_info(self):
        """
            Returns a dictionary representing the object's information
        """

        info = {}

        for symbol, member in self.__portfolio_members.items():
            info[symbol] = member.get_object_info()

        return info
        
    def __create_portfolio_member(self, symbol):
        manager = stock_manager.get_manager()
        stock = manager.get_stock(symbol)

        if not stock:
            raise PzdNotFoundError("{} is not loaded!".format(symbol))

        return PortfolioMember(stock)
        

class PortfolioMember(MarketObjectBase):
    def __init__(self, stock, average_price=0, performance_percentage=0, performance=0, position_size=0, activity=[]):
        """
            Portfolio Member constructor

            Args:
            stock (Stock) - the stock which PortfolioMember represents
        """
        self.__stock = stock
        self.__average_price = average_price
        self.__performance_percentage = performance_percentage
        self.__performance = performance
        self.__position_size = position_size
        self.__activity = activity

    def update(self):
        """
            Updates the performance values
        """
        if self.__position_size != 0:
            self.__performance = self.__average_price - self.__stock.price
            self.__performance_percentage = (self.__average_price / self.__stock.price - 1) * 100

    def add_position(self, price, date, amount):
        """
            Tries to add a position to the portfolio.

            Args:
            symbol (str) - Stock symbol
            price (float) - current Stock price
            date (datetime) - current (simulated) date
            amount (int)  - the size of the position to add
        """
        self.__average_price = (self.__average_price * self.__position_size + price * amount) / (self.__position_size + amount)
        date_str = datetime.strftime(date, const.DATE_FORMAT)
        self.__activity.append(("BUY", date_str, price, amount))
        self.__position_size = self.__position_size + amount
        logger = PizdyukLogger.get_logger()
        logger.log_info("Position added!")

    def remove_position(self, price, date, amount):
        """
            Tries to remove a position from the portfolio.

            Args:
            symbol (str) - Stock symbol
            price (float) - current Stock price
            date (datetime) - current (simulated) date
            amount (int)  - the size of the position to add
        """
        if self.__position_size >= amount:
            date_str = datetime.strftime(date, const.DATE_FORMAT)

            if (self.__position_size - amount) != 0:
                self.__average_price = (self.__average_price * self.__position_size - price * amount) / (self.__position_size - amount)
            else:
                self.__average_price = 0

            self.__activity.append(("SELL", date_str, price, amount))
            self.__position_size = self.__position_size - amount
            return

        raise PzdInvalidOperationError("Not enought shares to sell! {}".format(self.__stock.symbol))

    def get_object_info(self):
        """
            Returns a dictionary representing the object's information
        """
        return {
            "symbol": self.__stock.symbol,
            "current_price": self.__stock.price,
            "average_price": self.__average_price,
            "performance": self.__performance,
            "performance_percentage": self.__performance_percentage,
            "num_shares": self.__position_size,
            "activity": self.__activity
        }

    @property
    def performance(self):
        """
            A getter function for 'performance' attribute
        """
        return self.__performance

    @property
    def performance_percentage(self):
        """
            A getter function for 'performance_percentage' attribute
        """
        return self.__performance_percentage

    @property
    def activity(self):
        """
            Returns a string representation of portfolio activity
        """
        representation = ""

        for info in self.__activity:
            representation = representation + str(info) + "\n"

        return representation

    @property
    def total_value(self):
        """
            A getter function for a total value of the portfolio
        """
        return self.__position_size * self.__average_price

    @property
    def position_size(self):
        """
            A getter function for "position_size" attribute
        """
        return self.__position_size 

    @property
    def average_price(self):
        """
            A getter function for the average price of the portfolio
        """
        return self.__average_price
    