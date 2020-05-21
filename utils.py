import os
import logging


def config_logger():
    my_logger = logging.getLogger("simple-leaderboard")
    path = os.path.dirname(os.path.realpath(__file__))
    handler = logging.FileHandler(f"{path}/debug.log")
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)10s:%(lineno)s %(message)s"
    )
    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    my_logger.setLevel(logging.DEBUG)
    return my_logger


logger = config_logger()
