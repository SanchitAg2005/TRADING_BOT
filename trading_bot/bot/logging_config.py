import os
import logging
from logging.handlers import RotatingFileHandler
from .config import config

def setup_logging() -> logging.Logger:
    """
    Configures and returns a rotating file logger for the trading bot.
    Logs are written to the logs/trading.log file.
    """
    # Ensure logs directory exists
    log_dir = os.path.dirname(config.LOG_FILE_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("trading_bot")
    
    # Prevent adding handlers multiple times if imported multiple times
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))

    # Create rotating file handler (10MB max size, keep 5 backups)
    file_handler = RotatingFileHandler(
        config.LOG_FILE_PATH, maxBytes=10*1024*1024, backupCount=5
    )
    
    # Create formatter and add it to the handler
    # Include timestamp, log level, module, and message
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(file_handler)
    
    # Note: We do NOT add a StreamHandler here because Typer/Rich
    # handles the CLI output. Mixing standard logging to stdout 
    # with Rich can lead to messy terminal outputs.

    return logger

logger = setup_logging()
