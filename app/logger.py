import logging
import datetime
import os

from flask.cli import load_dotenv

from app.config import WORKING_DIR

current_date = datetime.datetime.now().strftime('%Y%m%d')
log_dir = os.path.join(WORKING_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"{current_date}_imou.log")

# Configure logging to write to a file
logging.basicConfig(
    filename=log_file,  # Log file name
    level=logging.INFO,  # Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

def _log(message, level='info'):
    """
    Log a message with the specified level.
    
    :param message: The message to log
    :param level: The log level ('debug', 'info', 'warning', 'error', 'critical')
    """
    if level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message)
    else:
        logging.info(message)  # Default to INFO if an invalid level is provided

def warning(message):
    _log(message, level='warning')

def error(message):
    _log(message, level='error')

def info(message):
    _log(message, level='info')

def critical(message):
    _log(message, level='critical')