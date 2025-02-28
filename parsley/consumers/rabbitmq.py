import asyncio
import json
import logging

from aio_pika import Message as AioPikaMessage
from aio_pika import connect
from aio_pika import exceptions as aio_pika_exceptions
import backoff

from parsley.message import Message
from parsley.ports.consumer import BaseAsyncConsumer
from parsley.settings import settings


class AsyncRabbitMQConsumer(BaseAsyncConsumer):
    def __init__(
        self, queue_name: str, logger: logging.Logger = logging.getLogger("")
    ) -> None:
        self.queue_name = queue_name
        self.routing_key = queue_name  # for direct exchange
        self.logger = logger

    @backoff.on_exception(**settings.backoff_config)
    async def initialize(self) -> None:
        """
        Establishes a connection to RabbitMQ, declares the exchange and queue,
        and binds the queue to the specified routing key.
        """
        self.connection = await connect(
            settings.rabbitmq_url, loop=asyncio.get_running_loop()
        )
        channel = await self.connection.channel()
        self.exchange = await channel.declare_exchange("direct")
        self.queue = await channel.declare_queue(self.queue_name)
        await self.queue.bind(self.exchange, self.routing_key)
        self.logger.info("AsyncRabbitMQConsumer initialized successfully")

    @backoff.on_exception(**settings.backoff_config)
    async def consume(self):
        """
        Consumes messages from the bound RabbitMQ queue.

        The `timeout` parameter specifies the maximum wait time for a message to prevent unnecessary CPU usage.
        If a message arrives immediately, the wait will end instantly without consuming the full timeout duration.
        """
        try:
            raw_message: AioPikaMessage = await self.queue.get(
                timeout=settings.rabbitmq_max_wait_poll_time
            )
        except aio_pika_exceptions.QueueEmpty:
            self.logger.debug("queue is empty... sleeping...")
            await asyncio.sleep(settings.rabbitmq_empty_queue_delay)
        else:
            message = Message(**json.loads(raw_message.body.decode("utf-8")))
            await raw_message.ack()
            return message

    @backoff.on_exception(**settings.backoff_config)
    async def close(self) -> None:
        """
        Closes the RabbitMQ queue and connection.

        Unbinds the queue from the exchange, deletes the queue, and closes the connection.
        """
        if self.queue:
            await self.queue.unbind(self.exchange, self.routing_key)
            await self.queue.delete()
        if self.connection:
            await self.connection.close()
