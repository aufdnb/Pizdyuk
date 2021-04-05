from threading import Thread
from pzd_events import Event, TypedEvent

class Pizdyuk_Thread(Thread):
    """ Thread class """

    """
        (Event): event which is triggered on thread start
    """
    on_started = Event()

    """
        (Event): event which is triggered on thread finish
    """
    on_finished = Event()

    """
        (TypedEvent[object]): event which is triggered if
        an error was raised during run() execution.
        The error raised is the argument of the event.
    """
    on_error = TypedEvent(object)

    """
        (TypedEvent[object]): event which is triggered if the run()
        successfully terminated.
        The returned result of the func() is the argument of the event.
    """
    on_success = TypedEvent(object)

    def __init__(self, func, *args, **kwargs):
        """
            Pizdyuk thread constructor
            
            Args:
            func - function to execute
            *args - function args
            **kwargs - function kwargs
        """
        super().__init__(target=func)
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def run(self):
        """
            Runnable function of Thread.
        """
        self.on_started.invoke()

        try:
            result = self.__func(*self.__args, **self.__kwargs)

            if not result:
                result = "success"
                
            self.on_success.invoke(result)
        except Exception as e:
            self.on_error.invoke(e)
        finally:
            self.on_finished.invoke()



    