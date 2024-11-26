import logging

from redis.asyncio import StrictRedis

from parsley.message import MessageBuilder
from parsley.ports.producer import BaseAsyncProducer
from parsley.settings import settings


class AsyncRedisProducer(BaseAsyncProducer):
    def __init__(
        self, channel_name, logger: logging.Logger = logging.getLogger("")
    ) -> None:
        self.channel_name = channel_name
        self.client = StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )
        self.logger = logger

    async def initialize(self): ...

    async def produce(self, task_name, *args, **kwargs):
        """Publishes a message to the specified Redis channel."""
        message = MessageBuilder.build(task_name, *args, **kwargs)
        await self.client.publish(self.channel_name, message.model_dump_json())

    async def close(self) -> None:
        """Closes the Redis client connection."""
        await self.client.close()
