import logging
from logging.handlers import RotatingFileHandler

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance
    
    def _initialize(self, should_log=False, log_file_path='./logs/jarvis.log'):
        self.logger = logging.getLogger('BETA-1')
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

MAIN_LOGGER = Logger().get_logger()