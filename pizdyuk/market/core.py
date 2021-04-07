from pzd_errors import PzdNotImplementedError, ErrorSeverity

class MarketObjectBase:
    def update(self):
        raise PzdNotImplementedError("update function should never be called on MarketObjectBase", ErrorSeverity.FATAL)

    def get_object_info(self):
        """ Return a dictionary with info about the object """
        raise PzdNotImplementedError("get_object_info should never be valled on MarketObjectBase directly", ErrorSeverity.FATAL)

class Action:
    def __init__(self, func, *args, **kwargs):
        """
            Action constructor

            Args: 
            func - function to represent the action
        """
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def execute(self):
        """
            Executes the underlying function with provided args and keywords
        """
        self.__func(*self.__args, **self.__kwargs)