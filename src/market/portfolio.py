import parent_dir
from core import MarketObjectBase

class Portfolio(MarketObjectBase):
    """ Class to represet a portfolio """
    def __init__(self, user_id, portfolio_members=None):
        """ 
            Portfolio constructor

            Args:
            user_id (string) - id of a user who owns the portfolio
            protfolio_memebers [Optional] (list[PortfolioMembers]) - collection of portfolio members
        """

        self.__user_id = user_id
        self.__portfolio_members = []

        if portfolio_members:
            self.__portfolio_members = portfolio_members

    def update(self):
        for portfolio_member in self.__portfolio_members:
            portfolio_member.update()


class PortfolioMember(MarketObjectBase):

    def __init__(self, stock, bought_price, bought_time):
        """
            Portfolio Member constructor

            Args:
            stock (Stock) - the stock which PortfolioMember represents
            bought_price (float) - the price at which the stock was bought
            bought_time (datetime) - the simulated time when the stock was bought
        """
        self.__stock = stock
        self.__bought_price = bought_price
        self.__bought_time = bought_time

        self.__performance_percentage = 0
        self.__performance = 0

    def update(self):
        self.__performance = self.__bought_price - self.__stock.price
        self.__performance_percentage = self.__performance / self.__bought_price

    @property
    def performance(self):
        return self.__performance

    @property
    def performance_percentage(self):
        return self.__performance_percentage
    