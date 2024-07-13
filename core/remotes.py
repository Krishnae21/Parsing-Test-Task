import asyncio
from typing import Any
import httpx
from loguru import logger
from pydantic_core import Url

from core.protocols import ClientSettingsProtocol
from config.settings import SETTINGS
from core.utils import handle_http_errors


class AllRequestsFailedError(Exception):
    """Exception для случаев когда вообще не получили ответ ни для одного запроса"""

    message = "Ни один запрос не был успешно обработан"


class BaseClient:
    """Базовый Адаптер"""

    def __init__(self) -> None:
        self._settings: ClientSettingsProtocol
        self._client: httpx.AsyncClient

    async def fetch_data(self, url: Url | None = None) -> Any:
        """Основная функа для получения данных"""
        if url is None:
            url = Url(self._settings.base_url)

        if self._settings.enable_duplicate_requests:
            try:
                return await self._fetch_with_duplicates()
            except AllRequestsFailedError as exc:
                logger.error(exc.message)
        else:
            try:
                return await self._fetch_single()
            except Exception as exc:
                logger.error(exc)

    @handle_http_errors
    async def _fetch_single(self) -> str:
        """Запрос один раз"""
        res = await self._client.get(self._settings.base_url)
        res.raise_for_status()
        logger.info("Ответ получен")
        return res.text

    async def _fetch_with_duplicates(self) -> str | None:
        """
        Дублирование запросов.
        logic:
            1. Создаем
            2. ждем done
            3. идем по всем в done (может быть несколько так-как ошибочные могут упасть сразу же)
            4. Если не упал, то отменяем остальные
                Иначе пункт 2
        """
        pending = {asyncio.create_task(self._fetch_single()) for _ in range(self._settings.count_duplicate_request)}

        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                try:
                    result = task.result()
                    if result:
                        for t in pending:
                            t.cancel()
                            logger.debug(f"Отменяю таск {str(t.get_name())}")
                        return result

                except Exception as exc:  # noqa: PERF203
                    logger.warning(f"Запрос упал {exc}")

        raise AllRequestsFailedError


class MoexClient(BaseClient):
    """Адаптер для MOEX"""

    def __init__(self) -> None:
        self._settings = SETTINGS.moex_settings
        self._client = httpx.AsyncClient(
            timeout=self._settings.timeout,
        )


class RandomMoexClient(MoexClient):
    """
    Адаптер для MOEX. Добавляем случайности для падения запросов.
    """

    RANDOM = 0.2  # NOTE: можно поиграться со значениями

    @handle_http_errors
    async def _fetch_single(self) -> str:
        import random

        if random.random() < self.RANDOM:  # noqa: S311
            raise httpx.RequestError("MOEX: Random error")
        res = await self._client.get(self._settings.base_url)
        res.raise_for_status()

        logger.info("Ответ получен")
        return res.text
