import logging
import os
from pathlib import Path


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    if log_filename := os.environ.get("PREPROCESSING_LOG_FILE_PATH"):
        os.makedirs(Path(log_filename).parent, exist_ok=True)
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
    else:
        logging.warning("A log file doesn't define")
    return logger
