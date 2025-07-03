from .email.email_strategy import EmailStrategyImpl
from .email.fast_email_sender import FastEmailSenderProvider
from .email.storage_email_template import StorageEmailTemplateProvider
from .persistence.entity_manager import EntityManagerImpl
from .persistence.recipient_batches import RecipientBatchesImpl
from .persistence.recipient_reader import RecipientReaderImpl
from .persistence.recipient_repository import RecipientRepository
from .persistence.transaction_manager import SqlaTransactionManager
from .tasks.bulk_mailing import BulkMailingTask


__all__ = (
    "BulkMailingTask",
    "EmailStrategyImpl",
    "EntityManagerImpl",
    "FastEmailSenderProvider",
    "RecipientBatchesImpl",
    "RecipientReaderImpl",
    "RecipientRepository",
    "SqlaTransactionManager",
    "StorageEmailTemplateProvider",
)
