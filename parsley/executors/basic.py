import asyncio
import logging
from importlib import import_module

from parsley.message import Message
from parsley.ports.di.container import BaseExecutorQueueContainer
from parsley.ports.executor import BaseAsyncExecutor
from parsley.settings import settings


class AsyncTaskExecutor(BaseAsyncExecutor):
    """Executor class responsible for executing tasks based on messages from queue."""

    def __init__(
        self,
        task_registry: dict[str, str],
        di_queue_container: BaseExecutorQueueContainer,
        logger: logging.Logger = logging.getLogger(""),
    ) -> None:
        self.tasks = {}
        self.task_registry = task_registry
        self.logger = logger
        self.di_queue_container = di_queue_container

    async def initialize(self) -> None:
        """Initializes task executor by dynamically loading tasks from task registry."""
        await self.di_queue_container.initialize()
        for task_name, module in self.task_registry.items():
            task_module = import_module(module)
            task = getattr(task_module, task_name)
            if task:
                self.tasks[task_name] = task
        self.logger.info(f"AsyncTaskExecutor initialize successfuly: {self.tasks}")

    async def run(self) -> None:
        """Periodically polls the execution queue and processes tasks."""
        while True:
            await asyncio.sleep(settings.tasks_execute_interval)
            self.logger.info("🚀 Starting task execution...")
            if await self.di_queue_container.empty():
                self.logger.info("📭 No incoming messages to execute.")
                continue
            while not await self.di_queue_container.empty():
                message: Message = await self.di_queue_container.get()
                task = self.tasks.get(message.task_name)
                if task:
                    future = task(*message.input_data.args, **message.input_data.kwargs)
                    asyncio.create_task(future)
            self.logger.info("Executed all accumulated messages.")

    async def close(self):
        await self.di_queue_container.close()
