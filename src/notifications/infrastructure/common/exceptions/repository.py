from notifications.infrastructure.common.exceptions.base import (
    BaseInfrastructureException,
)


class RepositoryException(BaseInfrastructureException):
    "Exception when working with a repository."

    error_type: str = "REPOSITORY_EXCEPTION"
