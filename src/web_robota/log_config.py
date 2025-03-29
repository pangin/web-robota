import logging


def setup_logger(name, log_level: logging.DEBUG | logging.INFO | logging.WARNING | logging.ERROR = logging.INFO):
    logger = logging.getLogger(name)

    logger.setLevel(log_level)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()

        console_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger