from taskiq_aio_pika import AioPikaBroker

from src.settings import settings

broker = AioPikaBroker(settings.rmq.url)
