# Parsley

Parsley is a simple asynchronous task manager.

## Installation

```bash
pip install git+https://github.com/merrazeal/Parsley.git
```

## Redis Usage
### Requierements
```
redis==5.2.0
```

### You need to declare the following environment variables:
#### Required:
- `PARSLEY__MESSAGE_EXECUTE_INTERVAL`: The frequency at which tasks will be executed by the executor.
- `PARSLEY__REDIS_HOST`: Host address of the Redis server.
- `PARSLEY__REDIS_PORT`: Port number for the Redis server.
- `PARSLEY__REDIS_DB`: Redis database index number to use.
#### Optional:
- `PARSLEY__REDIS_USERNAME (default: None)`: Username for authenticating with Redis.
- `PARSLEY__REDIS_PASSWORD (default: None)`: Password for authenticating with Redis.

### Simple worker example:
```python
import asyncio
import logging
from contextlib import asynccontextmanager
from logging import config as logging_config

from parsley.consumers.redis import AsyncRedisConsumer
from parsley.executors import SimpleAsyncTaskExecutor
from parsley.worker import AsyncTaskWorker


@asynccontextmanager
async def get_worker(consumer, task_executor, logger=logging.getLogger(""), blocking=False):
    worker = AsyncTaskWorker(
        consumer=consumer,
        task_executor=task_executor,
        logger=logger,
        blocking=blocking,
    )
    yield worker
    await worker.close()

async def main():
    logging_config.dictConfig(LOGGING)  # your log_conf
    async with get_worker(
        consumer=AsyncRedisConsumer(
            channel_name="your_channel_name", logger=logging.getLogger("consumer")
        ),
        task_executor=SimpleAsyncTaskExecutor(
            task_registry={
                "your_async_func_task_name": "your_task_module.your_task_module",
            },
            logger=logging.getLogger("executor"),
        ),
        logger=logging.getLogger("worker"),
        blocking=True,
    ) as worker:
        await worker.run()

if __name__ == '__main__':
    asyncio.run(main())
```
- The task registry module value should match the Python import path, like PYTHONPATH/your_module.your_module.
- You can also add the worker(like listener) in the `on startup` and `on shutdown` events, or within the `lifespan` context to manage the lifecycle of the worker. Ensure that the worker is **non-blocking** (blocking=False)


### Simple producer example:

```python
from contextlib import asynccontextmanager

from parsley.producers.redis import AsyncRedisProducer


@asynccontextmanager
async def get_producer(channel_name):
    producer = AsyncRedisProducer(channel_name=channel_name)
    yield producer
    await producer.close()


async def test():
    async with get_producer("your_channel_name") as test_producer:
        await test_producer.produce("your_func_name", *your_func_args, **your_func_kwargs)

```

- `your_func_name` - This is the name of the task, which corresponds to a consumer task that will be processed.
- `your_func_args(not required)` - These are the positional arguments passed to the task in the consumer.
- `your_func_kwargs(not required)` - These are the keyword arguments passed to the task in the consumer.

## RabbitMQ Usage
### Requierements
```
aio-pika==9.5.3
```

### You need to declare the following environment variables:
#### Required:
- `PARSLEY__RABBITMQ_HOST`: Host address of the RabbitMQ server.
- `PARSLEY__RABBITMQ_PORT`: Port number for the RabbitMQ server.
- `PARSLEY__RABBITMQ_USER`: Username for authenticating with the RabbitMQ server.
- `PARSLEY__RABBITMQ_PASSWORD`: Password for authenticating with the RabbitMQ server.
- `PARSLEY__RABBITMQ_VHOST`: Virtual host to use on the RabbitMQ server (must also be configured in RabbitMQ).

#### Optional:
- `PARSLEY__RABBITMQ_EMPTY_QUEUE_DELAY (default: 1)`: Delay (in seconds) before retrying when the queue is empty.

### Simple worker example:
```python
import asyncio
import logging
from contextlib import asynccontextmanager
from logging import config as logging_config

from parsley.consumers.rabbitmq import AsyncRabbitMQConsumer
from parsley.executors import SimpleAsyncTaskExecutor
from parsley.worker import AsyncTaskWorker


@asynccontextmanager
async def get_worker(consumer, task_executor, logger=logging.getLogger("consumer"), bloking=False):
    worker = AsyncTaskWorker(
        consumer=consumer,
        task_executor=task_executor,
        logger=logger,
        blocking=bloking,
    )
    yield worker
    await worker.close()


async def main():
    logging_config.dictConfig(LOGGING)  # your log_conf
    async with get_worker(
        consumer=AsyncRabbitMQConsumer(
            queue_name="your_channel_name", logger=logging.getLogger("consumer")
        ),
        task_executor=SimpleAsyncTaskExecutor(
            task_registry={
                "your_async_func_task_name": "your_task_module.your_task_module",
            },

            logger=logging.getLogger("executor"),
        ),
        bloking=True,
    ) as worker:
        await worker.run()


if __name__ == '__main__':
    asyncio.run(main())

```
- The task registry module value should match the Python import path, like PYTHONPATH/your_module.your_module.
- You can also add the worker(like listener) in the `on startup` and `on shutdown` events, or within the `lifespan` context to manage the lifecycle of the worker. Ensure that the worker is **non-blocking** (blocking=False)

### Simple producer example:

```python
import asyncio
from contextlib import asynccontextmanager

from parsley.producers.rabbitmq import AsyncRabbitMQProducer



@asynccontextmanager
async def get_producer(channel_name):
    producer = AsyncRabbitMQProducer(queue_name=channel_name)
    await producer.initialize()
    yield producer
    await producer.close()


async def test():
    async with get_producer("your_channel_name") as test_producer:
        await test_producer.produce("your_func_name", *your_func_args, **your_func_kwargs)

if __name__ == "__main__":
    asyncio.run(test())

```
- `your_func_name` - This is the name of the task, which corresponds to a consumer task that will be processed.
- `your_func_args(not required)` - These are the positional arguments passed to the task in the consumer.
- `your_func_kwargs(not required)` - These are the keyword arguments passed to the task in the consumer.

## Task registry full example

We have the `/app/` directory set as the PYTHONPATH.
Inside this directory, there is a module called `hello_module`, and within it, a file `hello.py` that contains an asynchronous function `hello_world()` (our task).

In this case, the task registry should look like this:
```python
task_registry = {
    "hello_world": "hello_module.hello",
}
```