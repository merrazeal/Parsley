from abc import ABC, abstractmethod

from parsley.message import Message


class BaseAsyncConsumer(ABC):
    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def consume(self) -> Message | None: ...

    @abstractmethod
    async def close(self) -> None: ...
