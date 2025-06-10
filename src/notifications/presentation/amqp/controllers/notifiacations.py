from dishka.integrations.faststream import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from notifications.application.common.dto import EmailNotificationDTO
from notifications.application.interactors import (
    EmailNotificationInteractor,
)
from notifications.infrastructure.common.resources.rmq import (
    email_notification_queue,
)
from notifications.presentation.amqp.common.request_models import (
    EmailNotificationRequest,
)


notifications_router = RabbitRouter()


@notifications_router.subscriber(queue=email_notification_queue)
async def email_notifications(
    data: EmailNotificationRequest,
    interactor: Depends[EmailNotificationInteractor],
) -> None:
    dto = EmailNotificationDTO(
        type=data.type,
        recipient=data.recipient,
        data=data.data,
    )
    await interactor(dto)
