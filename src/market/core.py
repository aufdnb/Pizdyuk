class MarketObjectBase:
    def update(self):
        raise NotImplementedError("Update function should never be called on MarketObjectBase")

class Action:
    def __init__(self, func, *args, **kwargs):
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        self.__func(*self.__args, **self.__kwargs)