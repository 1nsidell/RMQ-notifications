from logging import Logger

from faststream.rabbit import RabbitBroker, RabbitQueue
from faststream.security import SASLPlaintext
from taskiq_aio_pika import AioPikaBroker

from notifications.infrastructure.common.config.constants import RabbitQueues
from notifications.infrastructure.common.config.settings import (
    RabbitMQConfig,
    get_settings,
)


config = get_settings()
taskiq_broker = AioPikaBroker(config.rmq.url)


def new_faststream_broker(
    rmq_config: RabbitMQConfig,
    logger: Logger | None = None,
) -> RabbitBroker:
    return RabbitBroker(
        host=rmq_config.HOST,
        port=rmq_config.PORT,
        security=SASLPlaintext(
            username=rmq_config.USERNAME,
            password=rmq_config.PASSWORD,
        ),
        virtualhost=rmq_config.VHOST,
        timeout=rmq_config.TIMEOUT,
        logger=logger,
    )


add_recipient_queue = RabbitQueue(
    name=RabbitQueues.ADD_RECIPIENT,
    durable=True,
)

delete_recipient_queue = RabbitQueue(
    name=RabbitQueues.DELETE_RECIPIENT,
    durable=True,
)

change_email_recipient_queue = RabbitQueue(
    name=RabbitQueues.CHANGE_EMAIL_RECIPIENT,
    durable=True,
)

change_username_recipient_queue = RabbitQueue(
    name=RabbitQueues.CHANGE_USERNAME_RECIPIENT,
    durable=True,
)

email_notification_queue = RabbitQueue(
    name=RabbitQueues.EMAIL_NOTIFICATION,
    durable=True,
)

bulk_mailing_queue = RabbitQueue(
    name=RabbitQueues.BULK_MAILING,
    durable=True,
)
