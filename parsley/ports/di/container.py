from abc import ABC, abstractmethod

from parsley.message import Message


class BaseExecutorQueueContainer(ABC):
    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def empty(self) -> bool: ...

    @abstractmethod
    async def get(self) -> Message: ...

    @abstractmethod
    async def put(self, message: Message) -> None: ...
