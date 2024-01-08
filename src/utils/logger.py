import logging
import os
from logging.handlers import RotatingFileHandler
import json

# Load logging settings from the project settings JSON file
with open('config/project_settings.json', 'r') as file:
    project_settings = json.load(file)
    logging_settings = project_settings.get('logging_settings', {})

# Create logs directory if it doesn't exist
if logging_settings.get('log_to_file') and logging_settings.get('log_file_path'):
    os.makedirs(os.path.dirname(logging_settings['log_file_path']), exist_ok=True)

# Configure logging
class Logger:
    def __init__(self):
        self.logger = logging.getLogger(logging_settings.get('project_name'))
        self.logger.setLevel(logging_settings.get('log_level', 'INFO').upper())

        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # File handler
        if logging_settings.get('log_to_file'):
            file_handler = RotatingFileHandler(
                logging_settings.get('log_file_path', 'project.log'),
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(log_format)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# Usage:
# logger = Logger().get_logger()
# logger.info("This is an info message")
# logger.error("This is an error message")
