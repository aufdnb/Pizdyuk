from threading import Thread
from pzd_events import Event, TypedEvent

class Pizdyuk_Thread(Thread):
    """ Thread class """
    on_started = Event()
    on_finished = Event()
    on_error = TypedEvent(object)
    on_success = TypedEvent(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__(target=func)
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    def run(self):
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



    