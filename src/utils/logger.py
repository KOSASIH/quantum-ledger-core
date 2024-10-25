import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name='app_logger', log_file='app.log', max_bytes=5 * 1024 * 1024, backup_count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler with rotation
        if not os.path.exists('logs'):
            os.makedirs('logs')
        handler = RotatingFileHandler(os.path.join('logs', log_file), maxBytes=max_bytes, backupCount=backup_count)
        handler.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Example usage
if __name__ == "__main__":
    log = Logger()
    log.info("This is an info message.")
    log.error("This is an error message.")
