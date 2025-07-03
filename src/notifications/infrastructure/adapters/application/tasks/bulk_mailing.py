from typing import Annotated

from dishka import FromComponent
from dishka.integrations.taskiq import FromDishka as Depends, inject

from notifications.application.common.dto import BulkEmailDTO
from notifications.application.interactors import BulkEmailInteractor
from notifications.infrastructure.common.external import taskiq_broker


class BulkMailingTask:
    async def __call__(self, data: BulkEmailDTO) -> None:
        await bulk_mailing.kiq(data=data)


@taskiq_broker.task
@inject(patch_module=True)
async def bulk_mailing(
    data: BulkEmailDTO,
    interactor: Depends[
        Annotated[BulkEmailInteractor, FromComponent("taskiq")]
    ],
) -> None:
    await interactor(data=data)
