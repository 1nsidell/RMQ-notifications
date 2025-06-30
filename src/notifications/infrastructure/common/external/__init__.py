from .rmq import (
    add_recipient_queue,
    bulk_mailing_queue,
    change_email_recipient_queue,
    change_username_recipient_queue,
    delete_recipient_queue,
    email_notification_queue,
    new_faststream_broker,
    taskiq_broker,
)


__all__ = (
    "add_recipient_queue",
    "bulk_mailing_queue",
    "change_email_recipient_queue",
    "change_username_recipient_queue",
    "delete_recipient_queue",
    "email_notification_queue",
    "new_faststream_broker",
    "taskiq_broker",
)
