from notifications.core import BaseDomainErros


class RMQError(BaseDomainErros):
    """Base rmq errors."""

    pass


class RMQMessageError(RMQError):
    """RabbitMQ message error."""

    error_type: str = "RMQ_ERROR"
    status_code: int = 400
