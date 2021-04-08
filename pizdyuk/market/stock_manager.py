import os
import sys
import pzd_constants as const
from market.core import MarketObjectBase
from market.stock import Stock
from pzd_errors import PzdLogicError
from pzd_io import get_stock_data
from pzd_utils import datetime_to_str

MANAGER = None

def get_manager():
    """
        Similar to getInstance in Singleton paradigm in other languages
    """
    global MANAGER
    if not MANAGER:
        MANAGER = StockManager()
    
    return  MANAGER

class StockManager(MarketObjectBase):
    """ Class that's manages the stocks """
    def __init__(self):
        global MANAGER
        if MANAGER:
            raise PzdLogicError("Stock manager instance already exists. StockManager should not be initialized more than once")

        self.__stocks = {}
        self.__load()

    def update(self):
        """
            Updates all of the stocks
        """
        for symbol, stock in self.__stocks.items():
            stock.update()

    def get_stock(self, symbol):
        """
            Returns: [Stock] if symbol found else [None]
        """
        return self.__stocks.get(symbol, None)

    def handle_request(self, **kwargs):
        """
            Handles request to get the information of the stock
        """
        symbol = kwargs.pop("symbol", None)

        if not symbol:
            return (400, {"error" : "Stock symbol missing!"})

        stock = self.get_stock(symbol)

        if not stock:
            return (404, {"error": "Symbol {} not found".format(symbol)})

        return (200, {
            "symbol": symbol,
            "current_time": datetime_to_str(stock.current_time),
            "price": stock.price
        })

    def __load(self):
        data_path = const.STOCK_DATA_PATH
        src_dir = os.path.dirname(os.path.dirname(__file__))
        data_path = os.path.join(src_dir, data_path)

        for root, dirs, files in os.walk(data_path):
            for f in files:
                symbol = os.path.splitext(f)[0]
                stock_data = get_stock_data("{0}/{1}".format(data_path, f))
                s = Stock(symbol, stock_data)
                self.__stocks[symbol] = s


    