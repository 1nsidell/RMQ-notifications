# FastAPI Notifications Microservice

A robust microservice for sending email notifications (confirmation, password recovery, etc.) via RabbitMQ, built with FastAPI, aio-pika, and fastapi-mail.

---

## Features

- **Asynchronous Email Delivery**: Uses FastAPI and fastapi-mail for efficient, non-blocking email sending.
- **RabbitMQ Integration**: Consumes notification tasks from RabbitMQ queues.
- **Template-based Emails**: Jinja2 HTML templates for customizable email content.
- **Extensible Handlers**: Easily add new notification types and handlers.
- **Graceful Shutdown**: Handles signals for safe shutdown and message processing.
- **Sensitive Data Masking**: Logging utilities to mask sensitive info in logs.
- **Configurable via Environment**: All settings via `.env` or environment variables.

---

## Architecture Overview

```
[Main App] --(Publishes JSON to RMQ Queue)--> [FastAPI Notifications Service]
                                                 |
                                                 v
                                    [RMQ Consumer (aio-pika)]
                                                 |
                                                 v
                                 [Dispatcher] --> [Handler] --> [Email Service]
                                                 |
                                                 v
                                         [FastMail/Jinja2]
```

- **RMQConsumerImpl**: Connects to RabbitMQ, consumes messages, and dispatches them.
- **Dispatchers**: Route messages to the appropriate handler based on type.
- **Handlers**: Implement logic for each notification type (e.g., confirm email, recovery).
- **Email Services**: Compose and send emails using templates and FastMail.

---

## Quickstart

### 1. Clone and Install

```bash
git clone https://github.com/your-org/fastapi-notifications.git
cd fastapi-notifications
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
# Edit .env with your mail and RabbitMQ settings
```

### 3. Run RabbitMQ

Make sure RabbitMQ is running and accessible with the credentials in `.env`.

### 4. Start the Service

```bash
python -m notifications.main
```

Or with Docker:

```bash
docker-compose up --build
```

---

## Usage

- **Send a notification**: Publish a JSON message to the configured RabbitMQ queue (see `RABBIT_EMAIL_QUEUE` in `.env`).
- **Message format**:
    ```json
    {
      "type": "confirm_email",
      "recipient": "user@example.com",
      "token": "sometoken"
    }
    ```
    Supported types: `confirm_email`, `recovery_password`.

---

## Project Structure

- `src/notifications/app/` - Application logic, handlers, services, exceptions.
- `src/notifications/core/` - Settings, logging, templates, base exceptions.
- `src/notifications/gateways/` - Message queue consumers and protocols.
- `tests/` - Unit tests and fixtures.

---

## Extending

To add a new notification type:

1. **Create a Handler** in `src/notifications/app/notification_handlers/emails/`.
2. **Register it** with the registry using the `@EmailNotificationRegistry.register("your_type", implementation="email")` decorator.
3. **Update templates** if needed.

---

## Testing

Run all tests:

```bash
pytest
```

---

## Typing

- This project strictly adheres to static typing using [mypy](https://mypy-lang.org/).
- Type annotations are enforced throughout the codebase.

---

## Linting

- Code is linted using [ruff](https://docs.astral.sh/ruff/).
- All code should pass ruff checks before merging.

---

## Formatting

- Code is formatted using [black](https://black.readthedocs.io/).
- All code should be auto-formatted with black before merging.

---

## Logging

- Logs are output to both console and `logs/app.log` (JSON format).
- Sensitive data is masked automatically.

---

## Contributing

1. Fork the repo and create your branch.
2. Write tests for your feature or bugfix.
3. Run `ruff` for linting.
4. Run `black` for formatting.
5. Run `mypy` for type checking.
6. Submit a pull request.

---

## License

MIT License

---

## Authors

- Daniel (2025)
