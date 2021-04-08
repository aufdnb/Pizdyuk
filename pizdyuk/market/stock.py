from market.core import MarketObjectBase

class Stock(MarketObjectBase):
    """ Class to represent a stock """
    def __init__(self, symbol, stock_data):
        """ 
        Stock constructor

        Args:
        stock_data (list [(date (datetime),price (float)) ]): stock prices
        """

        self.__symbol = symbol
        self.__stock_data = stock_data
        self.__current_data_index = -1

    def update(self):
        """
            Updates the current price of the stock
        """
        self.__current_data_index = self.__current_data_index + 1

    @property
    def symbol(self):
        """
            Getter function for the stock symbol
        """
        return self.__symbol

    @property
    def price(self):
        """
            Getter function for the stock price
        """
        return self.__stock_data[self.__current_data_index][1]

    @property
    def current_time(self):
        """
            Getter function for the stock's current time
        """
        return self.__stock_data[self.__current_data_index][0]