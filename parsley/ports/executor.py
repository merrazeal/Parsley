from abc import ABC, abstractmethod


class BaseAsyncExecutor(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def run(self) -> None:
        ...
