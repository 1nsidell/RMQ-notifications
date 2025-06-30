from dishka.integrations.faststream import FromDishka as Depends
from faststream.rabbit import RabbitRouter

from notifications.application.common.dto import (
    ChangeEmailRecipientDTO,
    ChangeUsernameRecipientDTO,
    CreateRecipientDTO,
    DeleteRecipientDTO,
)
from notifications.application.interactors import (
    AddRecipientInteractor,
    ChangeEmailRecipientInteractor,
    ChangeUsernameRecipientInteractor,
    DeleteRecipientInteractor,
)
from notifications.infrastructure.common.external import (
    add_recipient_queue,
    change_email_recipient_queue,
    change_username_recipient_queue,
    delete_recipient_queue,
)
from notifications.presentation.amqp.common.request_models import (
    AddRecipientRequest,
    ChangeEmailRecipientRequest,
    ChangeUsernameRecipientRequest,
    DeleteRecipientRequest,
)


recipient_router = RabbitRouter()


@recipient_router.subscriber(queue=add_recipient_queue)
async def add_recipient(
    data: AddRecipientRequest,
    interactor: Depends[AddRecipientInteractor],
) -> None:
    dto = CreateRecipientDTO(
        oid=data.oid,
        email=data.email,
        username=data.username,
    )
    await interactor(data=dto)


@recipient_router.subscriber(queue=delete_recipient_queue)
async def delete_recipient(
    data: DeleteRecipientRequest,
    interactor: Depends[DeleteRecipientInteractor],
) -> None:
    dto = DeleteRecipientDTO(oid=data.oid)
    await interactor(data=dto)


@recipient_router.subscriber(queue=change_email_recipient_queue)
async def change_email_recipient(
    data: ChangeEmailRecipientRequest,
    interactor: Depends[ChangeEmailRecipientInteractor],
) -> None:
    dto = ChangeEmailRecipientDTO(oid=data.oid, new_email=data.new_email)
    await interactor(data=dto)


@recipient_router.subscriber(queue=change_username_recipient_queue)
async def change_username_recipient(
    data: ChangeUsernameRecipientRequest,
    interactor: Depends[ChangeUsernameRecipientInteractor],
) -> None:
    dto = ChangeUsernameRecipientDTO(
        oid=data.oid, new_username=data.new_username
    )
    await interactor(data=dto)
