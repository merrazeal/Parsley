import json
import logging

import backoff
from redis.asyncio import StrictRedis

from parsley.message import Message
from parsley.ports.consumer import BaseAsyncConsumer
from parsley.settings import settings


class AsyncRedisConsumer(BaseAsyncConsumer):
    def __init__(
        self, queue_name: str, logger: logging.Logger = logging.getLogger("")
    ) -> None:
        self.client = StrictRedis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            username=settings.redis_username,
        )
        self.channel = self.client.pubsub()
        self.channel_name = queue_name  # is channel_name, queue for di compabilty
        self.logger = logger

    @backoff.on_exception(**settings.backoff_config)
    async def initialize(self) -> None:
        """ "Subscribes to the specified Redis channel."""
        await self.channel.subscribe(self.channel_name)
        self.logger.info("AsyncRedisConsumer initialized successfully")

    @backoff.on_exception(**settings.backoff_config)
    async def consume(self) -> Message | None:
        """Consumes messages from the subscribed Redis channel.

        The timeout parameter specifies the maximum wait time for a message to prevent unnecessary CPU usage.
        If a message arrives immediately, the wait will end instantly without consuming full timeout duration.
        """
        raw_message = await self.channel.get_message(
            ignore_subscribe_messages=True, timeout=settings.redis_max_wait_poll_time
        )
        if raw_message:
            return Message(**json.loads(raw_message["data"].decode("utf-8")))
    
    @backoff.on_exception(**settings.backoff_config)
    async def close(self) -> None:
        """Closes the Redis Pub/Sub channel and the Redis client connection."""
        if self.channel:
            await self.channel.aclose()
        if self.client:
            await self.client.aclose()
