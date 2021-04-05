import inspect

class EventBase:
    def __init__(self):
        self._handlers = []

    def add_handler(self, event_handler):
        """ Adds an event handler """
        self._validate_handler(event_handler)
        self._handlers.append(event_handler)

    def clear_handlers(self):
        """ Removes all attached handlers """
        self._handlers.clear()

    def _validate_handler(self, event_handler):
        if not callable(event_handler):
            raise ValueError("Event handler is not a callable")

class TypedEvent(EventBase):
    """ Event class """

    def __init__(self, event_type):
        """ 
            Event class constructor

            Args:
            event_type (Type): type corresponding to the argument of the handler parameter

            Currently only supports one parameter
        """
        super().__init__()

        if type(event_type) is not type:
            raise ValueError("event_type must be of type type")

        self.__event_type = event_type

    def invoke(self, argument):
        """
            Invokes all handlers

            Args:
            argument (event_type): argument to invoke handlers with
        """
        if not isinstance(argument, self.__event_type):
            raise TypeError("Expected {0}: invoked with {1}".format(self.__event_type, type(argument)))

        for handler in self._handlers:
            handler(argument)

class Event(EventBase):
    def __init__(self):
        super().__init__()

    def invoke(self):
        for handler in self._handlers:
            handler()
