import logging


class Logger:
    def __init__(self, debug=False):
        self._debug = debug
        self._logger = logging.getLogger()

    def log(self, message: str):
        
        self._logger.log(message)

    def message(self, message: str):
        print(message)