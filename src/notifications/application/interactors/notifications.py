import logging

from notifications.application.common.dto import NotificationDTO
from notifications.application.common.errors import (
    UnknownNotificationTypeError,
)
from notifications.application.common.types import NotificationServices


log = logging.getLogger(__name__)


class NotificationsInteractor:
    def __init__(
        self,
        processors: NotificationServices,
    ) -> None:
        self._processors = processors

    async def __call__(self, data: NotificationDTO) -> None:
        try:
            await self._processors[data.type](data.data)
        except KeyError as e:
            log.error("Unknown notification type.", exc_info=True)
            raise UnknownNotificationTypeError from e
