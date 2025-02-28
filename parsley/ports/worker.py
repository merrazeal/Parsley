from abc import ABC, abstractmethod


class BaseAsyncTaskWorker(ABC):
    @abstractmethod
    async def run(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...
