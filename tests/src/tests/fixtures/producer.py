import pytest_asyncio

from parsley.producers.redis import AsyncRedisProducer
from parsley.producers.rabbitmq import AsyncRabbitMQProducer
from tests.src.core.settings import settings


@pytest_asyncio.fixture(scope="session")
async def redis_producer():
    producer = AsyncRedisProducer(queue_name=settings.redis_channel_name)
    await producer.initialize()
    yield producer
    await producer.close()


@pytest_asyncio.fixture(scope="session")
async def rabbitmq_producer():
    producer = AsyncRabbitMQProducer(queue_name=settings.rabbitmq_queue_name)
    await producer.initialize()
    yield producer
    await producer.close()
