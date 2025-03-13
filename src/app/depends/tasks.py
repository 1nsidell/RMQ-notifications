from src.app.tasks.rmq_consumer import RMQConsumer
from src.app.depends import EmailUseCase
from src.app.use_cases import EmailUseCaseProtocol
from src.settings import Settings, settings


def get_rmq_consumer(
    settings: Settings,
    email_use_case: EmailUseCaseProtocol,
) -> RMQConsumer:
    return RMQConsumer(settings, email_use_case)


Consumer: RMQConsumer = get_rmq_consumer(settings, EmailUseCase)
