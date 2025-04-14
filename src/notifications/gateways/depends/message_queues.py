from typing import Dict

from notifications.app.depends import EmailNotificationDispatcher
from notifications.app.tasks.dispatchers import MessageDispatcherProtocol
from notifications.core.settings import Settings, settings
from notifications.gateways.message_queues import NotificationConsumerProtocol
from notifications.gateways.message_queues.impls.rmq_consumer import (
    RMQConsumerImpl,
)


def get_rmq_consumer(
    settings: Settings,
    dispatchers: Dict[str, MessageDispatcherProtocol],
) -> NotificationConsumerProtocol:
    return RMQConsumerImpl(settings, dispatchers)


RMQConsumer: NotificationConsumerProtocol = get_rmq_consumer(
    settings=settings,
    dispatchers={
        settings.rmq.RABBIT_EMAIL_QUEUE: EmailNotificationDispatcher,
    },
)
