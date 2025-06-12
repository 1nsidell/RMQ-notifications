from notifications.application.common.errors.base import ApplicationError


class EmailError(ApplicationError):
    """Base email exceptions."""

    pass


class UnknownNotificationTypeError(EmailError):
    "Incorrect notification type"

    error_type: str = "UNKNOW_NOTIFICATION_TYPE"
