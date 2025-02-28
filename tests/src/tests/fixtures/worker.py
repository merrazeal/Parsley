import asyncio
import pytest_asyncio

from parsley.executors.basic import AsyncTaskExecutor
from parsley.consumers.redis import AsyncRedisConsumer
from parsley.consumers.rabbitmq import AsyncRabbitMQConsumer
from parsley.executors.di_container import LocalExecutorQueueContainer
from parsley.worker import AsyncTaskWorker
from tests.src.core.settings import settings


@pytest_asyncio.fixture(scope="session", autouse=True)
async def redis_worker():
    worker = AsyncTaskWorker(
        consumer=AsyncRedisConsumer(
            queue_name=settings.redis_channel_name
        ),
        task_executor=AsyncTaskExecutor(
            task_registry={
                "sleep_task": "tests.src.tests.tasks.sleep",
            },
            di_queue_container=LocalExecutorQueueContainer(),
        ),
        blocking=False,
    )
    await worker.run()
    yield worker
    await worker.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def rabbitmq_worker():
    worker = AsyncTaskWorker(
        consumer=AsyncRabbitMQConsumer(
            queue_name=settings.rabbitmq_queue_name
        ),
        task_executor=AsyncTaskExecutor(
            task_registry={
                "sleep_task": "tests.src.tests.tasks.sleep",
            },
            di_queue_container=LocalExecutorQueueContainer(),
        ),
        blocking=False,
    )
    await worker.run()
    yield worker
    await worker.close()
