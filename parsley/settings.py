from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    message_execute_interval: int
    redis_host: str
    redis_port: int
    redis_db: int

    class Config:
        env_prefix = "PARSLEY__"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
