from notifications.infrastructure.common.exceptions.base import (
    InfrastructureException,
)


class RepositoryException(InfrastructureException):
    "Exception when working with a repository."

    error_type: str = "REPOSITORY_EXCEPTION"
