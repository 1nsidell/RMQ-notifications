from dishka.integrations.faststream import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from notifications.application.common.dto import BulkEmailDTO
from notifications.application.interactors.bulk_email import (
    BulkEmailInteractor,
)
from notifications.infrastructure.common.external import (
    bulk_mailing_queue,
)
from notifications.presentation.amqp.common.request_models import (
    BulkMailingRequest,
)


bulk_email_router = RabbitRouter()


@bulk_email_router.subscriber(queue=bulk_mailing_queue)
async def bulk_mailing_handler(
    data: BulkMailingRequest,
    task: Depends[BulkEmailInteractor],
) -> None:
    dto = BulkEmailDTO(type=data.type)
    await task(data=dto)
