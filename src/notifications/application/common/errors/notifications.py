from notifications.application.common.errors.base import ApplicationError


class IncorrectNotificationDataError(ApplicationError):

    error_type: str = "INCORRECT_NOTIFICATION_DATA"


class UnknownNotificationTypeError(ApplicationError):
    "Incorrect notification type"

    error_type: str = "UNKNOW_NOTIFICATION_TYPE"
