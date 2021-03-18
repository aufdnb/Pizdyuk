import parent_dir
from core import MarketObjectBase

class Stock(MarketObjectBase):
    """ Class to represent a stock """
    def __init__(self, symbol, stock_data):
        """ 
        Stock constructor

        Args:
        stock_data (list [(date (str),price (float)) ]): stock prices
        """

        self.__symbol = symbol
        self.__stock_data = stock_data
        self.__current_data_index = -1

    def update(self):
        self.__current_data_index = self.__current_data_index + 1

    @property
    def symbol(self):
        return self.__symbol

    @property
    def price(self):
        return self.__stock_data[self.__current_data_index][1]

    @property
    def current_time(self):
        return self.__stock_data[self.__current_data_index][0]