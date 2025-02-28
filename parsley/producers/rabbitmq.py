import asyncio
import logging

from aio_pika import Message as AioPikaMessage
from aio_pika import connect
import backoff

from parsley.message import MessageBuilder
from parsley.ports.producer import BaseAsyncProducer
from parsley.settings import settings


class AsyncRabbitMQProducer(BaseAsyncProducer):
    def __init__(
        self, queue_name, logger: logging.Logger = logging.getLogger("")
    ) -> None:
        self.queue_name = queue_name
        self.routing_key = queue_name  # for direct exchange
        self.logger = logger

    @backoff.on_exception(**settings.backoff_config)
    async def initialize(self):
        self.connection = await connect(
            settings.rabbitmq_url, loop=asyncio.get_running_loop()
        )
        self.channel = await self.connection.channel()
        self.logger.info("AsyncRabbitMQProducer initialized successfully")

    @backoff.on_exception(**settings.backoff_config)
    async def produce(self, task_name, *args, **kwargs):
        message = MessageBuilder.build(task_name, *args, **kwargs)
        await self.channel.default_exchange.publish(
            AioPikaMessage(
                message.model_dump_json().encode("utf-8"),
                content_type="application/json",
            ),
            self.routing_key,
        )

    @backoff.on_exception(**settings.backoff_config)
    async def close(self) -> None:
        await self.connection.close()
