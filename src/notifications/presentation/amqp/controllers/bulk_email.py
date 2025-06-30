from dishka.integrations.faststream import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from notifications.application.common.dto import BulkEmailDTO
from notifications.infrastructure.common.external import (
    bulk_mailing_queue,
)
from notifications.infrastructure.common.ports import BulkMailingTask
from notifications.presentation.amqp.common.request_models import (
    BulkMailingRequest,
)


bulk_email_router = RabbitRouter()


@bulk_email_router.subscriber(queue=bulk_mailing_queue)
async def bulk_mailing_handler(
    data: BulkMailingRequest,
    task: Depends[BulkMailingTask],
) -> None:
    dto = BulkEmailDTO(type=data.type)
    await task(data=dto)
