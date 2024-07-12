import asyncio

from data_storage import DataStorage

DS = DataStorage()


class Parser:
    async def run_parser(self):
        pass


if __name__ == "__main__":
    parser = Parser()
    asyncio.run(parser.run_parser())
