import json
import logging

from redis.asyncio import StrictRedis

from parsley.message import Message
from parsley.ports.consumer import BaseAsyncConsumer
from parsley.settings import settings


class AsyncRedisConsumer(BaseAsyncConsumer):
    """An asynchronous Redis consumer for subscribing to and consuming messages from a specific Redis channel."""

    def __init__(
        self, channel_name: str, logger: logging.Logger = logging.getLogger("")
    ) -> None:
        self.client = StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )
        self.channel = self.client.pubsub()
        self.channel_name = channel_name
        self.logger = logger

    async def initialize(self) -> None:
        """ "Subscribes to the specified Redis channel."""
        await self.channel.subscribe(self.channel_name)

    async def consume(self) -> list[Message] | None:
        """Consumes messages from the subscribed Redis channel.

        The timeout parameter specifies the maximum wait time for a message to prevent unnecessary CPU usage.
        If a message arrives immediately, the wait will end instantly without consuming full timeout duration.
        """
        raw_message = await self.channel.get_message(
            ignore_subscribe_messages=True, timeout=1
        )
        if raw_message:
            return Message(**json.loads(raw_message["data"].decode("utf-8")))

    async def close(self) -> None:
        """Closes the Redis Pub/Sub channel and the Redis client connection."""
        await self.channel.close()
        await self.client.close()
