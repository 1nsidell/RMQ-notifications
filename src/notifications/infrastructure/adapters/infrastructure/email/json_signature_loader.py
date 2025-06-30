import json
import logging
from pathlib import Path

from notifications.application.common.dto import (
    EmailSignature,
)
from notifications.application.common.errors import (
    UnknownNotificationTypeError,
)
from notifications.infrastructure.common.ports.email.signature_loader import (
    SignatureLoader,
)


logger = logging.getLogger(__name__)


class JsonSignatureLoader(SignatureLoader):
    def __init__(self, path: Path) -> None:
        self._file_path = path
        self._signatures: dict[str, EmailSignature] = {}
        self._raw_signatures: dict[str, dict[str, str]] = {}
        self._is_json_loaded = False
        logger.info(
            "SignatureLoader initialized with path: %s.", self._file_path
        )

    def _ensure_json_loaded(self) -> None:
        if not self._is_json_loaded:
            try:
                with open(self._file_path, encoding="utf-8") as f:
                    self._raw_signatures = json.load(f)
                self._is_json_loaded = True
                logger.debug(
                    "JSON file loaded successfully: %s.", self._file_path
                )
            except FileNotFoundError:
                logger.error(
                    "Email signatures file not found: %s.", self._file_path
                )
                raise RuntimeError(
                    f"Email signatures file not found: '{self._file_path}'."
                )
            except json.JSONDecodeError:
                logger.error(
                    "Invalid JSON in email signatures file: '%s'.",
                    self._file_path,
                )
                raise RuntimeError(
                    f"Invalid JSON in email signatures file: '{self._file_path}'."
                )

    def _load_signature(self, email_type: str) -> EmailSignature:
        try:
            data = self._raw_signatures[email_type]
            signature = EmailSignature(
                subject=data["subject"], template=data["template"]
            )
            logger.debug("Signature loaded for email type: %s.", email_type)
            return signature
        except KeyError as e:
            if email_type not in self._raw_signatures:
                logger.error(
                    "Email notification type not found: %s.", email_type
                )
                raise UnknownNotificationTypeError(
                    f"Email notification type '{email_type}' not found.",
                )
            logger.error(
                "Missing required field in signature '%s': %s.", email_type, e
            )
            raise RuntimeError(
                f"Missing required field in signature '{email_type}'.",
            ) from e

    def get_signature(self, email_type: str) -> EmailSignature:
        if email_type not in self._signatures:
            logger.debug("Loading signature for email type: %s.", email_type)
            self._ensure_json_loaded()
            self._signatures[email_type] = self._load_signature(email_type)
        return self._signatures[email_type]

    @property
    def signatures(self) -> dict[str, EmailSignature]:
        self._ensure_json_loaded()
        for signature in self._raw_signatures.keys():
            if signature not in self._signatures:
                logger.debug("Loading signature: %s", signature)
                self._signatures[signature] = self._load_signature(signature)
        return self._signatures.copy()
