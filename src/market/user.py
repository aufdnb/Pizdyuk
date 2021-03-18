import parent_dir
import pzd_utils as utils
from core import MarketObjectBase 

class User(MarketObjectBase):
    """ Class to represent a user """
    def __init__(self, name, id=None):
        self.__name = name
        self.__id = id

        if not id:
            self.__id = utils.get_unique_id()

        self.__portfolio = 

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id