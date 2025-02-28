from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbitmq_queue_name: str = "parslsey_test"
    redis_channel_name: str = "parsley_test"
    execute_interval: int = Field(..., validation_alias="PARSLEY__TASKS_EXECUTE_INTERVAL")


@lru_cache(maxsize=1)
def get_settings():
    return Settings()


settings = get_settings()
