import logging
import sys

from pythonjsonlogger import jsonlogger

def configure_logging(debug: bool):
    handler = logging.StreamHandler(sys.stdout)


    if debug:
        formatter = logging.Formatter(
             "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    else:
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )

    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)