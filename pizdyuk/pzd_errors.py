from enum import Enum
from pzd_logging import PizdyukLogger

class ErrorSeverity(Enum):
    FATAL = 0
    ERROR = 1
    WARNING = 2

class PizdyukError(Exception):
    def __init__(self, message, severity=ErrorSeverity.ERROR):
        super().__init__(message)
        self.__message = message
        self.__severity = severity

    @property
    def severity(self):
        return self.__severity

    @property
    def message(self):
        return self.__message

class PzdNotImplementedError(PizdyukError):
    def __init__(self, message, severity=ErrorSeverity.ERROR):
        super().__init__(message, severity)

class PzdNotFoundError(PizdyukError):
    def __init__(self, message, severity=ErrorSeverity.ERROR):
        super().__init__(message, severity)
        
class PzdInvalidOperationError(PizdyukError):
    def __init__(self, message, severity=ErrorSeverity.ERROR):
        super().__init__(message, severity)

class PzdLogicError(PizdyukError):
    def __init__(self, message, severity=ErrorSeverity.FATAL):
        super().__init__(message, severity)

class PzdNotLoadedError(PizdyukError):
    def __init__(self, message, severity=ErrorSeverity.FATAL):
        super().__init__(message, severity)

class PizdyukErrorHandler:
    """ Error Handler of Pizdyuk """

    def __init__(self, on_fatal=None, on_error=None, on_warning=None):
        """ 
            PizdyukErrorHandler constructor

            Args:
            on_fatal (Optional: function[PizdyukError]) - callback on fatal error
            on_error (Optional: function[PizdyukError]) - callback on error
            on_warning (Optional: function[PizdyukError]) - callback on warning
        """


        self.add_fatal_handler(on_fatal)
        self.add_error_handler(on_error)
        self.add_fatal_handler(on_warning)

        self.__logger = PizdyukLogger.get_logger()

    def add_fatal_handler(self, on_fatal):
        """ Adds a callback for handling fatal errors """
        self.__on_fatal = on_fatal

    def add_error_handler(self, on_error):
        """ Adds a callback for handling errors """
        self.__on_error = on_error
    
    def add_warning_handler(self, on_warning):
        """ Adds a callback for handling warnings """
        self.__on_warning = on_warning

    def handle(self, pzd_error):
        """
            Function to handler errors of type PizdyukError
            If function is not of type PizdyukError it simply reraises the error
        """

        if not isinstance(pzd_error, PizdyukError):
            raise pzd_error


        switch = {
            ErrorSeverity.FATAL: self.__handle_fatal,
            ErrorSeverity.ERROR: self.__handle_error,
            ErrorSeverity.WARNING: self.__handle_warning
        }

        switch[pzd_error.severity](pzd_error)

    def __handle_fatal(self, error):
        self.__logger.log_fatal(error.message)

        if self.__on_fatal:
            self.__on_fatal(error)

        raise error

    def __handle_error(self, error):
        self.__logger.log_error(error.message)

        if self.__on_error:
            self.__on_error(error)

    def __handle_warning(self, error):
        self.__logger.log_warning(error.message)

        if self.__on_warning:
            self.__on_warning(error)
