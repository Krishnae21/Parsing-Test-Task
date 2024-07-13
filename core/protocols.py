# ruff: noqa: ANN001 ANN201
from typing import Protocol


class DataStorageProtocol(Protocol):
    async def add_data(self, data): ...


class ClientProtocol(Protocol):
    async def fetch_data(self, url=None): ...


class DataProcessorProtocol(Protocol):
    async def process_data(self, data): ...


class ClientSettingsProtocol(Protocol):
    base_url: str
    timeout: float
    enable_duplicate_requests: bool
    count_duplicate_request: int
