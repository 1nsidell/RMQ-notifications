class NotificationRegistry:
    handlers = {}  # notification type -> handler class

    @classmethod
    def register(cls, notification_type: str):
        """Decorator for handler registration."""

        def decorator(handler_class):
            cls.handlers[notification_type] = handler_class
            return handler_class

        return decorator
