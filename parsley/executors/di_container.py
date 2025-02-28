import asyncio
import logging

from parsley.message import Message
from parsley.ports.di.container import BaseExecutorQueueContainer


class LocalExecutorQueueContainer(BaseExecutorQueueContainer):
    def __init__(self, logger: logging.Logger = logging.getLogger("")):
        self.logger = logger

    async def initialize(self) -> None:
        self._queue = asyncio.Queue()
        self.logger.info("LocalExecutorQueueContainer initialized successfully")

    async def empty(self) -> bool:
        return self._queue.empty()

    async def get(self) -> Message:
        return await self._queue.get()

    async def put(self, message: Message) -> None:
        await self._queue.put(message)

    async def close(self) -> None:
        ...
