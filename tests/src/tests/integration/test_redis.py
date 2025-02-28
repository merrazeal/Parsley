import asyncio
from unittest.mock import AsyncMock

import pytest

from tests.src.core.settings import settings


pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_task_execution(redis_worker, redis_producer, test_logger):
    assert "sleep_task" in redis_worker.task_executor.tasks
    assert await redis_worker.task_executor.di_queue_container.empty()
    mock_task = AsyncMock()
    redis_worker.task_executor.tasks["sleep_task"] = mock_task
    await redis_producer.produce("sleep_task", 1)
    await asyncio.sleep(settings.execute_interval)
    mock_task.assert_called_once_with(1)
    assert await redis_worker.task_executor.di_queue_container.empty()
    test_logger.info("Redis-based task management system integration test completed successfully")
