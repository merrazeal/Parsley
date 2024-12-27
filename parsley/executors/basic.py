import asyncio
import logging
from importlib import import_module

from parsley.message import InputData, Message
from parsley.ports.executor import BaseAsyncExecutor
from parsley.ports.di.container import BaseExecutorQueueContainer
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
        for task_name, module in self.task_registry.items():
            task_module = import_module(module)
            task = getattr(task_module, task_name)
            if task:
                self.tasks[task_name] = task
        self.logger.info(f"Tasks initialize successfuly: {self.tasks}")

    async def _execute(self, task_name: str, input_data: InputData) -> None:
        """Executes a specific task."""
        self.logger.info(f"Starting task: {task_name} with input data: {input_data}")
        task = self.tasks[task_name]
        try:
            await task(*input_data.args, **input_data.kwargs)
        except Exception as e:
            self.logger.error(f"Error occurred while executing task '{task_name}': {e}")
        else:
            self.logger.info(f"Completed task: '{task_name}'")

    async def run(self) -> None:
        """Periodically polls the execution queue and processes tasks."""
        while True:
            await asyncio.sleep(settings.message_execute_interval)
            self.logger.info("🚀 Starting task execution...")
            if await self.di_queue_container.empty():
                self.logger.info("📭 No incoming messages to execute.")
                continue
            while not await self.di_queue_container.empty():
                message: Message = await self.di_queue_container.get()
                task = self.tasks.get(message.task_name)
                if task:
                    await self._execute(message.task_name, message.input_data)
            self.logger.info("Executed all accumulated messages.")

    async def close(self):
        await self.di_queue_container.close()
