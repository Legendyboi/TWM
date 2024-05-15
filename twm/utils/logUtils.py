import logging
import datetime
import os


class CustomFormatter(logging.Formatter):
    gray = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    green = '\x1b[0;32m'
    reset = '\x1b[0m'

    def __init__(self, time_fmt, lvlName_fmt, message_fmt):
        super().__init__()
        self.time_fmt = time_fmt
        self.lvlName = lvlName_fmt
        self.message = message_fmt
        self.FORMATS = {
            logging.DEBUG: self.green + self.time_fmt + self.reset + '|' + self.gray + lvlName + self.reset + '|' + self.gray + message + self.reset,
            logging.INFO: self.green + self.time_fmt + self.reset + '|' + self.blue + lvlName + self.reset + '|' + self.blue + message + self.reset,
            logging.WARNING: self.green + self.time_fmt + self.reset + '|' + self.yellow + lvlName + self.reset + '|' + self.yellow + message + self.reset,
            logging.ERROR: self.green + self.time_fmt + self.reset + '|' + self.red + lvlName + self.reset + '|' + self.red + message + self.reset,
            logging.CRITICAL: self.green + self.time_fmt + self.reset + '|' + self.bold_red + lvlName + self.reset + '|' + self.bold_red + message + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)



# Create custom logger logging all five levels
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Format for logs
time_fmt = '[%(asctime)s]'
lvlName = '%(levelname)8s'
message = '%(message)s'
fmt = time_fmt + '|' + lvlName + '|' + message

# Stdout handler for logging to the console
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(time_fmt, lvlName, message))

# File handler for logging to a file
today = datetime.date.today()

os.chdir('~/.config/TWM')

file_handler = logging.FileHandler('TWM_{}.log'.format(today.strftime('%d_%m_%Y')))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(fmt))

# Adding both handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

