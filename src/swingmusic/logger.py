"""
Logger module
"""
import pathlib

from swingmusic.config import Paths
import logging
import datetime as dt
import json
import logging.config
import logging.handlers


LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class JsonFormat(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] | None = None,):

        super().__init__()
        self.fmt_keys = fmt_keys or {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "args": record.args,
            "name": record.name,
            "line": record.lineno,
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(record.created, tz=dt.timezone.utc).isoformat(),
            "who": record.name
        }

        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {}

        for key, val in self.fmt_keys.items():
            if (msg_val := always_fields.pop(val, None)) is not None:
                message[key] = msg_val
            else:
                message[key] = getattr(record, val)

        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message


class CustomFormatter(logging.Formatter):
    """
    Custom log formatter
    """

    grey = "\033[92m"
    yellow = "\x1b[33;20m"
    red = "\033[41m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format_ = "[%(asctime)s] %(name)s %(levelname)s %(message)s (%(filename)s:%(lineno)d)"
    format_ = "[%(asctime)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"
    # format_ = "%(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_ + reset,
        logging.INFO: grey + format_ + reset,
        logging.WARNING: yellow + format_ + reset,
        logging.ERROR: red + format_ + reset,
        logging.CRITICAL: bold_red + format_ + reset,
    }

    def __init__(self, *, fmt_keys: dict[str, str] | None = None,):

        super().__init__()
        self.fmt_keys = fmt_keys or {}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)


CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "()": JsonFormat,
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "logger": "name",
                "module": "module",
                "function": "funcName",
                "line": "lineno"
            }
        },
        "custom": {
            "()": CustomFormatter,
            "fmt_keys": {
                "level": "levelname",
                "message": "message",
                "timestamp": "timestamp",
                "logger": "name",
                "module": "module",
                "function": "funcName",
                "line": "lineno"
            }
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "custom",
            "stream": "ext://sys.stderr"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "maxBytes": 5*1024*1024, # 5 MB
            "backupCount": 5
        },
        "remote": {
            "class": "logging.handlers.SocketHandler",
            "level": "DEBUG",
            "formatter": "json",
            "host": "127.0.0.2",
            "port": "19996"
        }
    },
    "loggers": {
        "swingmusic": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": [
                "stdout",
                "file"
            ]
        },
        "waitress": {
            "level": "ERROR",
            "propagate": False,
            "handlers": [
                "stdout",
                "file"
            ]
        }
    }
}

log = None

def setup_logger(debug=False):
    """
    setup logger
    needs to be called at the beginning and at least once

    :param debug: When True Loglevel is set to DEBUG and enable Socket log
    """

    app_dir = Paths().app_dir

    CONFIG["handlers"]["file"]["filename"] = app_dir / "log.jsonl"
    # BIG TODO: make log delete or rotate big log files

    # enable socket log
    if debug:
        logging.warning("YOU ARE IN DEBUG MODE.")
        for key in CONFIG["loggers"].keys():
            CONFIG["loggers"][key]["handlers"].append("remote")
            CONFIG["loggers"][key]["level"] = "DEBUG"

    logging.config.dictConfig(CONFIG)

    global log
    log = logging.getLogger(__name__)
    log.info("setup successfully")
