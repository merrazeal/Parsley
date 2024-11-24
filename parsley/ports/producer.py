from abc import ABC, abstractmethod


class BaseAsyncProducer(ABC):
    @abstractmethod
    async def initialize(self): ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def produce(self, task_name, *args, **kwargs): ...
