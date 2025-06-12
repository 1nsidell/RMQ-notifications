from sqlalchemy import BigInteger, Column, String, Table
from sqlalchemy.orm import composite

from notifications.domain.entities.recipient.entity import (
    Recipient,
)
from notifications.domain.entities.recipient.value_objects import (
    RecipientEmail,
    RecipientUsername,
)
from notifications.infrastructure.persistence.models import mapper_registry


recipients_table = Table(
    "recipients",
    mapper_registry.metadata,
    Column("recipient_id", BigInteger, primary_key=True),
    Column("recipient_email", String, nullable=False, index=True, unique=True),
    Column("recipient_username", String, nullable=False, unique=True),
)


def map_recipients_table() -> None:
    mapper_registry.map_imperatively(
        Recipient,
        recipients_table,
        properties={
            "oid": recipients_table.c.recipient_id,
            "email": composite(
                RecipientEmail, recipients_table.c.recipient_email
            ),
            "username": composite(
                RecipientUsername, recipients_table.c.recipient_username
            ),
        },
    )
