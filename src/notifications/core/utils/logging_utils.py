"""Модуль утилит для логгера"""

import json
import logging
import re
import time
from datetime import datetime, timezone


class UTCFormatter(logging.Formatter):  # UTC for logging
    converter = time.gmtime


class MaskingFilter(logging.Filter):
    def filter(self, record):
        record.msg = self.mask_sensitive_data(record.msg)
        return True

    @staticmethod
    def mask_sensitive_data(data: str) -> str:
        data = re.sub(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "***@***.com",
            data,
        )
        data = re.sub(r"(?<=password=)[^&]*", "*****", data)
        return data


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """

    def __init__(
        self,
        fmt_dict: dict = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ):
        self.fmt_dict = (
            fmt_dict if fmt_dict is not None else {"message": "message"}
        )
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        """
        Overwritten to look for the attribute in the format dict values instead of the fmt string.
        """
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        KeyError is raised if an unknown attribute is provided in the fmt_dict.
        """
        return {
            fmt_key: getattr(record, fmt_val, None)
            for fmt_key, fmt_val in self.fmt_dict.items()
        }

    def formatTime(self, record, datefmt=None) -> str:
        """
        Overridden to return the time in UTC with milliseconds.
        """
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        formatted_time = dt.strftime(datefmt or self.default_time_format)
        milliseconds = int(record.msecs)
        return f"{formatted_time}.{milliseconds:03d}z"

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON
        instead of a string.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)
