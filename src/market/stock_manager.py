import os
import parent_dir
import pzd_constants as const
from core import MarketObjectBase
from stock import Stock
from pzd_io import get_stock_data

__manager = None

def get_manager():
    if not __manager:
        __manager = StockManager()
    
    return  __manager

class StockManager(MarketObjectBase):
    """ Class that's manages the stocks """
    def __init__(self):
        if __manager:
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


    