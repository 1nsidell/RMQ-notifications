from notifications.application.common.errors.base import ApplicationError


class EmailError(ApplicationError):
    """Base email exceptions."""

    pass


class UnknownEmailNotificationTypeError(EmailError):
    "Incorrect notification type"

    error_type: str = "UNKNOW_EMAIL_NOTIFICATION_TYPE"
