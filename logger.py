import logging
from logging.handlers import RotatingFileHandler

class LoggerSetup:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerSetup, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance


    def __init__(self, should_log=False, log_file_path='./logs/jarvis.log'):
        if self._initialized:
            return

        self.logger = logging.getLogger('JARVIS')
        self.logger.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s [%(name)s lvl-%(levelname)s] at [%(module)s]:  %(message)s')

        # File Handler
        if should_log:
            file_handler = RotatingFileHandler(log_file_path, maxBytes=10485760, backupCount=5)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


    def get_logger(self):
        return self.logger
