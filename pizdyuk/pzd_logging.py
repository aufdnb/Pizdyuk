import datetime as date
from pzd_utils import datetime_to_str

class PizdyukLogger:
    __logger = None
    
    def __init__(self):
        global __logger

        if self.__logger:
            raise RuntimeError("Logger instance already exists")

    @staticmethod
    def get_logger():
        global __logger
        if not PizdyukLogger._PizdyukLogger__logger:
            PizdyukLogger._PizdyukLogger__logger = PizdyukLogger()

        return PizdyukLogger._PizdyukLogger__logger

    def log_info(self, msg):
        self.__log(msg, "INFO")

    def log_warning(self, warning):
        self.__log(warning, "WARNING")

    def log_error(self, error):
        self.__log(error, "ERROR")

    def log_fatal(self, fatal):
        self.__log(fatal, "FATAL")

    def __log(self, msg, lvl):
        date_str = datetime_to_str(date.datetime.now())
        log = "[{0}] [{1}] {2}".format(lvl, date_str, msg)
        print(log)
        