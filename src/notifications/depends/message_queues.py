from contextvars import ContextVar

from notifications.app.tasks.dispatchers import MessageDispatcherProtocol
from notifications.core.logging.logging_utils import request_id_var
from notifications.core.settings import RabbitMQConfig, settings
from notifications.depends.tasks import EmailNotificationDispatcher
from notifications.gateways.message_queues import (
    NotificationConsumerProtocol,
    RMQConsumerImpl,
)


def get_rmq_consumer(
    config: RabbitMQConfig,
    dispatchers: dict[str, MessageDispatcherProtocol],
    request_context_manager: ContextVar[str],
) -> NotificationConsumerProtocol:
    return RMQConsumerImpl(
        config=config,
        dispatchers=dispatchers,
        request_context_manager=request_context_manager,
    )


RMQConsumer: NotificationConsumerProtocol = get_rmq_consumer(
    config=settings.rmq,
    dispatchers={
        settings.rmq.RABBIT_EMAIL_QUEUE: EmailNotificationDispatcher,
    },
    request_context_manager=request_id_var,
)
