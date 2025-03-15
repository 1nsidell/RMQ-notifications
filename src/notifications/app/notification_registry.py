class NotificationRegistry:
    # notification_type -> (handler_class, dependency_type)
    handlers = {}

    @classmethod
    def register(cls, notification_type: str, dependency_type: str):
        """
        Decorator for registering a notification handler.
        dependency_type - a string specifying which use case should be injected.
        """

        def decorator(handler_class):
            cls.handlers[notification_type] = (handler_class, dependency_type)
            return handler_class

        return decorator
