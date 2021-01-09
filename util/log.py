
import logging
import logging.handlers
import datetime
import os


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_path = os.path.dirname(os.path.abspath(__file__))
    rf_handler = logging.handlers.TimedRotatingFileHandler(log_path + "../../log/" + "my.log", when="midnight", interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    f_handler = logging.FileHandler(log_path + "../../log/" + "error.log")
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger
