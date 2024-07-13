import asyncio

from config.logging import setup_logger
from data_storage import DataStorage, EchoDataStorage

from typing import NoReturn
from core.data_processors import DataProcessor
from core.enums import TypeParserEnum
from core.remotes import MoexClient, RandomMoexClient
from config.settings import SETTINGS
from core.protocols import (
    ClientProtocol,
    DataProcessorProtocol,
    DataStorageProtocol,
)


class Parser:
    """Фабрика и раннер"""

    def __init__(self, type_parser: TypeParserEnum = TypeParserEnum.MOEX) -> None:
        self.type_parser: TypeParserEnum = type_parser
        self._client: ClientProtocol
        self._storage: DataStorageProtocol
        self._data_processor: DataProcessorProtocol

    async def run_parser(self) -> NoReturn:
        self._initialize()
        while True:
            if not (raw_data := await self._client.fetch_data()):
                continue
            processed_data = await self._data_processor.process_data(raw_data)
            task = asyncio.create_task(self._storage.add_data(processed_data))
            asyncio.shield(task)

            await asyncio.sleep(SETTINGS.request_interval)

    def _initialize(self) -> None:
        """Собираем согласно типу"""
        match self.type_parser:
            case TypeParserEnum.MOEX:
                self._client = MoexClient()
                self._storage = DataStorage()
                self._data_processor = DataProcessor()

            case TypeParserEnum.MOEX_RANDOM:
                self._client = RandomMoexClient()
                self._storage = EchoDataStorage()
                self._data_processor = DataProcessor()

            # EXAMPLE:
            # case TypeParserEnum.NASDAQ:
            #     self._client = NasdaqClient()
            #     self._storage = DataStorage()
            #     self._data_processor = DataProcessor()
            case _:
                raise NotImplementedError


if __name__ == "__main__":
    parser = Parser()
    # parser = Parser(TypeParserEnum.MOEX_RANDOM) # NOTE: вкл для симуляции ошибок и логгирования ответа
    setup_logger()
    asyncio.run(parser.run_parser())
