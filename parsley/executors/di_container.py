

import asyncio
from parsley.message import Message
from parsley.ports.di.container import BaseExecutorQueueContainer


class LocalExecutorQueueContainer(BaseExecutorQueueContainer):
    async def initialize(self) -> None:
        self.__queue = asyncio.Queue()

    async def empty(self) -> bool:
        return self.__queue.empty()

    async def get(self) -> Message:
        return await self.__queue.get()

    async def put(self, message: Message) -> None:
        await self.__queue.put(message)

    async def close(self) -> None:
        ...
