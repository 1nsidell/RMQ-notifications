from .bulk_email import bulk_email_router
from .notifiacations import notifications_router
from .recipients import recipient_router


__all__ = (
    "bulk_email_router",
    "notifications_router",
    "recipient_router",
)
