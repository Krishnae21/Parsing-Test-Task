import asyncio
from typing import Any

from loguru import logger


class DataStorage:
    async def add_data(self, data):
        await asyncio.sleep(1)


class EchoDataStorage:
    """Test Storage. Сон увеличен. Логирование части ответа"""

    async def add_data(self, data: Any) -> None:
        await asyncio.sleep(3)
        logger.info(f"Часть данных: {data[:10]}")
