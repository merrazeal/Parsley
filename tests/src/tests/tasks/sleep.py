import asyncio


async def sleep_task(timeout: int):
    await asyncio.sleep(timeout)
