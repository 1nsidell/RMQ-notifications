from dishka.integrations.faststream import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from notifications.application.common.dto import NotificationDTO
from notifications.application.interactors import NotificationsInteractor
from notifications.infrastructure.common.external import (
    email_notification_queue,
)
from notifications.presentation.amqp.common.request_models import (
    NotificationRequest,
)


notifications_router = RabbitRouter()


@notifications_router.subscriber(queue=email_notification_queue)
async def email_notifications(
    data: NotificationRequest,
    interactor: Depends[NotificationsInteractor],
) -> None:
    dto = NotificationDTO(
        type=data.type,
        data=data.data,
    )
    await interactor(dto)
