"""
Logger module
"""

from app.settings import IS_BUILD
import logging


class CustomFormatter(logging.Formatter):
    """
    Custom log formatter
    """

    grey = "\033[92m"
    yellow = "\x1b[33;20m"
    red = "\033[41m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = (
    #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    # )
    format_ = "%(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_ + reset,
        logging.INFO: grey + format_ + reset,
        logging.WARNING: yellow + format_ + reset,
        logging.ERROR: red + format_ + reset,
        logging.CRITICAL: bold_red + format_ + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)


log = logging.getLogger("swing")
log.propagate = False
log.setLevel(logging.DEBUG)

# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

handler.setFormatter(CustomFormatter())
log.addHandler(handler)

# copied from: https://stackoverflow.com/a/56944256:
