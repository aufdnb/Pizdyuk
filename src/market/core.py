class MarketObjectBase:
    def update(self):
        raise NotImplementedError("update function should never be called on MarketObjectBase")

    def get_object_info(self):
        """ Return a dictionary with info about the object """
        raise NotImplementedError("get_object_info should never be valled on MarketObjectBase directly")

class Action:
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        self.__func(*self.__args, **self.__kwargs)