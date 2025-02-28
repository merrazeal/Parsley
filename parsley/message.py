import uuid
from typing import Any

from pydantic import BaseModel


class InputData(BaseModel):
    args: list[Any]
    kwargs: dict[str, Any]


class Message(BaseModel):
    id: uuid.UUID
    task_name: str
    input_data: InputData


class MessageBuilder:
    @classmethod
    def build(cls, func_name, *args, **kwargs) -> Message:
        return Message(
            id=uuid.uuid4(),
            task_name=func_name,
            input_data=InputData(args=args, kwargs=kwargs),
        )
