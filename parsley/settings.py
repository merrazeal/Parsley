from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General conf
    message_execute_interval: int

    # Redis conf
    redis_host: str | None = None
    redis_port: int | None = None
    redis_db: int | None = None
    redis_password: str | None = None
    redis_username: str | None = None
    redis_max_wait_poll_time: int = 5

    # RabbitMQ conf
    rabbitmq_host: str | None = None
    rabbitmq_port: int | None = None
    rabbitmq_user: str | None = None
    rabbitmq_password: str | None = None
    rabbitmq_vhost: str | None = None
    rabbimq_empty_queue_delay: int = 1
    rabbitmq_max_wait_poll_time: int = 5

    class Config:
        env_prefix = "PARSLEY__"

    @property
    def rabbitmq_url(self):
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}/{self.rabbitmq_vhost}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
