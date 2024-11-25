# Parsley

Parsley is a simple asynchronous task manager.

## Installation

```bash
pip install git+https://github.com/merrazeal/Parsley.git
```

## Usage
### You need to declare the following environment variables:
- `PARSLEY__MESSAGE_EXECUTE_INTERVAL`: The frequency at which tasks will be executed by the executor.
- `PARSLEY__REDIS_HOST`: Host address of the Redis server.
- `PARSLEY__REDIS_PORT`: Port number for the Redis server.
- `PARSLEY__REDIS_DB`: Redis database index number to use.

### Simple worker example:
```python
from contextlib import asynccontextmanager
from logging import config as logging_config

from parsley.consumers.redis import AsyncRedisConsumer
from parsley.executors import AsyncTaskExecutor
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
        task_executor=AsyncTaskExecutor(
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
- The task registry name should correspond to the Python path, such as `PYTHONPATH/your_task_module.your_task_module`
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

- your_func_name - This is the name of the task, which corresponds to a consumer task that will be processed.
- your_func_args - These are the positional arguments passed to the task in the consumer.
- your_func_kwargs - These are the keyword arguments passed to the task in the consumer.

