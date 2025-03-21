import asyncio
import logging

from parsley.message import Message
from parsley.ports.consumer import BaseAsyncConsumer
from parsley.ports.executor import BaseAsyncExecutor
from parsley.ports.worker import BaseAsyncTaskWorker


class AsyncTaskWorker(BaseAsyncTaskWorker):
    def __init__(
        self,
        consumer: BaseAsyncConsumer,
        task_executor: BaseAsyncExecutor,
        blocking: bool = False,
        logger: logging.Logger = logging.getLogger(""),
    ) -> None:
        self.logger = logger
        self.consumer = consumer
        self.task_executor = task_executor
        self.blocking = blocking

    async def _poll(self) -> None:
        """Polls for new messages and pushes them to the task executor's queue.

        Сonsumer will wait for a message for a specified timeout.
        """
        while True:
            new_message: Message | None = await self.consumer.consume()
            if new_message:
                self.logger.info(f"New messages received: {new_message}")
                await self.task_executor.di_queue_container.put(new_message)

    async def run(self) -> None:
        """Starts the task worker. Initializes both the consumer and executor,
        and begins processing messages
        """
        await self.task_executor.initialize()
        await self.consumer.initialize()
        self.logger.info("Starting to consume messages")
        asyncio.create_task(self.task_executor.run())
        if self.blocking:
            await self._poll()
        else:
            asyncio.create_task(self._poll())

    async def close(self) -> None:
        """Closes the consumer and executor, releasing any resources."""
        await self.consumer.close()
        await self.task_executor.close()
