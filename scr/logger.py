import logging
import os

class Logger:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file='app.log'):
        if self._initialized:
            return

        self.log_file = log_file
        self.logger = logging.getLogger('StudentManagementSystem')
        self.logger.setLevel(logging.INFO)
        self._setup_logger()

    def _setup_logger(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as file:
                pass  # Create the log file if it doesn't exist

        if not self.logger.hasHandlers():
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8', delay=False)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            console_formatter = logging.Formatter('%(message)s')

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            self.logger.propagate = False
        return self.logger
    
    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)
        self._flush_handlers()

    def _flush_handlers(self):
        for handler in self.logger.handlers:
            handler.flush()

    

