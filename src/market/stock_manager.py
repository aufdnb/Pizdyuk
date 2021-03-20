import os
import sys
import pzd_constants as const
from market.core import MarketObjectBase
from market.stock import Stock
from pzd_io import get_stock_data

MANAGER = None

def get_manager():
    global MANAGER
    if not MANAGER:
        MANAGER = StockManager()
    
    return  MANAGER

class StockManager(MarketObjectBase):
    """ Class that's manages the stocks """
    def __init__(self):
        global MANAGER
        if MANAGER:
            raise RuntimeError("Stock manager instance already exists. StockManager should not be initialized more than once")

        self.__stocks = {}
        self.__load()

    def update(self):
        for symbol, stock in self.__stocks.items():
            stock.update()

    def get_stock(self, symbol):
        return self.__stocks.get(symbol, None)

    def __load(self):
        data_path = const.STOCK_DATA_PATH

        for root, dirs, files in os.walk(data_path):
            for f in files:
                symbol = os.path.splitext(f)[0]
                stock_data = get_stock_data("{0}/{1}".format(data_path, f))
                s = Stock(symbol, stock_data)
                self.__stocks[symbol] = s


    