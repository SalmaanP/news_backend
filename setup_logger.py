import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)-s %(levelname)s [%(name)s]: %(message)s')
    handler = RotatingFileHandler('logs/log.log', maxBytes=10000000,
                                    backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
