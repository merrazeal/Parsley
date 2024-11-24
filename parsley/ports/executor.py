from abc import ABC, abstractmethod

from parsley.message import InputData


class BaseAsyncExecutor(ABC):
    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def _execute(self, task_name: str, input_data: InputData) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def run(self) -> None: ...
