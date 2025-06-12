from dishka.integrations.faststream import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from notifications.application.common.dto import EmailNotificationDTO
from notifications.application.interactors import (
    EmailNotificationInteractor,
)
from notifications.infrastructure.common.resources import (
    bulk_mailing_queue,
)
from notifications.presentation.amqp.common.request_models import (
    EmailNotificationRequest,
)


bulk_mailing_router = RabbitRouter()


@bulk_mailing_router.subscriber(queue=bulk_mailing_queue)
async def bulk_mailing_handler(
    request:,
    interactor:,
) -> None:

    await interactor.bulk_mailing(dto)
