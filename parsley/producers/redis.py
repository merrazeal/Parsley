import logging

import backoff
from redis.asyncio import StrictRedis

from parsley.message import MessageBuilder
from parsley.ports.producer import BaseAsyncProducer
from parsley.settings import settings


class AsyncRedisProducer(BaseAsyncProducer):
    def __init__(self, queue_name, logger: logging.Logger = logging.getLogger("")) -> None:
        self.channel_name = queue_name  # is channel_name, queue for di compabilty
        self.client = StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            username=settings.redis_username,
            password=settings.redis_password,
        )
        self.logger = logger

    async def initialize(self):
        self.logger.info("AsyncRedisProducer initialized successfully")

    @backoff.on_exception(**settings.backoff_config)
    async def produce(self, task_name, *args, **kwargs):
        """Publishes a message to the specified Redis channel."""
        message = MessageBuilder.build(task_name, *args, **kwargs)
        await self.client.publish(self.channel_name, message.model_dump_json())

    @backoff.on_exception(**settings.backoff_config)
    async def close(self) -> None:
        """Closes the Redis client connection."""
        await self.client.aclose()
