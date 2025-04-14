"""A utils module for logger."""

from datetime import datetime, timezone
from functools import lru_cache
import json
import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple, Union


class UTCFormatter(logging.Formatter):  # UTC for logging
    converter = time.gmtime


class MaskingFilter(logging.Filter):
    """Filter for masking sensitive data in logs."""

    def __init__(self, patterns: Optional[Dict[str, Tuple[str, str]]] = None):
        super().__init__()
        default_patterns = {
            "email": (
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                "***@***.com",
            ),
            "password": (
                r'(?i)(["\']?(password|passwd|pwd|secret_key|api_key|token)["\']?\s*[:=]\s*["\']?)([^"\'\s,}]+)',
                r"\1*****",
            ),
        }
        self._compiled_patterns = {
            name: (re.compile(pattern), replacement)
            for name, (pattern, replacement) in (
                patterns or default_patterns
            ).items()
        }

        self._sensitive_keywords = re.compile(
            r"(password|passwd|pwd|secret|api_?key|token)", flags=re.IGNORECASE
        )

    def filter(self, record: logging.LogRecord) -> bool:
        """Apply masking to log record."""
        msg_str = str(record.msg)
        if not self._has_sensitive_data(msg_str):
            return True

        record.msg = self._mask_message(msg_str)

        if record.args:
            record.args = tuple(
                (self._mask_message(str(arg)) if isinstance(arg, str) else arg)
                for arg in record.args
            )
        return True

    def _has_sensitive_data(self, data: str) -> bool:
        """Check if data might contain sensitive information."""
        return bool(self._sensitive_keywords.search(data)) or ("@" in data)

    def _mask_message(self, data: str) -> str:
        """Mask sensitive data in message."""
        for pattern, replacement in self._compiled_patterns.values():
            data = pattern.sub(replacement, data)

        if "{" in data and ('"' in data or "'" in data):
            parsed = json.loads(data)
            if isinstance(parsed, (dict, list)):
                return json.dumps(self._recursive_mask(parsed))
        return data

    @lru_cache(maxsize=1024)
    def _is_sensitive_key(self, key: str) -> bool:
        """Check if key contains sensitive data."""
        if not isinstance(key, str):
            return False
        return bool(self._sensitive_keywords.search(key))

    def _recursive_mask(self, data: Union[Dict, List, Any]) -> Any:
        """Recursively mask sensitive data in structures."""
        if isinstance(data, dict):
            return {
                k: (
                    "*****"
                    if self._is_sensitive_key(k)
                    else self._recursive_mask(v)
                )
                for k, v in data.items()
            }
        if isinstance(data, list):
            return [self._recursive_mask(i) for i in data]
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
        fmt_dict: Optional[dict] = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ):
        self.fmt_dict = fmt_dict or {"message": "message"}
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
        return f"{formatted_time}.{milliseconds:03d}Z"

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
