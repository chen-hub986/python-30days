import logging
import os

class Logger:
    _instance = None

    def __init__(self, log_file='app.log'):
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
            file_handler.setFormatter(formatter)
            self.logger.propagate = False
            self.logger.addHandler(file_handler)
        return self.logger
    
    def log_info(self, message):
        self.logger.info(message)
        self._flush_handlers()

    def log_error(self, message):
        self.logger.error(message)
        self._flush_handlers()

    def _flush_handlers(self):
        for handler in self.logger.handlers:
            handler.flush()

    

