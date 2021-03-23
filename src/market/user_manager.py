from market.core import MarketObjectBase
from market.user import User

MANAGER = None

def get_manager():
    global MANAGER
    if not MANAGER:
        MANAGER = UserManager()
    
    return  MANAGER

class UserManager(MarketObjectBase):
    def __init__(self):
        global MANAGER
        if MANAGER:
            raise RuntimeError("User manager instance already exists. UserManager should not be initialized more than once")

        self.__users = {}
        self.__load()

    def __load(self):
        """ Function to load saved users """
        print("LOADING")
        pass
    
    def update(self):
        for id, user in self.__users.items():
            user.update()

    def handle_create_request(self, **kwargs):
        name = kwargs.pop("name", None)
        id = kwargs.pop("user_id", None)
        balance = kwargs.pop("balance", 0)
        # TODO add parsing for portfolio members
        user_id = self.__create_user(name, id, balance)
        return (200, {"user_id": user_id})

    def __create_user(self, name, id=None, balance=0, portfolio_members = None):
        user = User(name, id, balance, portfolio_members)
        self.__users[user.id] = user
        return user.id

    def get_user(self, id):
        return self.__users.get(id, None)