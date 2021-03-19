from core import MarketObjectBase
from user import User

__manager = None

def get_manager():
    if not __manager:
        __manager = UserManager()
    
    return  __manager

class UserManager(MarketObjectBase):
    def __init__(self):
        if __manager:
            raise RuntimeError("User manager instance already exists. UserManager should not be initialized more than once")

        self.__users = {}
        self.__load()

    def __load(self):
        """ Function to load saved users """
        pass

    def create_user(self, name, id=None, portfolio_members = None):
        user = User(name, id, portfolio_members)
        self.__users[user.id] = user

    def get_user(self, id):
        return self.__users.get(id, None)